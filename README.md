# fm-dlp-core — Core Library for YouTube & 1000+ Sites

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=fff&style=for-the-badge)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/fm-dlp-core?style=for-the-badge&logo=pypi&logoColor=fff&label=PyPI&color=007ec6)](https://pypi.org/project/fm-dlp-core)
[![License](https://img.shields.io/badge/License-AGPLv3-00b96b?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-9cf?style=for-the-badge)](<>)
[![Ruff](https://img.shields.io/badge/Code%20Style-Ruff-ff69b4?logo=ruff&logoColor=fff&style=for-the-badge)](https://docs.astral.sh/ruff)

**fm-dlp-core** is a powerful Python library for searching and downloading content from YouTube, YouTube Music, and over 1000+ supported sites. Built on top of yt-dlp, it provides a clean, async-first API with rich features including concurrent downloads, metadata embedding, and flexible output formatting.

---

## ✨ Key Features

| Feature                     | Description                                                                 |
| --------------------------- | --------------------------------------------------------------------------- |
| 🎵 **Audio Extraction**     | Extract audio in 8 formats: MP3, AAC, FLAC, M4A, Opus, Vorbis, WAV, ALAC    |
| 🎬 **Video Download**       | Download videos in MP4, MKV, WebM, MOV, AVI, FLV with quality selection     |
| 🔍 **Search**               | Search YouTube videos and YouTube Music tracks/albums with formatted output |
| ⚡ **Concurrent Downloads** | Download multiple files in parallel with configurable job limits            |
| 🏷️ **Metadata Embedding**   | Automatically embed tags and thumbnails into audio files                    |
| 🔐 **Authentication**       | Support for cookies (file or browser) to access restricted content          |
| 💾 **Persistent Config**    | Save and load download preferences across sessions                          |
| 🎨 **Colored Output**       | Beautiful terminal output with ANSI colors (toggleable)                     |
| 🔌 **Extensible**           | Create custom search providers for any platform                             |

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Requirements](#-requirements)
- [Core Concepts](#-core-concepts)
- [Downloading Content](#-downloading-content)
- [Searching Content](#-searching-content)
- [Configuration](#-configuration)
- [Advanced Topics](#-advanced-topics)
- [API Reference](#-api-reference)
- [Examples](#-examples)
- [License](#-license)

---

## 🚀 Quick Start

```python
import asyncio
from fm_dlp_core import search, run_downloader

# 1. Search for a track
for result in search("Sewerslvt", limit=3, yt_video=False, album=False):
    print(result)

# 2. Download a track
asyncio.run(
    run_downloader(
        url="https://music.youtube.com/watch?v=y55fzyXZDSE",
        codec="mp3",
        kbps=320,
        path="./music",
        metadata=True,
        color=True,
    )
)
```

---

## 📦 Installation

```bash
pip install fm-dlp-core
```

For development:

```bash
git clone https://github.com/Fkernel653/fm-dlp-core
cd fm-dlp-core
pip install -e .
```

---

## ⚙️ Requirements

### Python Version

- **Python 3.11+** — Required for tomllib, asyncio and type hint features

### FFmpeg (Required)

FFmpeg is essential for audio/video processing, conversion, and metadata embedding.

| Platform          | Installation Command                                                         |
| ----------------- | ---------------------------------------------------------------------------- |
| **macOS**         | `brew install ffmpeg`                                                        |
| **Debian/Ubuntu** | `sudo apt install ffmpeg`                                                    |
| **Fedora**        | `sudo dnf install ffmpeg`                                                    |
| **Windows**       | Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH |

---

## 🧠 Core Concepts

### Async-First Design

All download operations are asynchronous, allowing you to run multiple downloads concurrently without blocking your application.

### Configuration Persistence

Settings like codec, bitrate, quality, and download path can be saved to a TOML file and reused across sessions.

### Provider Pattern

Search functionality is built on a provider pattern, making it easy to add support for new platforms by subclassing `BaseProvider`.

---

## 🎵 Downloading Content

### Overview

The download system supports:

- **Audio extraction** in 8 formats (MP3, AAC, FLAC, M4A, Opus, Vorbis, WAV, ALAC)
- **Video download** in MP4, MKV, WebM, MOV, AVI, FLV with quality selection
- **Batch downloads** from multiple URLs or text files
- **Concurrent downloads** with configurable job limits
- **Metadata embedding** with thumbnails

### DownloadParams Class

All download parameters are encapsulated in the `DownloadParams` dataclass:

```python
from fm_dlp_core.commands.downloader.params import DownloadParams

params = DownloadParams(
    url="https://youtube.com/watch?v=...",
    codec="mp3",
    kbps=320,
    quality="best",
    jobs=4,
    quiet=False,
    metadata=True,
    keep=False,
    save=False,
    use_config=False,
    path="./downloads",
    only_video=False,
    cookies="chrome",
    remote="ejs:github",
    color=True,
)
```

### Download Parameters Reference

| Parameter    | Type          | Description                                                                                                                                        |
| ------------ | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`        | `str`         | URL(s) to download (comma/space separated or path to file)                                                                                         |
| `codec`      | `str`         | Output format (see Supported Codecs)                                                                                                               |
| `kbps`       | `int`         | Audio bitrate in kbps. Use `0` for lossless formats (FLAC, WAV, ALAC)                                                                              |
| `quality`    | `str`         | Video quality: `"best"`, `"worst"`, `"1080"`, `"1080p"`, or custom format filter                                                                   |
| `jobs`       | `int`         | Number of concurrent downloads (also controls thread/process pool size)                                                                            |
| `quiet`      | `bool`        | Suppress output messages                                                                                                                           |
| `metadata`   | `bool`        | Embed metadata and thumbnail. **Note:** Automatically disabled for WAV format (not supported)                                                      |
| `keep`       | `bool`        | Keep original downloaded file (video file when extracting audio)                                                                                   |
| `save`       | `bool`        | Save parameters to config (requires `color` parameter for config key)                                                                              |
| `use_config` | `bool`        | Load parameters from config. Saved values take priority over instance values. Config key uses the `color` parameter value                          |
| `path`       | `str`         | Download directory                                                                                                                                 |
| `only_video` | `bool`        | Download video only (skip audio extraction). Uses `ProcessPoolExecutor` for video processing                                                       |
| `cookies`    | `str \| None` | Cookies file path or browser name (`"chrome"`, `"firefox"`, `"edge"`, `"opera"`). Uses cookiefile if path exists, otherwise cookiesfrombrowser     |
| `remote`     | `str \| None` | External JavaScript components source for bypassing anti-bot protections. Valid values: `"ejs:github"` (yt-dlp repo) or `"ejs:npm"` (NPM registry) |
| `color`      | `bool`        | Enable colored output. Also used as the configuration key identifier for storing/retrieving settings                                               |

### Supported Codecs

| Type      | Formats                                                      |
| --------- | ------------------------------------------------------------ |
| **Audio** | `mp3`, `aac`, `flac`, `m4a`, `opus`, `vorbis`, `wav`, `alac` |
| **Video** | `mp4`, `mov`, `mkv`, `webm`, `avi`, `flv`                    |

### Executor Selection

The downloader automatically selects the appropriate executor type:

- **ProcessPoolExecutor** — Used for video downloads and container formats (MP4, MKV, etc.) that benefit from CPU parallelism for transcoding
- **ThreadPoolExecutor** — Used for audio downloads (MP3, M4A, etc.) which are typically I/O-bound and work better with threading

This optimization is handled automatically based on the `only_video` flag and `codec` selection.

<details>
<summary><b>📘 Click for examples</b></summary>

**Basic Usage with run_downloader**

```python
import asyncio
from fm_dlp_core import run_downloader

asyncio.run(
    run_downloader(
        url="https://youtube.com/watch?v=VIDEO_ID",
        codec="mp3",
        kbps=192,
        path="./downloads",
    )
)
```

---

**Advanced Usage with Download Class**

```python
from fm_dlp_core import Download
from fm_dlp_core.commands.downloader.params import DownloadParams

async def download_video():
    params = DownloadParams(
        url="https://youtube.com/watch?v=VIDEO_ID",
        codec="mp4",
        quality="1080p",
        jobs=4,
        path="./videos",
        metadata=True,
        only_video=True,
        remote="ejs:github",
        color=True,
    )

    async with Download(params) as downloader:
        await downloader.download_all()
```

---

**Batch Downloads**

```python
from fm_dlp_core import Download
from fm_dlp_core.commands.downloader.params import DownloadParams

# Multiple URLs (comma or space separated)
params = DownloadParams(
    url="url1,url2,url3",  # or "url1 url2 url3"
    codec="flac",
    kbps=0,  # Lossless
    jobs=3,
)

async with Download(params) as downloader:
    await downloader.download_all()

# URLs from a text file (one per line, comma/space separated supported)
params = DownloadParams(
    url="urls.txt",
    codec="m4a",
    kbps=256,
)

async with Download(params) as downloader:
    await downloader.download_all()
```

---

**Manual Configuration Management**

```python
from fm_dlp_core.commands.downloader import DownloadConfig, DownloadParams

params = DownloadParams(
    url="https://youtube.com/watch?v=...",
    codec="mp3",
    kbps=320,
    quality="best",
    jobs=4,
    quiet=False,
    metadata=True,
    keep=False,
    save=True,  # Save to config
    use_config=True,  # Load from config
    path="./downloads",
    only_video=False,
    cookies="chrome",
    remote="ejs:github",
    color=True,
)

# Config will automatically handle save/load based on params
config = DownloadConfig(params)
applied_params = config.apply_config()  # Returns dict with merged params
config.save_config()  # Saves if save=True
```

</details>

---

## 🔍 Searching Content

### Overview

The search system supports:

- **YouTube Music** — Search for tracks and albums
- **YouTube** — Search for videos
- **Formatted output** with colors and structured display
- **Raw data** for programmatic use
- **URL-only** output for easy piping to downloads

### Search Parameters

| Parameter  | Type   | Description                                      |
| ---------- | ------ | ------------------------------------------------ |
| `query`    | `str`  | Search query string                              |
| `limit`    | `int`  | Maximum number of results (1-100)                |
| `yt_video` | `bool` | `True` = YouTube videos, `False` = YouTube Music |
| `album`    | `bool` | `True` = search albums, `False` = search tracks  |
| `raw`      | `bool` | Output raw Python dicts                          |
| `only_url` | `bool` | Output only URLs                                 |
| `color`    | `bool` | Enable colored output                            |

### Output Modes

| Mode          | Parameter                   | Description                            |
| ------------- | --------------------------- | -------------------------------------- |
| **Formatted** | `raw=False, only_url=False` | Beautiful colored output with metadata |
| **URL-Only**  | `only_url=True`             | Just the URLs (great for piping)       |
| **Raw Data**  | `raw=True`                  | Python dictionaries with full metadata |

<details>
<summary><b>📘 Click for examples</b></summary>

**YouTube Music Search (Tracks)**

```python
from fm_dlp_core import search

for result in search(
    query="Sewerslvt",
    limit=5,
    yt_video=False,   # Use YouTube Music
    album=False,      # Search for tracks
    color=True,
):
    print(result)
```

---

**YouTube Music Search (Albums)**

```python
for result in search(
    query="Draining Love Story",
    limit=3,
    yt_video=False,
    album=True,       # Search for albums
):
    print(result)
```

---

**YouTube Video Search**

```python
for result in search(
    query="Python tutorial",
    limit=5,
    yt_video=True,    # Use YouTube (videos)
    album=False,
):
    print(result)
```

---

**URL-Only Output**

```python
# Get only URLs
urls = list(search("breakcore", limit=10, only_url=True))

# Chain search → download
urls = list(search("chill beats", limit=5, only_url=True))
if urls:
    asyncio.run(run_downloader(url=" ".join(urls), codec="mp3", kbps=320))
```

---

**Raw Data Output**

```python
for data in search("Goreshit", limit=2, raw=True):
    print(data["title"], data["url"])
```

</details>

---

## ⚙️ Configuration

### Overview

The configuration system provides:

- **Persistent parameters** — Save download settings across sessions
- **Multiple config profiles** — Each profile is keyed by the `color` parameter value
- **Download path** — Set default download directory (stored separately)
- **TOML format** — Human-readable config file
- **Cookie support** — Browser cookies for restricted content

### Configuration File Location

| Platform    | Path                                               |
| ----------- | -------------------------------------------------- |
| **Windows** | `%LOCALAPPDATA%\fm-dlp\config.toml`                |
| **macOS**   | `~/Library/Application Support/fm-dlp/config.toml` |
| **Linux**   | `~/.config/fm-dlp/config.toml`                     |

### Configuration Profiles

The configuration system supports multiple profiles using the `color` parameter as the key. This allows you to maintain different presets (e.g., "default", "high-quality", "video-only") and switch between them.

### Configuration Functions

| Function                | Module                   | Description                                   |
| ----------------------- | ------------------------ | --------------------------------------------- |
| `set_parameters(...)`   | `utils.config.parametrs` | Save download parameters with profile key     |
| `get_parameters(color)` | `utils.config.parametrs` | Load download parameters for specific profile |
| `set_path(path)`        | `utils.config.path`      | Set default download directory                |
| `get_path()`            | `utils.config.path`      | Get current download directory                |

<details>
<summary><b>📘 Click for examples</b></summary>

**Save Download Parameters**

```python
from fm_dlp_core.utils.config.parametrs import set_parameters, get_parameters

# Save parameters with a specific color/key
set_parameters(
    codec="mp3",
    kbps=256,
    quality="720p",
    jobs=4,
    quiet=False,
    metadata=True,
    keep=False,
    only_video=False,
    cookies="chrome",
    remote="ejs:github",
    color=True,  # This serves as the profile key
)

# Load saved parameters for the same profile
params = get_parameters(color=True)
print(params)  # {'codec': 'mp3', 'kbps': 256, ...}

# Different profile
set_parameters(codec="flac", kbps=0, color=False)
params_high = get_parameters(color=False)
```

---

**Set Download Path**

```python
from fm_dlp_core.utils.config.path import set_path, get_path

# Set download path
result = set_path("/my/download/folder")
print(result)  # "Configuration saved successfully"

# Get current path
path = get_path()
print(f"Downloads will be saved to: {path}")
```

---

**Configuration File Examples**

```toml
path = "/home/user/folder"

[parameters]  # Profile for color=True
codec = "opus"
kbps = 256
quality = "best"
jobs = 5
quiet = false
metadata = true
keep = false
only_video = false
cookies = "firefox"
remote = "ejs:github"

[parameters_0]  # Profile for color=False
codec = "mp3"
kbps = 192
quality = "1080"
jobs = 3
quiet = true
metadata = true
keep = false
only_video = false
cookies = "chrome"
remote = "ejs:github"
```

---

**Using Configuration in Downloads**

```python
import asyncio
from fm_dlp_core import run_downloader

# This will automatically load saved config if use_config=True
asyncio.run(
    run_downloader(
        url="https://youtube.com/watch?v=...",
        codec="mp3",  # Will be overridden by saved config if use_config=True
        use_config=True,
        color=True,  # Determines which profile to load
    )
)

# Save current parameters for future use
asyncio.run(
    run_downloader(
        url="https://youtube.com/watch?v=...",
        codec="flac",
        kbps=0,
        save=True,  # Save these parameters
        color=True,
    )
)
```

</details>

---

## 🔧 Advanced Topics

<details>
<summary><b>Custom Search Providers</b></summary>

Create your own search provider by subclassing `BaseProvider`:

```python
from fm_dlp_core.commands.search.providers import BaseProvider

class SoundCloudProvider(BaseProvider):
    def _extract_results(self, query: str, limit: int, is_track: bool) -> list:
        # Implement your search logic
        # Return list of entries (dicts)
        return results

    def _extract_url(self, entry: dict, is_track: bool) -> str | None:
        return entry.get("permalink_url")

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
        return f"No results found for '{query}'\n"

# Use your provider
provider = SoundCloudProvider(color=True, error_prefix="Error: ")
for result in provider.search(query="lo-fi", limit=5, is_track=True):
    print(result)
```

</details>

<details>
<summary><b>Custom yt-dlp Options</b></summary>

For advanced use cases, you can build custom yt-dlp options:

```python
from fm_dlp_core.commands.downloader import DownloadParams, OptionsBuilder

params = DownloadParams(
    url="https://youtube.com/watch?v=...",
    codec="mp3",
    kbps=320,
    quality="best",
    jobs=4,
    quiet=False,
    metadata=True,
    keep=False,
    save=False,
    use_config=False,
    path="./downloads",
    only_video=False,
    cookies="firefox",
    remote="ejs:github",
    color=True,
)

builder = OptionsBuilder(params)
opts = builder.build()

# Add custom options
opts["extractor_args"] = {"youtube": {"skip": ["hls"]}}

# Use with yt-dlp directly
from yt_dlp import YoutubeDL
with YoutubeDL(opts) as ydl:
    ydl.download(["https://youtube.com/watch?v=..."])
```

</details>

<details>
<summary><b>Cookie Authentication</b></summary>

For private or age-restricted content:

```python
import asyncio
from fm_dlp_core import run_downloader

# Using browser cookies
asyncio.run(
    run_downloader(
        url="https://youtube.com/watch?v=...",
        codec="mp3",
        cookies="chrome",  # or "firefox", "edge", "opera"
        path="./downloads",
    )
)

# Using cookies file
asyncio.run(
    run_downloader(
        url="https://youtube.com/watch?v=...",
        codec="mp3",
        cookies="./cookies.txt",
        path="./downloads",
    )
)
```

</details>

<details>
<summary><b>Quality String Parsing</b></summary>

The `quality` parameter supports the following formats:

| Format    | Description                                               |
| --------- | --------------------------------------------------------- |
| `"best"`  | Highest available video quality (`bestvideo`)             |
| `"worst"` | Lowest available video quality (`worstvideo`)             |
| `"1080"`  | Best video with height ≤ 1080 (`bestvideo[height<=1080]`) |
| `"1080p"` | Same as `"1080"` (strips the 'p' suffix)                  |
| Custom    | Any valid yt-dlp format filter string                     |

</details>

---

## 📚 API Reference

### Core Package

| Module                            | Description                                                 |
| --------------------------------- | ----------------------------------------------------------- |
| `fm_dlp_core`                     | Main package with `Download`, `Search`, and utilities       |
| `fm_dlp_core.commands.downloader` | Download functionality with `Download` and `run_downloader` |
| `fm_dlp_core.commands.search`     | Search functionality with `Search` and `search`             |
| `fm_dlp_core.utils`               | Shared utilities (colors, constants, config)                |
| `fm_dlp_core.utils.config`        | Configuration management (paths, parameters)                |
| `fm_dlp_core.utils.colors`        | Terminal color utilities                                    |

### Key Classes

| Class                  | Module                                | Description                           |
| ---------------------- | ------------------------------------- | ------------------------------------- |
| `Download`             | `commands.downloader`                 | Async downloader with context manager |
| `DownloadConfig`       | `commands.downloader.config`          | Configuration container               |
| `DownloadParams`       | `commands.downloader.params`          | Data container for all parameters     |
| `OptionsBuilder`       | `commands.downloader.options_builder` | yt-dlp options builder                |
| `URLParser`            | `commands.downloader.url_parser`      | Parse URLs from string/file           |
| `Search`               | `commands.search`                     | Main search handler                   |
| `ResultFormatter`      | `commands.search.formatters`          | Format search results                 |
| `BaseProvider`         | `commands.search.providers`           | Abstract provider base                |
| `YouTubeProvider`      | `commands.search.providers`           | YouTube video search                  |
| `YouTubeMusicProvider` | `commands.search.providers`           | YouTube Music search                  |

### Key Functions

| Function                  | Module                   | Description                 |
| ------------------------- | ------------------------ | --------------------------- |
| `run_downloader`          | `commands.downloader`    | Async download entry point  |
| `search`                  | `commands.search`        | Convenience search function |
| `set_parameters`          | `utils.config.parametrs` | Save download parameters    |
| `get_parameters`          | `utils.config.parametrs` | Load download parameters    |
| `set_path`                | `utils.config.path`      | Set download directory      |
| `get_path`                | `utils.config.path`      | Get download directory      |
| `echo`                    | `utils`                  | Print with color support    |
| `success/error/info/hint` | `utils.colors`           | Formatted colored messages  |

---

## 💡 Examples

<details>
<summary><b>Example 1: Download a Music Playlist</b></summary>

```python
import asyncio
from fm_dlp_core import run_downloader

async def download_playlist(playlist_url: str):
    await run_downloader(
        url=playlist_url,
        codec="flac",
        kbps=0,  # Lossless
        jobs=4,
        metadata=True,
        path="./music",
        color=True,
    )

asyncio.run(download_playlist("https://music.youtube.com/playlist?list=..."))
```

</details>

<details>
<summary><b>Example 2: Search and Download Top Tracks</b></summary>

```python
import asyncio
from fm_dlp_core import search, run_downloader

def get_top_tracks(artist: str, limit: int = 5) -> list[str]:
    return list(search(artist, limit=limit, yt_video=False, only_url=True))

async def download_artist(artist: str):
    urls = get_top_tracks(artist, limit=3)
    if urls:
        await run_downloader(
            url=" ".join(urls),
            codec="mp3",
            kbps=320,
            metadata=True,
            path=f"./music/{artist}",
        )

asyncio.run(download_artist("Porter Robinson"))
```

</details>

<details>
<summary><b>Example 3: Custom Download with Progress Callback</b></summary>

```python
import asyncio
from fm_dlp_core import Download
from fm_dlp_core.commands.downloader.params import DownloadParams

class MyDownloader(Download):
    def _sync_download(self, url: str):
        # Override to add custom behavior
        print(f"Downloading: {url}")
        super()._sync_download(url)

async def main():
    params = DownloadParams(
        url="https://youtube.com/watch?v=...",
        codec="mp4",
        kbps=0,
        quality="1080p",
        jobs=2,
        quiet=False,
        metadata=True,
        keep=False,
        save=False,
        use_config=False,
        path="./videos",
        only_video=True,
        cookies=None,
        remote="ejs:github",
        color=True,
    )
    async with MyDownloader(params) as downloader:
        await downloader.download_all()

asyncio.run(main())
```

</details>

<details>
<summary><b>Example 4: Working with Raw Search Data</b></summary>

```python
from fm_dlp_core import search

# Get raw data for programmatic use
for result in search(
    query="Daft Punk",
    limit=10,
    yt_video=False,
    album=False,
    raw=True,  # Returns dicts
):
    print(f"Title: {result['title']}")
    print(f"Artist: {result.get('artists', [{}])[0].get('name', 'Unknown')}")
    print(f"Duration: {result.get('duration')}s")
    print(f"URL: https://music.youtube.com/watch?v={result.get('videoId')}")
    print("-" * 40)
```

</details>

<details>
<summary><b>Example 5: Error Handling</b></summary>

```python
import asyncio
from fm_dlp_core import run_downloader

async def safe_download(url: str):
    try:
        await run_downloader(
            url=url,
            codec="mp3",
            kbps=192,
            path="./downloads",
        )
    except Exception as e:
        print(f"Download failed for {url}: {e}")

asyncio.run(safe_download("https://youtube.com/watch?v=invalid_id"))
```

</details>

<details>
<summary><b>Example 6: Using Configuration Profiles</b></summary>

```python
from fm_dlp_core.utils.config.parametrs import set_parameters, get_parameters

# Save a profile with color=True
set_parameters(
    codec="flac",
    kbps=0,
    quality="best",
    jobs=4,
    quiet=False,
    metadata=True,
    keep=False,
    only_video=False,
    cookies="chrome",
    remote="ejs:github",
    color=True,
)

# Save another profile with color=False
set_parameters(
    codec="mp3",
    kbps=192,
    quality="720",
    jobs=2,
    quiet=True,
    metadata=True,
    keep=False,
    only_video=False,
    cookies="firefox",
    remote="ejs:github",
    color=False,
)

# Load specific profile
params = get_parameters(color=True)  # Returns the flac profile
params_low = get_parameters(color=False)  # Returns the mp3 profile

# Use a specific profile in download
import asyncio
from fm_dlp_core import run_downloader

async def download_with_profile(profile_color: bool):
    params = get_parameters(color=profile_color)
    await run_downloader(
        url="https://youtube.com/watch?v=...",
        codec=params["codec"],
        kbps=params["kbps"],
        quality=params["quality"],
        jobs=params["jobs"],
        quiet=params["quiet"],
        metadata=params["metadata"],
        keep=params["keep"],
        only_video=params["only_video"],
        cookies=params["cookies"],
        remote=params["remote"],
        use_config=False,  # Manual param passing
        color=profile_color,
    )

asyncio.run(download_with_profile(True))
```

</details>

<details>
<summary><b>Example 7: URLParser Usage</b></summary>

```python
from fm_dlp_core.commands.downloader import URLParser

# Parse URLs from comma-separated string
parser = URLParser("url1,url2,url3", quiet=False)
urls = parser.parse()
print(urls)  # ['url1', 'url2', 'url3']

# Parse URLs from space-separated string
parser = URLParser("url1 url2 url3", quiet=False)
urls = parser.parse()

# Parse URLs from file (one per line, comma/space separated supported)
parser = URLParser("urls.txt", quiet=False)
urls = parser.parse()

# File content example:
# https://youtube.com/watch?v=abc123
# https://youtube.com/watch?v=def456, https://youtube.com/watch?v=ghi789
# # This is a comment (ignored)
# https://youtube.com/watch?v=jkl012
```

</details>

---

## 🖥️ Output Formatting

### Search Results Format

```
    1. Mr. Kill Myself
        ├─ Sewerslvt
        ├─ Draining Love Story
        ├─ 13,456,789 │ 7:52
        └─ https://music.youtube.com/watch?v=y55fzyXZDSE
           ──────────────────────────────────────────────────
```

### Format Elements

| Element              | Description                         |
| -------------------- | ----------------------------------- |
| **N.**               | Sequential result number            |
| **Title**            | Track, album, or video title        |
| **Artist**           | Artist or channel name              |
| `├─└─│`              | Tree structure for visual hierarchy |
| **Views │ Duration** | View count and length               |
| **URL**              | Direct link to content              |

### Colored Output Functions

```python
from fm_dlp_core.utils.colors import success, error, info, hint, styled, BOLD_YELLOW

print(success("Download completed!"))
print(error("Failed to process video"))
print(info("Extracting metadata..."))
print(hint("Try using a higher bitrate for better quality"))
print(styled("Custom styled message", BOLD_YELLOW))
```

---

## 📄 License

This project is licensed under the **AGPLv3 License** — see the [LICENSE](LICENSE) file for details.

### Acknowledgments

| Library                                             | Purpose                                |
| --------------------------------------------------- | -------------------------------------- |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp)          | Download engine supporting 1000+ sites |
| [ytmusicapi](https://github.com/sigma67/ytmusicapi) | YouTube Music search API               |
| [mutagen](https://github.com/quodlibet/mutagen)     | Metadata tagging for audio files       |

---

**Author:** [Fkernel653](https://github.com/Fkernel653)  
**Project:** [GitHub](https://github.com/Fkernel653/fm-dlp-core) • [PyPI](https://pypi.org/project/fm-dlp-core)  
**Documentation:** [fm-dlp-core Docs](https://github.com/Fkernel653/fm-dlp-core#readme)

---

_If you encounter any issues, please [open an issue](https://github.com/Fkernel653/fm-dlp-core/issues) on GitHub._
