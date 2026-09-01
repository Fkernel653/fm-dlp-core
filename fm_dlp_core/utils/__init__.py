"""
Utility modules for the fm-dlp core package.

This package provides shared utilities used across the application including:
- Color management and styled terminal output with ANSI escape codes
- Codec and container format constants for media processing
- Terminal output helper functions with standardized formatting
- Lazy-loaded yt-dlp integration

The `colors` submodule provides comprehensive color formatting for terminal
output with both predefined styles and a flexible `styled()` function for
custom formatting.
"""

from .colors import (
    BOLD_CYAN,
    BOLD_GREEN,
    BOLD_RED,
    BOLD_WHITE,
    BOLD_YELLOW,
    GRAY,
    RESET,
    WHITE,
    error,
    hint,
    info,
    set_colors,
    styled,
    success,
)
from .constants import (
    ALL_CODECS,
    AUDIO_CODECS,
    VALID_REMOTE_SOURCES,
    VIDEO_CONTAINER_AUDIO_MAP,
    VIDEO_CONTAINERS,
)
from .output import echo, echo_error, get_ytdlp, validate_remote

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
    "VALID_REMOTE_SOURCES",
    "VIDEO_CONTAINERS",
    "VIDEO_CONTAINER_AUDIO_MAP",
    "WHITE",
    "echo",
    "echo_error",
    "error",
    "get_ytdlp",
    "hint",
    "info",
    "set_colors",
    "styled",
    "success",
    "validate_remote",
]
