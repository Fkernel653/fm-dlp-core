"""
Configuration management for fm-dlp using persistent TOML storage.

This module handles reading, writing, and managing application configuration
including download paths and download parameters. Configuration is stored
in a platform-specific user config directory:

- Windows: %LOCALAPPDATA%\\fm-dlp\\config.toml
- macOS: ~/Library/Application Support/fm-dlp/config.toml
- Linux: $XDG_CONFIG_HOME/fm-dlp/config.toml or ~/.config/fm-dlp/config.toml

The configuration is cached for performance using LRU caching, with automatic
cache invalidation on updates.

Functions:
    get_config_dir: Get the platform-specific config directory path.
    update_config: Write configuration data to the TOML file.
    load_config: Load configuration from the TOML file with caching.

Constants:
    ENCODING: Encoding for writing / reading files
    CONFIG_DIR: The resolved configuration directory path.
    CONFIG_FILE: The full path to the config.toml file.

Example:
    >>> from fm_dlp_core.utils.config import load_config, update_config
    >>> config = load_config(color=True)
    >>> config["path"] = "/downloads"
    >>> update_config(config)
    True
"""

import os
import sys
import tomllib
from functools import lru_cache
from pathlib import Path
from typing import Any

from ...utils import echo
from ..colors import error, set_colors

ENCODING: str = "utf-8"


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
CONFIG_FILE = Path(CONFIG_DIR) / "config.toml"


def _toml_dumps(data: dict[str, Any]) -> str:
    """Serialize dict to TOML string."""
    lines: list[str] = []
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"[{key}]")
            for sub_key, sub_value in value.items():
                lines.append(f"{sub_key} = {_toml_value_to_str(sub_value)}")
        else:
            lines.append(f"{key} = {_toml_value_to_str(value)}")
        lines.append("")
    return "\n".join(lines)


def _toml_value_to_str(value: Any) -> str:
    """Convert Python value to TOML string representation."""
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, list):
        items = [_toml_value_to_str(item) for item in value]
        return f"[{', '.join(items)}]"
    elif isinstance(value, dict):
        items: list[str] = []
        for k, v in value.items():
            key_str = f'"{k}"' if not isinstance(k, str) else k
            items.append(f"{key_str} = {_toml_value_to_str(v)}")
        return f"{{ {', '.join(items)} }}"
    else:
        return str(value)


def update_config(data: dict[str, Any]) -> bool:
    """
    Update configuration data to the TOML file, creating directories if needed.

    Writes the provided dictionary to the config TOML file with pretty formatting.
    Automatically creates the parent config directory if it doesn't exist. Clears
    the cached config after writing to ensure subsequent loads fetch fresh data.

    Args:
        data (dict): Dictionary containing the complete configuration data to write.

    Returns:
        bool: True if the configuration was updated successfully, False if a
              permission error or I/O error occurred.
    """
    try:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        toml_content = _toml_dumps(data)
        _ = CONFIG_FILE.write_text(toml_content, ENCODING)
        load_config.cache_clear()
        return True
    except (PermissionError, OSError):
        return False


@lru_cache(maxsize=1)
def load_config(color: bool) -> dict[str, Any]:
    """
    Load configuration from the TOML file with caching for performance.

    Reads and parses the config TOML file. Uses LRU caching (maxsize=1) so
    repeated calls within the same session don't hit the filesystem repeatedly.
    The cache is automatically cleared when `update_config` is called.

    If the config file doesn't exist, returns an empty dictionary. If the file
    exists but is corrupted (invalid TOML), logs an error, returns an empty dict,
    and the caller can then write a fresh config.

    Args:
        color (bool): Enable colored output for error messages when the config
                      file is corrupted.

    Returns:
        dict: Parsed configuration dictionary, or empty dict if the file doesn't
              exist or is corrupted.
    """
    if not CONFIG_FILE.exists():
        return {}
    try:
        content = CONFIG_FILE.read_text(ENCODING)
        return tomllib.loads(content)
    except (tomllib.TOMLDecodeError, OSError):
        set_colors(color)
        echo(error("Config file is corrupted. Creating new one..."), file=sys.stderr)
        return {}
