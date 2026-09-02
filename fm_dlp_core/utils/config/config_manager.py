import os
import sys
import tomllib
from functools import lru_cache
from pathlib import Path
from typing import Any

from ...utils import echo, error, set_colors

ENCODING = "utf-8"


def get_config_dir(dir_name: str = "fm-dlp") -> str:
    """
    Get the user configuration directory path based on the operating system.

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


CONFIG_DIR: str = get_config_dir()
CONFIG_FILE: Path = Path(CONFIG_DIR) / "config.toml"


class TOMLSerializer:
    """
    Serializes Python dictionaries to TOML format.

    This class provides methods to convert Python data structures (dict, list,
    str, bool, etc.) into TOML string representation.

    Example:
        >>> serializer = TOMLSerializer()
        >>> data = {"name": "fm-dlp", "enabled": True, "paths": ["/downloads"]}
        >>> toml_str = serializer.dumps(data)
        >>> print(toml_str)
        name = "fm-dlp"
        enabled = true
        paths = ["/downloads"]
    """

    @classmethod
    def dumps(cls, data: dict[str, Any]) -> str:
        """
        Serialize a dictionary to a TOML string.

        Args:
            data: Dictionary to serialize.

        Returns:
            TOML string representation of the dictionary.
        """
        lines: list[str] = []
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"[{key}]")
                for sub_key, sub_value in value.items():
                    lines.append(f"{sub_key} = {cls._value_to_str(sub_value)}")
            else:
                lines.append(f"{key} = {cls._value_to_str(value)}")
            lines.append("")
        return "\n".join(lines)

    @classmethod
    def _value_to_str(cls, value: Any) -> str:
        """
        Convert a Python value to its TOML string representation.

        Args:
            value: The Python value to convert.

        Returns:
            TOML string representation of the value.
        """
        if isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, list):
            items = [cls._value_to_str(item) for item in value]
            return f"[{', '.join(items)}]"
        elif isinstance(value, dict):
            items: list[str] = []
            for k, v in value.items():
                key_str = f'"{k}"' if not isinstance(k, str) else k
                items.append(f"{key_str} = {cls._value_to_str(v)}")
            return f"{{ {', '.join(items)} }}"
        else:
            return str(value)


@lru_cache(maxsize=1)
def load_config(color: bool) -> dict[str, Any]:
    """
    Load configuration from the TOML file with caching for performance.

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


def update_config(data: dict[str, Any]) -> bool:
    """
    Update configuration data to the TOML file, creating directories if needed.

    Args:
        data (dict): Dictionary containing the complete configuration data to write.

    Returns:
        bool: True if the configuration was updated successfully, False if an error occurred.
    """
    try:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        toml_content = TOMLSerializer.dumps(data)
        _ = CONFIG_FILE.write_text(toml_content, ENCODING)
        load_config.cache_clear()
        return True
    except (PermissionError, OSError):
        return False
