"""
Configuration management for fm-dlp using persistent JSON storage.

This module handles reading, writing, and managing application configuration
including download paths and download parameters. Configuration is stored
in a platform-specific user config directory:

- Windows: %LOCALAPPDATA%\\fm-dlp\\config.json
- macOS: ~/Library/Application Support/fm-dlp/config.json
- Linux: $XDG_CONFIG_HOME/fm-dlp/config.json or ~/.config/fm-dlp/config.json

The configuration is cached for performance using LRU caching, with automatic
cache invalidation on updates.

Functions:
    get_config_dir: Get the platform-specific config directory path.
    update_config: Write configuration data to the JSON file.
    load_config: Load configuration from the JSON file with caching.

Constants:
    CONFIG_DIR: The resolved configuration directory path.
    CONFIG_FILE: The full path to the config.json file.

Example:
    >>> from fm_dlp_core.utils.config import load_config, update_config
    >>> config = load_config(color=True)
    >>> config["path"] = "/downloads"
    >>> update_config(config)
    True
"""

import json
import os
import sys
from functools import lru_cache
from pathlib import Path

from ...utils import echo
from ..colors import error, set_colors


def get_config_dir(dir_name: str = "fm-dlp") -> str:
    """
    Get the user configuration directory path based on the operating system.

    Returns the appropriate platform-specific config directory:
    - Windows: %LOCALAPPDATA%\\{dir_name} or %APPDATA%\\{dir_name}
    - macOS: ~/Library/Application Support/{dir_name}
    - Linux/Unix: $XDG_CONFIG_HOME/{dir_name} or ~/.config/{dir_name}

    This follows standard conventions for each platform, ensuring configuration
    files are stored in the expected location for the user's operating system.

    Args:
        dir_name (str, optional): Name of the application directory to create
                                  under the config root. Defaults to "fm-dlp".

    Returns:
        str: The absolute path to the configuration directory.
    """
    home = Path.home()

    if sys.platform == "win32":
        appdata = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA")
        d = Path(appdata) if appdata else (home / "AppData" / "Local")
    elif sys.platform == "darwin":
        d = home / "Library" / "Application Support"
    else:
        xdg = os.environ.get("XDG_CONFIG_HOME")
        d = Path(xdg) if xdg else (home / ".config")

    return str(d / dir_name)


CONFIG_DIR = get_config_dir()
CONFIG_FILE = Path(CONFIG_DIR) / "config.json"


def update_config(data: dict, encoding: str = "utf-8") -> bool:
    """
    Update configuration data to the JSON file, creating directories if needed.

    Writes the provided dictionary to the config JSON file with pretty formatting
    (indent=4, ensure_ascii=False for Unicode support). Automatically creates
    the parent config directory if it doesn't exist. Clears the cached config
    after writing to ensure subsequent loads fetch fresh data.

    Args:
        data (dict): Dictionary containing the complete configuration data to write.
        encoding (str, optional): File encoding for the JSON file.
                                  Defaults to "utf-8".

    Returns:
        bool: True if the configuration was updated successfully, False if a
              permission error or I/O error occurred.
    """
    try:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding)
        load_config.cache_clear()
        return True
    except (PermissionError, OSError):
        return False


@lru_cache(maxsize=1)
def load_config(color: bool, encoding: str = "utf-8") -> dict:
    """
    Load configuration from the JSON file with caching for performance.

    Reads and parses the config JSON file. Uses LRU caching (maxsize=1) so
    repeated calls within the same session don't hit the filesystem repeatedly.
    The cache is automatically cleared when `update_config` is called.

    If the config file doesn't exist, returns an empty dictionary. If the file
    exists but is corrupted (invalid JSON), logs an error, returns an empty dict,
    and the caller can then write a fresh config.

    Args:
        color (bool): Enable colored output for error messages when the config
                      file is corrupted.
        encoding (str, optional): File encoding for reading the JSON file.
                                  Defaults to "utf-8".

    Returns:
        dict: Parsed configuration dictionary, or empty dict if the file doesn't
              exist or is corrupted.
    """
    if not CONFIG_FILE.exists():
        return {}
    try:
        return json.loads(CONFIG_FILE.read_text(encoding))
    except (json.JSONDecodeError, OSError):
        set_colors(color)
        echo(error("Config file is corrupted. Creating new one..."), file=sys.stderr)
        return {}
