from typing import Any

from ..colors import success
from . import CONFIG_FILE, echo, error, load_config, save_config, set_colors, sys

PARAM_KEY = "parameters"


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
        config = load_config(color)

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

        if not save_config(config, encoding):
            raise PermissionError()

        if not quiet:
            echo(success("Parameters have been successfully saved"))
        return True

    except PermissionError:
        if not quiet:
            echo(
                error(f"Permission denied! Cannot write to {CONFIG_FILE}"),
                file=sys.stderr,
            )
        return False
    except OSError as e:
        if not quiet:
            echo(error(f"Error saving configuration: {e}"), file=sys.stderr)
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
