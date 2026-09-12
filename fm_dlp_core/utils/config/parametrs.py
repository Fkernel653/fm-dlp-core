from ...utils import echo, echo_error, set_colors, success
from .config_manager import CONFIG_FILE, ConfigManager


class ParametersManager:
    """
    Manage download parameters stored in the configuration file.

    This class provides methods to read and write the ``[parameters]``
    section of the application's TOML configuration. It handles codec,
    bitrate, quality, job count, and various boolean flags, as well as
    optional cookies and remote URL values.

    Attributes:
        param_key (str): The configuration key under which parameters are stored.
        color (bool): Whether colored output is enabled for messages.
        config_manager (ConfigManager): The underlying configuration manager.

    Example:
        >>> manager = ParametersManager(color=True)
        >>> manager.set_parameters(
        ...     codec="mp3",
        ...     kbps=320,
        ...     quality="high",
        ...     jobs=4,
        ...     quiet=False,
        ...     metadata=True,
        ...     keep=False,
        ...     only_video=False,
        ... )
        True
        >>> manager.get_parameters()["codec"]
        'mp3'
    """

    def __init__(self, color: bool = True):
        self.color = color
        self.config_manager = ConfigManager(color)
        self.param_key = "parameters"
        set_colors(color)

    def set_parameters(
        self,
        codec: str,
        kbps: int,
        quality: str,
        jobs: int,
        quiet: bool,
        metadata: bool,
        keep: bool,
        only_video: bool,
        cookies: str | None = None,
        remote: str | None = None,
    ) -> bool:
        """
        Write download parameters to the configuration file.

        Args:
            codec (str): Audio codec to use.
            kbps (int): Bitrate in kilobits per second.
            quality (str): Desired download quality.
            jobs (int): Number of parallel download jobs.
            quiet (bool): Suppress informational output when True.
            metadata (bool): Whether to embed metadata.
            keep (bool): Whether to keep intermediate files.
            only_video (bool): Whether to download only the video stream.
            cookies (str | None, optional): Path to a cookies file. Defaults to None.
            remote (str | None, optional): Remote URL to validate and store. Defaults to None.

        Returns:
            bool: True if the parameters were saved successfully, False otherwise.
        """
        try:
            config = self.config_manager.load_config()

            params: dict[str, str | int | bool | None] = {
                "codec": codec,
                "kbps": kbps,
                "quality": quality,
                "jobs": jobs,
                "quiet": quiet,
                "metadata": metadata,
                "keep": keep,
                "only_video": only_video,
            }

            if cookies:
                params["cookies"] = cookies

            if remote:
                params["remote"] = remote

            config[self.param_key] = params

            if not self.config_manager.update_config(config):
                raise PermissionError()

            self._if_quiet(
                quiet, "Parameters have been successfully saved", success_result=True
            )
            return True

        except PermissionError:
            self._if_quiet(
                quiet,
                f"Permission denied! Cannot write to {CONFIG_FILE}",
                error_result=True,
            )
            return False
        except OSError as e:
            self._if_quiet(quiet, f"Error saving configuration: {e}", error_result=True)
            return False

    def get_parameters(self) -> dict[str, str | int | bool | None]:
        """
        Retrieve download parameters from the configuration file.

        Returns:
            dict[str, str | int | bool | None]: A dictionary of stored parameters, or an empty
            dictionary if the configuration file does not exist or contains
            no parameters section.
        """
        if not CONFIG_FILE.exists():
            return {}

        config = self.config_manager.load_config()
        return config.get(self.param_key, {})

    def _if_quiet(
        self,
        quiet: bool,
        text: str,
        error_result: bool | None = None,
        success_result: bool | None = None,
    ) -> None:
        """
        Print a message unless quiet mode is enabled.

        Args:
            quiet (bool): If True, no output is produced.
            text (str): The message to display.
            error_result (bool | None, optional): If True, display as an error. Defaults to None.
            success_result (bool | None, optional): If True, display as a success. Defaults to None.
        """
        if not quiet:
            if error_result:
                echo_error(text)
            elif success_result:
                echo(success(text))
