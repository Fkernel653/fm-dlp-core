import json
import os
import sys
from functools import lru_cache
from pathlib import Path

from ...utils import echo
from ..colors import error, set_colors


def get_config_dir(dir_name: str = "fm-dlp") -> str:
    """Get the user config directory based on platform."""
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
    """Update configuration data to JSON file.

    Args:
        data: Dictionary containing configuration data to update.
        encoding: File encoding (default: utf-8).

    Returns:
        True if configuration was updated successfully, False otherwise.
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
    """Load configuration from JSON file with caching.

    Args:
        color: Colored output for error messages.
        encoding: File Encoding.

    Returns:
        Dictionary containing configuration data. Empty dict if file doesn't exist.
    """
    if not CONFIG_FILE.exists():
        return {}
    try:
        return json.loads(CONFIG_FILE.read_text(encoding))
    except (json.JSONDecodeError, OSError):
        set_colors(color)
        echo(error("Config file is corrupted. Creating new one..."), file=sys.stderr)
        return {}
