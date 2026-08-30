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
    TOMLSerializer: Serializes Python dictionaries to TOML format.

Functions:
    get_config_dir: Get the platform-specific config directory path.
    update_config: Write configuration data to the TOML file.
    load_config: Load configuration from the TOML file with caching.
    get_parameters: Get download parameters from configuration.
    set_parameters: Set download parameters in configuration.
    get_path: Get download path from configuration.
    set_path: Set download path in configuration.

Constants:
    ENCODING: Encoding for writing / reading files.
    CONFIG_DIR: The resolved configuration directory path.
    CONFIG_FILE: The full path to the config.toml file.
    PARAM_KEY: Key for accessing parameters in configuration.
    PATH_KEY: Key for accessing path in configuration.

Example:
    >>> from fm_dlp_core.utils.config import load_config, update_config, get_path
    >>> config = load_config(color=True)
    >>> config["path"] = "/downloads"
    >>> update_config(config)
    True
    >>> download_path = get_path(config)
    '/downloads'
"""

from .config_manager import (
    CONFIG_DIR,
    CONFIG_FILE,
    ENCODING,
    TOMLSerializer,
    get_config_dir,
    load_config,
    update_config,
)
from .parametrs import PARAM_KEY, get_parameters, set_parameters
from .path import PATH_KEY, get_path, set_path

__all__ = [
    "CONFIG_DIR",
    "CONFIG_FILE",
    "ENCODING",
    "PARAM_KEY",
    "PATH_KEY",
    "TOMLSerializer",
    "get_config_dir",
    "get_parameters",
    "get_path",
    "load_config",
    "set_parameters",
    "set_path",
    "update_config",
]
