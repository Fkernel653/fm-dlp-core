from pathlib import Path

from ...utils import echo_error, set_colors


def get_config_dir(dir_name: str = "fm-dlp") -> str:
    """
    Get the user configuration directory path based on the operating system.

    Args:
        dir_name (str, optional): Name of the application directory to create
                                  under the config root. Defaults to "fm-dlp".

    Returns:
        str: The absolute path to the configuration directory.
    """
    import os
    import sys

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


CONFIG_FILE = Path(get_config_dir()) / "config.toml"


class ConfigManager:
    """
    Manage application configuration stored in a TOML file.

    This class is responsible for loading and updating the configuration
    file located in the platform-specific user configuration directory.

    Attributes:
        color (bool): Whether colored output is enabled for messages.

    Example:
        >>> manager = ConfigManager(color=True)
        >>> config = manager.load_config()
        >>> config["path"] = "/downloads"
        >>> manager.update_config(config)
        True
    """

    def __init__(self, color: bool = True):
        self.color = color
        self.encoding = "utf-8"
        set_colors(color)

    def load_config(self) -> dict[str, str | int | bool | None]:
        """
        Load configuration from the TOML file.

        Args:
            color (bool): Enable colored output for error messages when the config
                          file is corrupted.

        Returns:
            dict: Parsed configuration dictionary, or empty dict if the file doesn't
                  exist or is corrupted.
        """
        import tomllib

        if not CONFIG_FILE.exists():
            return {}
        try:
            content = CONFIG_FILE.read_text(self.encoding)
            return tomllib.loads(content)
        except (tomllib.TOMLDecodeError, OSError):
            echo_error("Config file is corrupted. Creating new one...", exit=False)
            return {}

    def update_config(self, data: dict[str, str | int | bool | None]) -> bool:
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
            CONFIG_FILE.write_text(toml_content, self.encoding)
            return True
        except (PermissionError, OSError):
            return False


class TOMLSerializer:
    """
    Serializes Python dictionaries to TOML format.

    This class provides methods to convert Python data structures (str and dict) into TOML string representation.

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
    def dumps(cls, data: dict[str, str | int | bool | None]) -> str:
        """
        Serialize a dictionary to a TOML string.

        Args:
            data: Dictionary to serialize.

        Returns:
            TOML string representation of the dictionary.
        """
        lines = []
        for k, v in data.items():
            if isinstance(v, dict):
                lines.append(f"[{k}]")
                for sub_key, sub_value in v.items():
                    lines.append(f"{sub_key} = {cls._value_to_str(sub_value)}")
            else:
                lines.append(f"{k} = {cls._value_to_str(v)}")
            lines.append("")
        return "\n".join(lines)

    @classmethod
    def _value_to_str(cls, value: str | int | bool | dict | None) -> str:
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
        elif isinstance(value, dict):
            items = []
            for k, v in value.items():
                key_str = f'"{k}"' if not isinstance(k, str) else k
                items.append(f"{key_str} = {cls._value_to_str(v)}")
            return f"{{ {', '.join(items)} }}"
        return str(value)
