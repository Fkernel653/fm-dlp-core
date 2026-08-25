"""
Utility modules for the fm-dlp core package.

This package provides shared utilities used across the application including:
- Color management and styled terminal output
- Codec and container format constants
- Terminal output helper functions

Constants:
    AUDIO_CODECS: Set of supported audio codec formats (mp3, aac, flac, etc.)
    VIDEO_CONTAINERS: Set of supported video container formats (mp4, mkv, etc.)
    ALL_CODECS: Union of AUDIO_CODECS and VIDEO_CONTAINERS
    VIDEO_CONTAINER_AUDIO_MAP: Mapping of video containers to their default
                               audio codec for extraction

Functions:
    echo: Print a message to stdout or stderr with newline.
    echo_error: Print an error message to stderr with newline.

The colors submodule provides comprehensive color formatting for terminal output.
"""

import sys
from typing import TextIO

from .colors import error

AUDIO_CODECS: set[str] = {"mp3", "aac", "flac", "m4a", "opus", "vorbis", "wav", "alac"}
VIDEO_CONTAINERS: set[str] = {"mp4", "mov", "mkv", "webm", "avi", "flv"}
ALL_CODECS: set[str] = AUDIO_CODECS | VIDEO_CONTAINERS
VIDEO_CONTAINER_AUDIO_MAP: dict[str, str] = {
    "mp4": "m4a",
    "mov": "m4a",
    "mkv": "opus",
    "webm": "opus",
    "avi": "mp3",
    "flv": "aac",
}


def echo(text: str, file: TextIO = sys.stdout) -> None:
    """Print message to file.

    Args:
        text: Message to print.
        file: File to write to (default: stdout).
    """
    _ = file.write(text + "\n")


def echo_error(text: str) -> None:
    """Print error message to file.

    Args:
        text: Message to print.
    """
    echo(error(text), file=sys.stderr)
    sys.exit(1)
