from pathlib import Path
from typing import Any

from ...utils import echo, echo_error, info, set_colors, success
from .params import ConfigParams


def get_config_dir(dir_name: str = "fm-dlp") -> Path:
    """Get the user configuration directory path based on the operating system."""
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

    return d / dir_name


CONFIG_FILE = get_config_dir() / "config.toml"


class ConfigManager:
    """
    Manage application configuration stored in a TOML file.

    Attributes:
        params (ConfigParams): Configuration parameters (quiet, color, config_file).
        config_file (Path): Resolved path to the TOML config file. Falls back
            to the platform-specific default when ``params.config_file`` is
            missing or not a ``.toml`` file.
    """

    def __init__(self, params: ConfigParams):
        self.params = params
        self.encoding = "utf-8"
        if params.config_file is None or not params.config_file.endswith(".toml"):
            if params.config_file is not None:
                self._if_quiet(
                    params.quiet,
                    "The configuration file must be TOML format. Using default.",
                    error_result=True,
                    exit_on_error=False,
                )
            self.config_file = CONFIG_FILE
        else:
            self.config_file = Path(params.config_file).expanduser()
        set_colors(params.color)

    def load_config(self) -> dict[str, Any]:
        """Load and parse the TOML config. Returns {} if missing/corrupted."""
        import tomllib

        if not self.config_file.exists():
            return {}
        try:
            content = self.config_file.read_text(self.encoding)
            return tomllib.loads(content)
        except (tomllib.TOMLDecodeError, OSError):
            self._if_quiet(
                self.params.quiet,
                "Config file is corrupted. Creating new one...",
                error_result=True,
                exit_on_error=False,
            )
            return {}

    def update_config(self, data: dict[str, Any]) -> bool:
        """Write ``data`` to the config file. Returns True on success."""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            toml_content = TOMLSerializer.dumps(data)
            self.config_file.write_text(toml_content, self.encoding)
            return True
        except (PermissionError, OSError):
            return False

    def _if_quiet(
        self,
        quiet: bool,
        text: str,
        error_result: bool | None = None,
        exit_on_error: bool = True,
        success_result: bool | None = None,
        info_result: bool | None = None,
    ) -> None:
        if not quiet:
            if error_result:
                echo_error(text, exit=exit_on_error)
            elif success_result:
                echo(success(text))
            elif info_result:
                echo(info(text))
            else:
                echo(text)


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
    def dumps(cls, data: dict[str, Any]) -> str:
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
    def _value_to_str(cls, value: Any) -> str:
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
