"""
Utility modules for the fm-dlp core package.

This package provides shared utilities used across the application including:
- Color management and styled terminal output with ANSI escape codes
- Codec and container format constants for media processing
- Terminal output helper functions with standardized formatting

The `colors` submodule provides comprehensive color formatting for terminal
output with both predefined styles and a flexible `styled()` function for
custom formatting.
"""

import sys
from typing import TextIO

from .colors import (
    BOLD_CYAN,
    BOLD_GREEN,
    BOLD_RED,
    BOLD_WHITE,
    BOLD_YELLOW,
    GRAY,
    RESET,
    error,
    hint,
    info,
    set_colors,
    styled,
    success,
)

AUDIO_CODECS = ("mp3", "aac", "flac", "m4a", "opus", "vorbis", "wav", "alac")
VIDEO_CONTAINERS = ("mp4", "mov", "mkv", "webm", "avi", "flv")
ALL_CODECS = AUDIO_CODECS + VIDEO_CONTAINERS
VIDEO_CONTAINER_AUDIO_MAP = {
    "mp4": "m4a",
    "mov": "m4a",
    "mkv": "opus",
    "webm": "opus",
    "avi": "mp3",
    "flv": "aac",
}


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
    file.write(text + "\n")


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


__all__ = [
    "ALL_CODECS",
    "AUDIO_CODECS",
    "BOLD_CYAN",
    "BOLD_GREEN",
    "BOLD_RED",
    "BOLD_WHITE",
    "BOLD_YELLOW",
    "GRAY",
    "RESET",
    "VIDEO_CONTAINERS",
    "VIDEO_CONTAINER_AUDIO_MAP",
    "echo",
    "echo_error",
    "error",
    "hint",
    "info",
    "set_colors",
    "styled",
    "success",
]
