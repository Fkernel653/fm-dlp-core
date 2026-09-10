from pathlib import Path

from ...utils import (
    BOLD_GREEN,
    echo,
    echo_error,
    error,
    hint,
    info,
    set_colors,
    styled,
)
from .config_manager import CONFIG_FILE, ConfigManager


class PathManager:
    """
    Manage the download path stored in the configuration file.

    This class provides methods to read and write the ``path`` key of the
    application's TOML configuration. When no configuration file exists,
    the user's home directory is used as a fallback.

    Attributes:
        PATH_KEY (str): The configuration key under which the path is stored.
        color (bool): Whether colored output is enabled for messages.
        config_manager (ConfigManager): The underlying configuration manager.

    Example:
        >>> manager = PathManager(color=True)
        >>> manager.set_path("~/Downloads")
        'Configuration saved successfully'
        >>> manager.get_path()
        '/home/user/Downloads'
    """

    PATH_KEY = "path"

    def __init__(self, color: bool = True):
        self.color = color
        self.config_manager = ConfigManager(color)
        set_colors(self.color)

    def set_path(self, path: str) -> str:
        """
        Validate and save the download path to the configuration file.

        Args:
            path (str): The path to the download directory. Tilde (``~``) is expanded.

        Returns:
            str: A success message if the path was saved, or an error message otherwise.
        """
        try:
            input_path = str(Path(path).expanduser().resolve())

            if not Path(input_path).is_dir():
                echo_error("Please enter the correct path!")
                raise SystemExit(1)

            config = self.config_manager.load_config()
            config[self.PATH_KEY] = input_path

            if not self.config_manager.update_config(config):
                raise PermissionError()

            return styled("Configuration saved successfully", BOLD_GREEN)

        except PermissionError:
            return error(f"Permission denied! Cannot write to {CONFIG_FILE}")
        except OSError as e:
            return error(f"Error saving configuration: {e}")

    def get_path(self) -> str:
        """
        Retrieve the download path from the configuration file.

        If no configuration file exists, the user's home directory is returned
        along with an informational hint. If the stored path is missing or no
        longer a valid directory, the process exits with an error.

        Returns:
            str: The resolved download directory path.
        """
        if not CONFIG_FILE.exists():
            echo(info("Home directory is used!"))
            echo(hint("Run the 'config' command to configure the download path\n"))
            return str(Path.home())

        data = self.config_manager.load_config()
        download_path = str(data.get(self.PATH_KEY))

        if not download_path or not Path(download_path).is_dir():
            echo_error("Download path does not exist.")
            raise SystemExit(1)

        return download_path
