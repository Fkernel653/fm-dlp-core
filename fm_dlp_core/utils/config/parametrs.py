from typing import Any

from ..colors import error, set_colors, success
from . import CONFIG_FILE, echo, load_config, sys, update_config

PARAM_KEY = "parameters"


def _if_quiet(
    quiet: bool,
    text: str,
    error_result: bool | None = None,
    success_result: bool | None = None,
) -> None:
    if not quiet:
        if error_result:
            echo(error(text), file=sys.stderr)
        elif success_result:
            echo(success(text))
        else:
            echo(text)


def set_parameters(
    codec: str,
    kbps: int,
    quality: str | None,
    jobs: int,
    quiet: bool,
    metadata: bool,
    keep: bool,
    only_video: bool,
    cookies: str | None,
    color: bool,
    encoding: str = "utf-8",
) -> bool:
    """Save download parameters to config file without overwriting other settings.

    Args:
        codec: Audio codec or video container.
        kbps: Audio bitrate in kbps.
        quality: Video quality preset (best, 1080p, 720p, 480p, 360p, 2160p, worst).
        jobs: Maximum concurrent downloads.
        quiet: Suppress yt-dlp output.
        metadata: Embed metadata and thumbnail.
        keep: Keep the original downloaded file after conversion.
        only_video: Download video only.
        cookies: Path to cookies file or browser name.
        color: Colored output.
        encoding: File Encoding.

    Returns:
        True if parameters saved successfully, False otherwise.
    """
    set_colors(color)

    try:
        config = load_config(color, encoding)

        config[PARAM_KEY] = {
            "codec": codec,
            "kbps": kbps,
            "quality": quality,
            "jobs": jobs,
            "quiet": quiet,
            "metadata": metadata,
            "keep": keep,
            "only_video": only_video,
            "cookies": cookies,
        }

        if not update_config(config, encoding):
            raise PermissionError()

        _if_quiet(quiet, "Parameters have been successfully saved", success_result=True)
        return True

    except PermissionError:
        _if_quiet(
            quiet,
            f"Permission denied! Cannot write to {CONFIG_FILE}",
            error_result=True,
        )
        return False
    except OSError as e:
        _if_quiet(quiet, f"Error saving configuration: {e}", error_result=True)
        return False


def get_parameters(color: bool, encoding: str = "utf-8") -> dict[str, Any]:
    """Retrieve saved parameters from config file.

    Args:
        color: Colored output for error messages.
        encoding: File Encoding.

    Returns:
        Dictionary with saved parameters or empty dict if none exist.
    """
    set_colors(color)

    if not CONFIG_FILE.exists():
        return {}

    config = load_config(color, encoding)
    return config.get(PARAM_KEY, {})
