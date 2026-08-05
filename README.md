# fm-dlp-core — Main core by fm-dlp

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=fff&style=for-the-badge)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/fm-dlp-core?style=for-the-badge&logo=pypi&logoColor=fff&label=PyPI&color=007ec6)](https://pypi.org/project/fm-dlp-core)
[![License](https://img.shields.io/badge/License-GPLv3-00b96b?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-9cf?style=for-the-badge)]()
[![Ruff](https://img.shields.io/badge/Code%20Style-Ruff-ff69b4?logo=ruff&logoColor=fff&style=for-the-badge)](https://docs.astral.sh/ruff)

Core containing utilities for searching from Youtube/YTMusic and downloading audio/video from [1000+ sites](https://github.com/yt-dlp/yt-dlp/supportedsites.md)

---

## 📑 Table of Contents
- [🚀 Quick Start](#-quick-start)
- [⚙️ Requirements](#️-requirements)
- [📚 API Reference](#-api-reference)
  - [🎵 Downloader](#-downloader)
  - [🔍 Search](#-search)
  - [⚙️ Configuration](#️-configuration)
  - [🖥️ Output Formatting](#️-output-formatting)
  - [📦 Internal Modules](#-internal-modules)
    - [Providers](#providers)
    - [Formatters](#formatters)
    - [Config](#config)
    - [Options Builder](#options-builder)
    - [URL Parser](#url-parser)
- [💡 Examples](#-examples)
- [📊 Search Output Examples](#-search-output-examples)
- [📄 License & Acknowledgments](#-license--acknowledgments)

---

## 🚀 Quick Start
```bash
pip install fm-dlp-core                    # Python 3.10+ & FFmpeg required
```

---

## ⚙️ Requirements
- **Python 3.10+** - Asyncio support required
- **FFmpeg** - Required for audio/video processing. Install via:
  - **macOS:** `brew install ffmpeg`
  - **Linux:** `sudo apt install ffmpeg` (Debian) or `sudo dnf install ffmpeg` (Fedora)
  - **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

---

## 📚 API Reference

### 🎵 Downloader

```python
import asyncio
from fm_dlp_core.commands.downloader import Download, run_downloader

# Convenience function
async def main():
    await run_downloader(
        url="https://www.youtube.com/watch?v=example",
        codec="mp3",
        kbps=192,
        quality="best",
        jobs=4,
        quiet=False,
        metadata=True,
        keep=False,
        save=False,
        use_config=False,
        path="./downloads",
        only_video=False,
        cookies=None,
        color=True,
    )

# Context manager (advanced)
async with Download(
    url="https://www.youtube.com/watch?v=example",
    codec="mp3",
    kbps=320,
    quality="1080p",
    jobs=2,
    quiet=True,
    metadata=True,
    keep=True,
    path="./downloads",
    only_video=False,
    cookies="chrome",
    color=True,
) as downloader:
    await downloader.download_all()
```

#### Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | `str` | URL(s) to download (comma/space separated or path to file) |
| `codec` | `str` | Audio codec or video container (`mp3`, `aac`, `flac`, `mp4`, `mkv`) |
| `kbps` | `int` | Audio bitrate in kbps (128, 192, 320) |
| `quality` | `str` | Video quality (`best`, `worst`, `1080p`, `720p`) |
| `jobs` | `int` | Maximum concurrent downloads |
| `quiet` | `bool` | Suppress output messages |
| `metadata` | `bool` | Embed metadata and thumbnail |
| `keep` | `bool` | Keep original file after conversion |
| `save` | `bool` | Save parameters to config file |
| `use_config` | `bool` | Load parameters from config file |
| `path` | `str` | Download directory path |
| `only_video` | `bool` | Download video only (no audio extraction) |
| `cookies` | `str\|None` | Path to cookies file or browser name |
| `color` | `bool` | Enable colored output |
| `encoding` | `str` | File encoding (default: utf-8) |

---

### 🔍 Search

```python
from fm_dlp_core.commands.search import search

# Search YouTube Music for tracks
for result in search(query="Sewerslvt", limit=5, yt_video=False):
    print(result)

# Search YouTube videos
for result in search(query="Python tutorial", limit=3, yt_video=True):
    print(result)

# Get only URLs
urls = list(search(query="breakcore", limit=10, only_url=True))

# Raw data
for data in search(query="Goreshit", limit=2, raw=True):
    print(data)  # dict
```

#### Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | Search query string |
| `limit` | `int` | Maximum number of results |
| `yt_video` | `bool` | Search YouTube videos (False = YouTube Music) |
| `album` | `bool` | Search for albums (False = tracks) |
| `raw` | `bool` | Output raw Python dicts |
| `only_url` | `bool` | Output only URLs |
| `color` | `bool` | Enable colored output |

---

### ⚙️ Configuration

```python
from fm_dlp_core.utils.config.parametrs import set_parameters, get_parameters
from fm_dlp_core.utils.config.path import set_path, get_path
from fm_dlp_core.utils.config import load_config, update_config

# Save parameters
set_parameters(codec="mp3", kbps=256, quality="720p", jobs=4)

# Load parameters
params = get_parameters(color=True, encoding="utf-8")

# Set download path
set_path("./my_downloads", color=True, encoding="utf-8")

# Load full config
config = load_config(color=True, encoding="utf-8")
```

#### Configuration File Location
| Platform | Location |
|----------|----------|
| **Windows** | `%LOCALAPPDATA%\fm-dlp\config.json` |
| **macOS** | `~/Library/Application Support/fm-dlp/config.json` |
| **Linux** | `~/.config/fm-dlp/config.json` |

---

### 🖥️ Output Formatting

```python
from fm_dlp_core.utils import echo
from fm_dlp_core.utils.colors import success, error, info, hint, set_colors, styled, BOLD_CYAN

# Enable/disable colors
set_colors(True)

# Formatted messages
echo(success("Download completed!"))
echo(error("Failed to download"))
echo(info("Processing file..."))
echo(hint("Use --help for more options"))

# Custom styled text
echo(styled("Custom message", BOLD_CYAN))
```

---

### 📦 Internal Modules

#### Providers

Abstract base class for search providers with implementations for YouTube and YouTube Music.

##### BaseProvider (Abstract Base Class)

`BaseProvider` is an abstract base class that defines the interface for creating custom search providers. To implement your own provider, subclass `BaseProvider` and override the abstract methods.

```python
from abc import ABC, abstractmethod
from fm_dlp_core.commands.search.providers import BaseProvider
from fm_dlp_core.commands.search.formatters import ResultFormatter

class MyCustomProvider(BaseProvider):
    """Custom search provider for your favorite platform."""
    
    def _extract_results(self, query: str, limit: int, is_track: bool) -> list:
        """Extract search results from your platform."""
        # Implement your search logic here
        # Return a list of entries (dicts)
        return results
    
    def _extract_url(self, entry: dict, is_track: bool) -> str | None:
        """Extract URL from a search entry."""
        # Return the URL for this entry
        return entry.get("url")
    
    def _fmt_entry(self, entry: dict, num: int, is_track: bool) -> str | None:
        """Format a single search entry."""
        # Use self.formatter to format the entry
        return self.formatter.fmt_result(
            num=num,
            title=entry.get("title", "Unknown"),
            artist=entry.get("artist", "Unknown"),
            url=self._extract_url(entry, is_track),
            is_yt_video=False,  # Set to True for video platforms
            is_track=is_track,
            # Add additional metadata as kwargs
        )
    
    def _get_empty_message(self, query: str, is_track: bool) -> str:
        """Get message when no results found."""
        return f"No results found for '{query}'\n"
```

**BaseProvider Methods:**

| Method | Description | Must Override |
|--------|-------------|---------------|
| `__init__(color, error_prefix, formatter=None)` | Initialize with color settings | ❌ |
| `search(query, limit, is_track, raw, only_url) -> Generator[str]` | Generic search with common logic | ❌ (already implemented) |
| `_extract_results(query, limit, is_track) -> list` | Extract search results from provider | ✅ |
| `_extract_url(entry, is_track) -> str \| None` | Extract URL from search entry | ✅ |
| `_fmt_entry(entry, num, is_track) -> str \| None` | Format a single search entry | ✅ |
| `_get_empty_message(query, is_track) -> str` | Get message when no results found | ✅ |

**Using Your Custom Provider:**

```python
# Create an instance of your custom provider
provider = MyCustomProvider(color=True, error_prefix="Error: ")

# Search using the provider
for result in provider.search(
    query="my search query",
    limit=10,
    is_track=True,       # True for tracks, False for albums/playlists
    raw=False,           # Return formatted output
    only_url=False,      # Return full details
):
    print(result)

# Get only URLs
urls = list(provider.search(query="query", limit=5, only_url=True))
```

##### Built-in Providers

| Class | Description |
|-------|-------------|
| `YouTubeProvider` | Search YouTube videos and playlists using yt-dlp |
| `YouTubeMusicProvider` | Search YouTube Music tracks and albums using ytmusicapi |

```python
from fm_dlp_core.commands.search.providers import YouTubeProvider, YouTubeMusicProvider

# YouTube search
yt = YouTubeProvider(color=True, error_prefix="Error: ")
for result in yt.search(query="test", limit=5, is_track=True, raw=False, only_url=False):
    print(result)

# YouTube Music search
ytm = YouTubeMusicProvider(color=True, error_prefix="Error: ")
for result in ytm.search(query="test", limit=5, is_track=True, raw=False, only_url=False):
    print(result)
```

---

#### Formatters

Format search results with colors and metadata.

```python
from fm_dlp_core.commands.search.formatters import ResultFormatter

formatter = ResultFormatter(color=True, error_prefix="Error: ")

# Format metadata
views = formatter.fmt_views(1234567)       # "1,234,567"
duration = formatter.fmt_duration(125)     # "2:05"
artist = formatter.extract_artist(item)    # Extract artist from YT Music response

# Format result entry
output = formatter.fmt_result(
    num=1,
    title="Song Title",
    artist="Artist Name",
    url="https://...",
    is_yt_video=False,
    is_track=True,
    album="Album Name",
    views="1,234",
    duration="3:45"
)
```

**Methods:**
| Method | Description |
|--------|-------------|
| `fmt_views(v)` | Format view count with commas |
| `fmt_duration(d)` | Convert seconds to MM:SS or HH:MM:SS |
| `extract_artist(item)` | Extract artist from YT Music response |
| `fmt_result(...)` | Format a search result with metadata |
| `fmt_error(error)` | Format error message |

---

#### Config

Configuration container for download settings.

```python
from fm_dlp_core.commands.downloader.config import DownloadConfig

config = DownloadConfig(
    url="https://...",
    codec="mp3",
    kbps=192,
    quality="best",
    jobs=4,
    quiet=False,
    metadata=True,
    keep=False,
    save=False,
    use_config=False,
    path="./downloads",
    only_video=False,
    cookies=None,
    color=True,
    encoding="utf-8"
)

# Apply config (load from file if use_config=True)
params = config.apply_config()

# Save config (if save=True)
config.save_config()
```

**Attributes:**
| Attribute | Type | Description |
|-----------|------|-------------|
| `url` | `str` | URL(s) to download |
| `codec` | `str` | Audio/video codec |
| `kbps` | `int` | Audio bitrate |
| `quality` | `str` | Video quality |
| `jobs` | `int` | Concurrent downloads |
| `quiet` | `bool` | Suppress output |
| `metadata` | `bool` | Embed metadata |
| `keep` | `bool` | Keep original file |
| `save` | `bool` | Save to config |
| `use_config` | `bool` | Load from config |
| `path` | `str` | Download directory |
| `only_video` | `bool` | Video-only mode |
| `cookies` | `str\|None` | Cookies source |
| `color` | `bool` | Colored output |
| `encoding` | `str` | File encoding |

**Methods:**
- `apply_config() -> dict` - Apply saved config if requested
- `save_config() -> bool` - Save current settings to config file

---

#### Options Builder

Build yt-dlp options dictionary for downloads.

```python
from fm_dlp_core.commands.downloader.options_builder import OptionsBuilder

builder = OptionsBuilder(
    codec="mp3",
    kbps=192,
    quality="best",
    jobs=4,
    quiet=False,
    metadata=True,
    keep=False,
    only_video=False,
    cookies=None,
    path="./downloads",
    color=True,
)

opts = builder.build()  # Returns yt-dlp options dict
```

**Methods:**
| Method | Description |
|--------|-------------|
| `build() -> dict` | Build complete yt-dlp options dictionary |
| `_parse_quality() -> str` | Parse quality string to yt-dlp filter |
| `_add_cookies(opts)` | Add cookie configuration |
| `_build_video_opts(opts)` | Build video-only options |
| `_build_audio_opts(opts)` | Build audio options |
| `_build_audio_only_opts(opts)` | Build audio-only options |
| `_build_video_with_audio_opts(opts)` | Build video+audio options |

---

#### URL Parser

Parse URLs from string or file path.

```python
from fm_dlp_core.commands.downloader.url_parser import URLParser

# Parse from string
parser = URLParser("url1,url2,url3", quiet=False)
urls = parser.parse()  # ['url1', 'url2', 'url3']

# Parse from file (one URL per line)
parser = URLParser("urls.txt", quiet=False)
urls = parser.parse()

# Parse with spaces
parser = URLParser("url1 url2 url3", quiet=False)
urls = parser.parse()
```

**Methods:**
| Method | Description |
|--------|-------------|
| `parse() -> list[str]` | Parse URLs from string or file path |
| `_parse_url_file(file_path) -> list[str]` | Read URLs from text file |

---

### 📋 Supported Codecs

#### Audio Codecs
`mp3`, `aac`, `flac`, `m4a`, `opus`, `vorbis`, `wav`, `alac`

#### Video Containers
`mp4`, `mov`, `mkv`, `webm`, `avi`, `flv`

```python
from fm_dlp_core.utils import ALL_CODECS, AUDIO_CODECS, VIDEO_CONTAINERS
```

---

## 💡 Examples

### Basic Download

Example of downloading a track from YouTube Music:

```python
import asyncio
from fm_dlp_core.commands.downloader import Download

async def main():
    async with Download(
        url="https://music.youtube.com/watch?v=0KNxOBerr_8",
        codec="opus",
        kbps=256,
        quality="best",
        jobs=1,
        quiet=False,
        metadata=True,
        keep=False,
        save=False,
        use_config=False,
        path="./Music",
        only_video=False,
        cookies=None,
        color=True,
    ) as downloader:
        await downloader.download_all()

asyncio.run(main())
```

<details>
<summary>📦 Result of execution</summary>

```text
Starting: https://music.youtube.com/watch?v=0KNxOBerr_8

[youtube] Extracting URL: https://music.youtube.com/watch?v=0KNxOBerr_8
[youtube] 0KNxOBerr_8: Downloading webpage
[youtube] 0KNxOBerr_8: Downloading android vr player API JSON
[info] 0KNxOBerr_8: Downloading 1 format(s): 251
[info] Downloading video thumbnail 41 ...
[info] Writing video thumbnail 41 to: /home/user/Music/Lexapro Delirium.webp
[download] Destination: /home/user/Music/Lexapro Delirium.webm
[download] 100% of    6.53MiB in 00:00:01 at 5.74MiB/s
[ExtractAudio] Destination: /home/user/Music/Lexapro Delirium.opus
Deleting original file /home/user/Music/Lexapro Delirium.webm (pass -k to keep)
[Metadata] Adding metadata to "/home/user/Music/Lexapro Delirium.opus"
[ThumbnailsConvertor] Converting thumbnail "/home/user/Music/Lexapro Delirium.webp" to png
[EmbedThumbnail] mutagen: Adding thumbnail to "/home/user/Music/Lexapro Delirium.opus"

Success: https://music.youtube.com/watch?v=0KNxOBerr_8
```

</details>

---

### Download YouTube Video as MP4

```python
import asyncio
from fm_dlp_core.commands.downloader import run_downloader

asyncio.run(run_downloader(
    url="https://www.youtube.com/watch?v=video_id",
    codec="mp4",
    quality="1080p",
    path="./videos",
    only_video=True,
))
```

### Batch Download Audio

```python
async with Download(
    url="id1,id2,id3",  # comma-separated
    codec="flac",
    kbps=0,  # Lossless
    jobs=3,
    metadata=True,
    path="./music",
) as downloader:
    await downloader.download_all()
```

### Search and Download Automation

```python
urls = list(search(query="chill beats", limit=5, only_url=True))
if urls:
    async with Download(url=" ".join(urls), codec="mp3", kbps=320) as downloader:
        await downloader.download_all()
```

### Create Custom Search Provider

```python
from fm_dlp_core.commands.search.providers import BaseProvider

class SoundCloudProvider(BaseProvider):
    def _extract_results(self, query: str, limit: int, is_track: bool) -> list:
        # Implement SoundCloud API search
        # ...
        return results
    
    def _extract_url(self, entry: dict, is_track: bool) -> str | None:
        return f"https://soundcloud.com/{entry.get('permalink_url')}"
    
    def _fmt_entry(self, entry: dict, num: int, is_track: bool) -> str | None:
        return self.formatter.fmt_result(
            num=num,
            title=entry.get("title", "Unknown"),
            artist=entry.get("user", {}).get("username", "Unknown"),
            url=self._extract_url(entry, is_track),
            is_yt_video=False,
            is_track=is_track,
        )
    
    def _get_empty_message(self, query: str, is_track: bool) -> str:
        return f"No tracks found for '{query}'\n"

# Use your custom provider
provider = SoundCloudProvider(color=True, error_prefix="Error: ")
for result in provider.search(query="lo-fi", limit=5, is_track=True):
    print(result)
```

---

## 📊 Search Output Examples

Examples of formatting search results from different sources.

### 🎵 YTMusic (Track)

    1. Mr. Kill Myself
        ├─ Sewerslvt
        ├─ Draining Love Story
        ├─ 13M │ 7:52
        └─ https://music.youtube.com/watch?v=y55fzyXZDSE
           ──────────────────────────────────────────────────

    N. Title
        ├─ Artist
        ├─ Album
        ├─ Views │ Duration
        └─ URL
           ──────────────────────────────────────────────────

### 💿 YTMusic (Album)

    1. Draining Love Story
        ├─ Sewerslvt
        ├─ 2020
        └─ https://music.youtube.com/playlist?list=OLAK5uy_lwWVcID2Sw8o6Jfa9vz8-a2hqEFffKb-g
          ──────────────────────────────────────────────────
          
    N. Title
        ├─ Artist
        ├─ Year
        └─ URL
           ──────────────────────────────────────────────────

### ▶️ YouTube (Video)

    1. Sewerslvt - goodbye
        ├─ Sewerslvt
        ├─ 2,405,647 │ 17:01
        └─ https://youtu.be/ABBpsy6rlVU
           ──────────────────────────────────────────────────

    N. Title
        ├─ Artist
        ├─ Views │ Duration
        └─ URL
           ──────────────────────────────────────────────────

---

### 🧩 Formatting Legend

| Element | Description |
|---------|-------------|
| **N.** | Sequential number of search result |
| **Title** | Track, album, or video title |
| **Artist** | Artist or channel name |
| `├─└─│` | Tree branch characters |
| **Views │ Duration** | View count and length (MM:SS or HH:MM:SS) |
| **URL** | Direct link to content |
| `───` | Visual separator line |

> **Note:** All formatting is handled automatically by the `ResultFormatter` class. Colors can be enabled/disabled via the `color` parameter in search and download functions.

---

## 📄 License & Acknowledgments

GPLv3 License — Built with:

| Library | Purpose |
|---------|---------|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Download engine supporting 1000+ sites |
| [ytmusicapi](https://github.com/sigma67/ytmusicapi) | YouTube Music search API |
| [mutagen](https://github.com/quodlibet/mutagen) | Metadata tagging for audio files |

**Author:** [Fkernel653](https://github.com/Fkernel653)

**Project:** [GitHub](https://github.com/Fkernel653/fm-dlp-core) • [PyPI](https://pypi.org/project/fm-dlp-core)
