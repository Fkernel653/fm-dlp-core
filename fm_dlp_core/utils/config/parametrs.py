from typing import Any

from ...commands.downloader.params import DownloadParams
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

    def set_parameters(self, params: DownloadParams) -> bool:
        """
        Write download parameters to the configuration file.

        Args:
            params (DownloadParams): Download parameter including codec,
                quality, number of jobs, metadata/quiet/keep flags, save path,
                cookies, remote storage, subtitles, and raw yt-dlp args. (Exclude URL)

        Returns:
            bool: True if the parameters were saved successfully, False otherwise.
        """
        try:
            config = self.config_manager.load_config()

            download_params: dict[str, Any] = {
                "codec": params.codec,
                "kbps": params.kbps,
                "quality": params.quality,
                "jobs": params.jobs,
                "quiet": params.quiet,
                "metadata": params.metadata,
                "keep": params.keep,
                "only_video": params.only_video,
                "subtitles": params.subtitles,
                "subtitle_langs": params.subtitle_langs,
                "embed_subs": params.embed_subs,
                "auto_subs": params.auto_subs,
            }

            if params.cookies:
                download_params["cookies"] = params.cookies

            if params.remote:
                download_params["remote"] = params.remote

            config[self.param_key] = params

            if not self.config_manager.update_config(config):
                raise PermissionError()

            self._if_quiet(
                params.quiet,
                "Parameters have been successfully saved",
                success_result=True,
            )
            return True

        except PermissionError:
            self._if_quiet(
                params.quiet,
                f"Permission denied! Cannot write to {CONFIG_FILE}",
                error_result=True,
            )
            return False
        except OSError as e:
            self._if_quiet(
                params.quiet, f"Error saving configuration: {e}", error_result=True
            )
            return False

    def get_parameters(self) -> dict[str, Any]:
        """
        Retrieve download parameters from the configuration file.

        Returns:
            dict[str, Any]: A dictionary of stored parameters, or an empty
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
        if not quiet:
            if error_result:
                echo_error(text)
            elif success_result:
                echo(success(text))
