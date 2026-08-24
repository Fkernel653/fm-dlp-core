"""Persistent download path storage using JSON config file."""

from pathlib import Path

from ...utils import echo, echo_error
from ..colors import (
    BOLD_GREEN,
    error,
    hint,
    info,
    set_colors,
    styled,
)
from . import CONFIG_FILE, load_config, update_config

PATH_KEY: str = "path"


def set_path(
    path: str,
    color: bool = True,
) -> str:
    """
    Set and save the download directory path to persistent configuration.

    Validates the provided path by:
    1. Resolving it to an absolute path (expanding ~ and resolving symlinks)
    2. Checking that it exists and is a directory
    3. Creating parent directories if they don't exist

    If validation passes, saves the path to the configuration file under the
    `path` key. If validation fails, exits with an error message.

    Args:
        path (str): Directory path for downloads. Can be absolute or relative,
                    and may include ~ for home directory expansion.
        color (bool): Enable colored output in success/error messages. (default: True)

    Returns:
        str: Success message indicating the path was saved, including the
             configured path and config file location.

    Raises:
        SystemExit: If the path doesn't exist, is not a directory, or if
                    permission is denied when writing to the config file.
    """
    set_colors(color)
    try:
        input_path = str(Path(path).expanduser().resolve())

        if not Path(input_path).is_dir():
            echo_error("Please enter the correct path!")

        config = load_config(color)
        config[PATH_KEY] = input_path

        if not update_config(config):
            raise PermissionError()

        return styled("Configuration saved successfully", BOLD_GREEN)

    except PermissionError:
        return error(f"Permission denied! Cannot write to {CONFIG_FILE}")
    except OSError as e:
        return error(f"Error saving configuration: {e}")


def get_path(
    color: bool = True,
) -> str:
    """
    Get the configured download directory path from persistent storage.

    Returns the saved path from the configuration file or defaults to the
    user's home directory if no configuration exists. If a saved path exists
    but is invalid (doesn't exist or is not a directory), exits with an error.

    This function is typically called when the user hasn't explicitly specified
    a download path via command-line arguments, allowing the saved preference
    to be used automatically.

    Args:
        color (bool): Enable colored output in info and error messages. (default: True)

    Returns:
        str: The resolved download directory path as an absolute string.

    Raises:
        SystemExit: If the saved path doesn't exist or is not a directory.
    """
    if not CONFIG_FILE.exists():
        echo(info("Home directory is used!"))
        echo(hint("Run the 'config' command to configure the download path\n"))
        return str(Path.home())

    data = load_config(color)
    download_path = str(data.get(PATH_KEY))

    if not download_path or not Path(download_path).is_dir():
        set_colors(color)
        echo_error("Download path does not exist.")

    return download_path
