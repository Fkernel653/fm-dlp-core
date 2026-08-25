"""
fm-dlp-core — Core package for YouTube audio/video downloading and searching.

This package provides the foundational functionality for the fm-dlp CLI application,
handling all core operations including search, download, and configuration management.

Core Features:
    - Download from 1000+ platforms using yt-dlp backend
    - Search YouTube Music and YouTube for tracks, albums, and videos
    - Multiple audio codec support (mp3, aac, flac, m4a, opus, vorbis, wav, alac)
    - Video format support (mp4, mov, mkv, webm, avi, flv)
    - Video-only download mode (without audio track)
    - Concurrent downloads with configurable job limits
    - Metadata embedding with thumbnails for audio files
    - Persistent configuration for download preferences
    - Cookie-based authentication for platform-specific downloads
    - Colored terminal output for better user experience

Package Structure:
    commands/
        downloader/   - Async download engine with format conversion
        search/       - YouTube and YouTube Music search providers
    utils/            - Shared utilities (colors, formatting, constants)
        config/       - Configuration management for paths and parameters

Exported Symbols:
    Download, run_downloader   - Async download functionality
    Search, search             - Search capabilities
    ALL_CODECS                 - Complete list of supported codecs/formats
    AUDIO_CODECS               - Audio-only codec formats
    VIDEO_CONTAINERS           - Video container formats
    VIDEO_CONTAINER_AUDIO_MAP  - Video container to audio codec mapping
    echo                       - Terminal output with color support

Requirements:
    - Python 3.11+ with tomllib support
    - ffmpeg for audio/video processing (required for conversion)

For more information, visit: https://github.com/Fkernel653/fm-dlp-core
"""

from .commands.downloader.downloader import Download, run_downloader
from .commands.search import Search, search
from .utils import (
    ALL_CODECS,
    AUDIO_CODECS,
    VIDEO_CONTAINER_AUDIO_MAP,
    VIDEO_CONTAINERS,
    echo,
)

__all__ = [
    "ALL_CODECS",
    "AUDIO_CODECS",
    "VIDEO_CONTAINERS",
    "VIDEO_CONTAINER_AUDIO_MAP",
    "Download",
    "Search",
    "echo",
    "run_downloader",
    "search",
]
