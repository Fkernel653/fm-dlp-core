from pathlib import Path

from ...utils import set_colors
from .config_manager import ConfigManager
from .params import ConfigParams


class PathManager:
    """
    Manage the download path stored in the configuration file.

    This class provides methods to read and write the ``path`` key of the
    application's TOML configuration. When no configuration file exists,
    the user's home directory is used as a fallback.

    Attributes:
        params (ConfigParams): Configuration parameters (quiet, color, config_file).
        config_manager (ConfigManager): Underlying config manager.
        path_key (str): Config key for the download path.
    """

    def __init__(self, params: ConfigParams):
        self.params = params
        self.config_manager = ConfigManager(params)
        self.path_key = "path"
        set_colors(params.color)

    def set_path(self, path: str) -> None:
        """
        Validate and save the download path to the configuration file.

        Args:
            path (str): The path to the download directory. Tilde (``~``) is expanded.

        Returns:
            None
        """
        try:
            input_path = str(Path(path).expanduser().resolve())

            if not Path(input_path).is_dir():
                self.config_manager._if_quiet(
                    self.params.quiet,
                    "Please enter the correct path!",
                    error_result=True,
                )
                return

            config = self.config_manager.load_config()
            config[self.path_key] = input_path

            if not self.config_manager.update_config(config):
                self.config_manager._if_quiet(
                    self.params.quiet,
                    f"Permission denied! Cannot write to "
                    f"{self.config_manager.config_file}",
                    error_result=True,
                )
                return

            self.config_manager._if_quiet(
                self.params.quiet,
                "Configuration saved successfully",
                success_result=True,
            )

        except OSError as e:
            self.config_manager._if_quiet(
                self.params.quiet,
                f"Error saving configuration: {e}",
                error_result=True,
            )

    def get_path(self) -> str:
        """
        Retrieve the download path from the configuration file.

        If no configuration file exists, the user's home directory is returned
        along with an informational hint. If the stored path is missing or no
        longer a valid directory, an error message is shown and the home
        directory is returned as a fallback.

        Returns:
            str: The resolved download directory path.
        """
        if not self.config_manager.config_file.exists():
            self.config_manager._if_quiet(
                self.params.quiet,
                "Configuration file not found",
                error_result=True,
                exit_on_error=False,
            )
            self.config_manager._if_quiet(
                self.params.quiet, "Home directory is used!", info_result=True
            )
            return str(Path.home())

        data = self.config_manager.load_config()
        download_path = data.get(self.path_key)

        if not download_path or not Path(str(download_path)).is_dir():
            self.config_manager._if_quiet(
                self.params.quiet,
                "Download path does not exist. Home directory is used!",
                error_result=True,
            )
            return str(Path.home())

        return str(download_path)
