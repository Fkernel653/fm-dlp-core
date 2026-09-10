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

Submodules:
    config_manager: Core configuration management including file I/O and TOML
                    serialization.
    parametrs: Parameter management for download configurations.
    path: Path management for download directories.

Classes:
    ConfigManager: Loads and updates the TOML configuration file with caching.
    ParametersManager: Reads and writes download parameters in the config.
    PathManager: Reads and writes the download path in the config.
    TOMLSerializer: Serializes Python dictionaries to TOML format.

Functions:
    get_config_dir: Get the platform-specific config directory path.

Constants:
    ENCODING: Encoding for writing / reading files.
    CONFIG_DIR: The resolved configuration directory path.
    CONFIG_FILE: The full path to the config.toml file.

Example:
    >>> from fm_dlp_core.utils.config import ConfigManager, PathManager
    >>> manager = ConfigManager(color=True)
    >>> config = manager.load_config()
    >>> config["path"] = "/downloads"
    >>> manager.update_config(config)
    True
    >>> path_manager = PathManager()
    >>> path_manager.get_path()
    '/downloads'
"""

from .config_manager import (
    CONFIG_DIR,
    CONFIG_FILE,
    ENCODING,
    ConfigManager,
    TOMLSerializer,
    get_config_dir,
)
from .parametrs import ParametersManager
from .path import PathManager

__all__ = [
    "CONFIG_DIR",
    "CONFIG_FILE",
    "ENCODING",
    "ConfigManager",
    "ParametersManager",
    "PathManager",
    "TOMLSerializer",
    "get_config_dir",
]
