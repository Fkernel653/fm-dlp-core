from typing import Any

from ...utils import echo, echo_error, validate_remote
from ..colors import set_colors, success
from .config_manager import CONFIG_FILE, load_config, update_config

PARAM_KEY: str = "parameters"


def _if_quiet(
    quiet: bool,
    text: str,
    error_result: bool | None = None,
    success_result: bool | None = None,
) -> None:
    if not quiet:
        if error_result:
            echo_error(text)
        elif success_result:
            echo(success(text))
        else:
            echo(text)


def set_parameters(
    codec: str,
    kbps: int,
    quality: str,
    jobs: int,
    quiet: bool,
    metadata: bool,
    keep: bool,
    only_video: bool,
    cookies: str | None,
    remote: str | None,
    color: bool = True,
) -> bool:
    """
    Save download parameters to configuration file without overwriting other settings.

    This function updates only the `parameters` section of the config, preserving
    any other settings (such as the download path) that may already exist in the
    configuration file. Parameters are saved under the `PARAM_KEY` ("parameters")
    key in the TOML config structure.

    Args:
        codec (str): Audio codec (e.g., "mp3", "m4a", "flac") or video container
                     (e.g., "mp4", "mkv", "webm").
        kbps (int): Audio bitrate in kbps (e.g., 128, 192, 320).
        quality (str): Video quality preset ("best", "worst", "1080p", "720p",
                              "480p", "360p", "2160p").
        jobs (int): Maximum number of concurrent downloads to run in parallel.
        quiet (bool): Suppress yt-dlp output and verbose logging.
        metadata (bool): Embed metadata tags and thumbnail into the output file.
        keep (bool): Keep the original downloaded file after conversion.
        only_video (bool): Download video stream only (no audio).
        cookies (str | None): Path to cookies file or browser name for authentication.
        remote (str | None): External JavaScript components source for bypassing anti-bot protections.
                                 Valid values: "ejs:github", "ejs:npm", or ""/None to disable.
                                 Saved to config and auto-applied to future downloads.
        color (bool): Enable colored output in success/error messages. (default: True)

    Returns:
        bool: True if parameters were saved successfully, False if an error occurred
              (permission denied, I/O error, or corrupted config).
    """
    set_colors(color)

    try:
        config = load_config(color)

        params = {
            "codec": codec,
            "kbps": kbps,
            "quality": quality,
            "jobs": jobs,
            "quiet": quiet,
            "metadata": metadata,
            "keep": keep,
            "only_video": only_video,
        }

        if cookies:
            params["cookies"] = cookies

        if remote:
            _ = validate_remote(remote)
            params["remote"] = remote

        config[PARAM_KEY] = params

        if not update_config(config):
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


def get_parameters(color: bool = True) -> dict[str, Any]:
    """
    Retrieve saved download parameters from the configuration file.

    Loads the parameters section from the config TOML file. If the config file
    doesn't exist or the parameters key is missing, returns an empty dictionary.
    This allows callers to safely merge saved parameters with current settings.

    Parameters are retrieved under the `PARAM_KEY` ("parameters") key and may
    include: codec, kbps, quality, jobs, quiet, metadata, keep, only_video,
    and cookies.

    Args:
        color (bool): Enable colored output for error messages. (default: True)

    Returns:
        dict[str, Any]: Dictionary containing saved parameters, or empty dict
                        if no configuration exists or no parameters are saved.
    """
    set_colors(color)

    if not CONFIG_FILE.exists():
        return {}

    config = load_config(color)
    return config.get(PARAM_KEY, {})
