"""
Terminal output and validation utilities.

This module provides functions for printing styled messages to stdout/stderr,
validating remote source identifiers, and lazily loading the yt-dlp library.
"""

import sys
from typing import TextIO

from .colors import error
from .constants import VALID_REMOTE_SOURCES

_YoutubeDL = None
"""Global cache for the yt-dlp YoutubeDL class to enable lazy loading."""


def echo(text: str, file: TextIO = sys.stdout) -> None:
    """
    Print a message to the specified output stream with a newline.

    This is a convenience wrapper around file.write() that ensures
    consistent newline handling across the application.

    Args:
        text: The message to print.
        file: The output stream to write to. Defaults to stdout.

    Example:
        >>> echo("Processing complete")
        Processing complete
        >>> import sys
        >>> echo("Error message", file=sys.stderr)
        Error message
    """
    _ = file.write(text + "\n")


def echo_error(text: str) -> None:
    """
    Print an error message to stderr and terminate the program.

    The error message is formatted with the standard error style
    (typically red) and written to stderr. The function then calls
    sys.exit(1) to halt execution with a non-zero exit code.

    Args:
        text: The error message to display.

    Example:
        >>> echo_error("File not found")
        [ERROR] File not found  # formatted in red
        # Program exits with code 1
    """
    echo(error(text), file=sys.stderr)
    sys.exit(1)


def validate_remote(remote: str | None) -> None:
    """
    Validate a remote source identifier against the allowed sources.

    If the provided remote identifier is not in VALID_REMOTE_SOURCES,
    this function prints an error message and terminates the program.

    Args:
        remote: The remote source identifier to validate (e.g., "ejs:github",
               "ejs:npm", or None).

    Raises:
        SystemExit: If the remote identifier is invalid, via echo_error().

    Example:
        >>> validate_remote("ejs:github")  # Valid, no output
        >>> validate_remote("ejs:gitlab")  # Invalid, exits with error
        [ERROR] Invalid remote value: 'ejs:gitlab'.
        Must be one of: ejs:github, ejs:npm, None
    """
    if remote not in VALID_REMOTE_SOURCES:
        echo_error(
            f"Invalid remote value: '{remote}'.\nMust be one of: {', '.join(str(v) for v in VALID_REMOTE_SOURCES)}"
        )


def get_ytdlp():
    """
    Lazily import and return the yt-dlp YoutubeDL class.

    This function ensures that the yt-dlp library is only imported when
    first needed, which reduces startup time and avoids dependency issues
    for code paths that don't require video downloading.

    The imported class is cached globally after the first call, so subsequent
    calls return immediately without re-importing.

    Returns:
        type: The yt-dlp YoutubeDL class object.

    Example:
        >>> YoutubeDL = get_ytdlp()
        >>> ydl = YoutubeDL()  # Create an instance for downloading
        >>> ydl.extract_info("https://youtube.com/watch?v=...", download=False)
    """
    global _YoutubeDL

    if _YoutubeDL is None:
        from yt_dlp import YoutubeDL

        _YoutubeDL = YoutubeDL
    return _YoutubeDL
