"""
Constants for audio and video format handling.

This module defines supported codecs, container formats, and mappings
used throughout the application for media processing and validation.
"""

AUDIO_CODECS = ("mp3", "aac", "flac", "m4a", "opus", "vorbis", "wav", "alac")
"""Tuple of supported audio codec formats."""

VIDEO_CONTAINERS = ("mp4", "mov", "mkv", "webm", "avi", "flv")
"""Tuple of supported video container formats."""

ALL_CODECS = AUDIO_CODECS + VIDEO_CONTAINERS
"""Union of all supported audio codecs and video containers."""

VIDEO_CONTAINER_AUDIO_MAP: dict[str, str] = {
    "mp4": "m4a",
    "mov": "m4a",
    "mkv": "opus",
    "webm": "opus",
    "avi": "mp3",
    "flv": "aac",
}
"""
Mapping from video container formats to their default audio extraction codec.

When extracting audio from a video file, this map determines which audio
codec to use as the default output format for each container type.
"""

VALID_REMOTE_SOURCES = ("ejs:github", "ejs:npm", None)
"""
Tuple of valid remote source identifiers for template or package fetching.

Valid values:
    - "ejs:github": Fetch from GitHub repository
    - "ejs:npm": Fetch from npm registry
    - None: No remote source (local only)
"""
