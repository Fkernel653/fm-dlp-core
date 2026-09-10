# fm-dlp-core — Core Library for YouTube & 1000+ Sites

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=fff&style=for-the-badge)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/fm-dlp-core?style=for-the-badge&logo=pypi&logoColor=fff&label=PyPI&color=007ec6)](https://pypi.org/project/fm-dlp-core)
[![License](https://img.shields.io/badge/License-AGPLv3-00b96b?style=for-the-badge&logo=gnu&logoColor=white)](LICENSE)
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

- **Python 3.11+** - TOML support required
- **FFmpeg** - Required for audio/video processing. Install via:
  - **macOS:** `brew install ffmpeg`
  - **Linux:**
    - **Debian:** `sudo apt install ffmpeg`
    - **Fedora:** `sudo dnf install ffmpeg`
    - **Arch Linux:** `sudo pacman -S ffmpeg`
  - **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

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
from fm_dlp_core.commands.downloader import DownloadParams

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
from fm_dlp_core.commands.downloader import Download, DownloadParams


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
from fm_dlp_core.commands.downloader import Download, DownloadParams

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
    yt_video=False,  # Use YouTube Music
    album=False,  # Search for tracks
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
    album=True,  # Search for albums
):
    print(result)
```

---

**YouTube Video Search**

```python
for result in search(
    query="Python tutorial",
    limit=5,
    yt_video=True,  # Use YouTube (videos)
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
- **Automatic config management** — TOML serialization and caching for performance

### Configuration File Location

| Platform    | Path                                               |
| ----------- | -------------------------------------------------- |
| **Windows** | `%LOCALAPPDATA%\fm-dlp\config.toml`                |
| **macOS**   | `~/Library/Application Support/fm-dlp/config.toml` |
| **Linux**   | `~/.config/fm-dlp/config.toml`                     |

### Configuration Architecture

The configuration subsystem is composed of three collaborating modules:

| Module           | Responsibility                                                       |
| ---------------- | -------------------------------------------------------------------- |
| `config_manager` | Core file I/O, TOML serialization, platform-specific path resolution |
| `parametrs`      | Read/write the `[parameters]` section (download settings)            |
| `path`           | Read/write the top-level `path` key (download directory)             |

### ConfigManager Class

The `ConfigManager` class is the low-level engine responsible for loading and updating the TOML configuration file.

```python
from fm_dlp_core.utils.config import ConfigManager

manager = ConfigManager(color=True)

# Load configuration (cached for performance via @lru_cache(maxsize=1))
config = manager.load_config()

# Update configuration (automatically invalidates the cache)
config["path"] = "/downloads"
manager.update_config(config)  # Returns True on success
```

**Key behaviors:**

- `load_config()` is a `@staticmethod` wrapped with `@lru_cache(maxsize=1)` — repeated reads hit the in-memory cache instead of disk
- `update_config()` calls `self.load_config.cache_clear()` after a successful write, so the next read reflects the new data
- Corrupted TOML files are handled gracefully: an error is printed and an empty dict is returned
- Missing config files return an empty dict without raising

### TOMLSerializer Class

The `TOMLSerializer` class converts Python data structures into TOML string representation. It is used internally by `ConfigManager.update_config()`.

```python
from fm_dlp_core.utils.config import TOMLSerializer

data = {
    "path": "/downloads",
    "parameters": {"codec": "mp3", "kbps": 320, "quality": "best"},
}
toml_string = TOMLSerializer.dumps(data)
print(toml_string)
# Output:
# path = "/downloads"
#
# [parameters]
# codec = "mp3"
# kbps = 320
# quality = "best"
#
```

**Supported types:**

| Python Type | TOML Output         |
| ----------- | ------------------- |
| `str`       | `"value"`           |
| `bool`      | `true` / `false`    |
| `int`       | `42`                |
| `list`      | `[item1, item2]`    |
| `dict`      | `{ key = "value" }` |

### ParametersManager Class

Manages the `[parameters]` section — codec, bitrate, quality, jobs, boolean flags, cookies, and remote URL.

```python
from fm_dlp_core.utils.config import ParametersManager

manager = ParametersManager(color=True)

# Save parameters
manager.set_parameters(
    codec="mp3",
    kbps=320,
    quality="best",
    jobs=4,
    quiet=False,
    metadata=True,
    keep=False,
    only_video=False,
    cookies="firefox",
    remote="ejs:github",
)

# Retrieve parameters
params = manager.get_parameters()
print(params["codec"])  # 'mp3'
```

**Key behaviors:**

- `PARAM_KEY = "parameters"` — the TOML section name
- The `remote` value is validated via `validate_remote()` before being stored
- `cookies` and `remote` are only written if truthy (omitted from the config otherwise)
- Success/error messages are suppressed when `quiet=True`

### PathManager Class

Manages the top-level `path` key — the download directory.

```python
from fm_dlp_core.utils.config import PathManager

manager = PathManager(color=True)

# Save a path (tilde is expanded, existence is validated)
manager.set_path("~/Downloads")
# Returns: 'Configuration saved successfully'

# Retrieve the path
manager.get_path()
# Returns: '/home/user/Downloads'
```

**Key behaviors:**

- `PATH_KEY = "path"` — the top-level TOML key
- `set_path()` expands `~`, resolves to absolute, and validates that the directory exists
- `get_path()` returns `Path.home()` with an info hint if no config file exists
- Exits with code 1 if the stored path is missing or no longer a valid directory

### Configuration Functions

| Function                                | Module                   | Description                              |
| --------------------------------------- | ------------------------ | ---------------------------------------- |
| `get_config_dir()`                      | `utils.config_manager`   | Get OS-specific config directory path    |
| `ConfigManager.load_config()`           | `utils.config_manager`   | Load config from TOML file with caching  |
| `ConfigManager.update_config()`         | `utils.config_manager`   | Update config file, creating directories |
| `ParametersManager.set_parameters(...)` | `utils.config.parametrs` | Save download parameters                 |
| `ParametersManager.get_parameters()`    | `utils.config.parametrs` | Load download parameters                 |
| `PathManager.set_path(path)`            | `utils.config.path`      | Set default download directory           |
| `PathManager.get_path()`                | `utils.config.path`      | Get current download directory           |
| `TOMLSerializer.dumps(data)`            | `utils.config_manager`   | Serialize dict to TOML string            |

### Configuration Management Features

1. **Cross-Platform Path Resolution**
   - Windows: Uses `LOCALAPPDATA` or `APPDATA` environment variables
   - macOS: Uses `~/Library/Application Support`
   - Linux: Uses `XDG_CONFIG_HOME` or `~/.config`

2. **Caching for Performance**
   - Configuration is cached using `@lru_cache(maxsize=1)`
   - Cache is automatically cleared when configuration is updated

3. **Error Handling**
   - Gracefully handles corrupted config files with colored error messages
   - Automatically creates new config file if corrupted or missing
   - Permission errors and OS errors are caught and reported

4. **Atomic Operations**
   - Configuration file operations create parent directories as needed
   - Writes are performed via `Path.write_text()` with UTF-8 encoding

### Configuration Profiles

The configuration system supports multiple profiles using the `color` parameter as the key. This allows you to maintain different presets (e.g., "default", "high-quality", "video-only") and switch between them.

<details>
<summary><b>📘 Click for examples</b></summary>

**Loading Configuration with Caching**

```python
from fm_dlp_core.utils.config import ConfigManager

manager = ConfigManager(color=True)

# Load configuration (cached for performance)
config = manager.load_config()
print(config)  # {'path': '/downloads', 'parameters': {...}}

# Update configuration (clears cache automatically)
new_config = {
    "path": "/new/downloads",
    "parameters": {
        "codec": "flac",
        "kbps": 0,
        "quality": "best",
        "jobs": 4,
        "metadata": True,
    },
}
success = manager.update_config(new_config)
if success:
    print("Configuration updated successfully")
    # Cache is automatically cleared
```

**Manual Configuration File Management**

```python
from fm_dlp_core.utils.config import (
    CONFIG_DIR,
    CONFIG_FILE,
    ENCODING,
    TOMLSerializer,
)

# Get configuration directory
print(f"Config directory: {CONFIG_DIR}")
# Output: /home/user/.config/fm-dlp (Linux)
# Output: /Users/user/Library/Application Support/fm-dlp (macOS)
# Output: C:\Users\user\AppData\Local\fm-dlp (Windows)

# Check if config file exists
if CONFIG_FILE.exists():
    print("Config file found!")
    content = CONFIG_FILE.read_text(encoding=ENCODING)
    print(content)

# Create custom TOML data
data = {
    "path": "/custom/path",
    "parameters": {
        "codec": "opus",
        "kbps": 192,
        "quality": "720p",
        "quiet": True,
        "metadata": True,
        "keep": False,
        "only_video": False,
        "cookies": "firefox",
        "remote": "ejs:github",
    },
}

# Serialize and save manually
toml_content = TOMLSerializer.dumps(data)
CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
CONFIG_FILE.write_text(toml_content, encoding=ENCODING)
```

**Automatic Profile Management**

```python
from fm_dlp_core.utils.config import ParametersManager

# Save different profiles (keyed by the color flag)
ParametersManager(color=True).set_parameters(
    codec="flac", kbps=0, quality="best", jobs=8,
    quiet=False, metadata=True, keep=False, only_video=False,
)

ParametersManager(color=False).set_parameters(
    codec="aac", kbps=128, quality="720p", jobs=2,
    quiet=True, metadata=True, keep=False, only_video=False,
)

# Load specific profiles
print(f"High quality: {ParametersManager(color=True).get_parameters()}")
print(f"Mobile quality: {ParametersManager(color=False).get_parameters()}")
```

**Configuration Directory Structure**

```python
from fm_dlp_core.utils.config import get_config_dir

# Get configuration directory
config_dir = get_config_dir("my-app")  # Custom application name
print(f"Config directory: {config_dir}")

# Default directory for fm-dlp
default_dir = get_config_dir()  # Uses "fm-dlp"
print(f"Default config directory: {default_dir}")
```

</details>

### Configuration File Examples

```toml
# Main configuration file: config.toml
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

### Configuration API Reference

| Class / Method                          | Description                                        |
| --------------------------------------- | -------------------------------------------------- |
| `get_config_dir(dir_name)`              | Get OS-specific config directory path              |
| `CONFIG_DIR`                            | Global constant for config directory               |
| `CONFIG_FILE`                           | Global constant for config file path               |
| `ENCODING`                              | Global encoding constant (`"utf-8"`)               |
| `ConfigManager(color)`                  | Create a config manager instance                   |
| `ConfigManager.load_config()`           | Load config with LRU caching and error handling    |
| `ConfigManager.update_config(data)`     | Update config file, creating directories if needed |
| `TOMLSerializer.dumps(data)`            | Serialize dict to TOML string                      |
| `TOMLSerializer._value_to_str(value)`   | Convert a Python value to TOML string              |
| `ParametersManager(color)`              | Create a parameters manager instance               |
| `ParametersManager.set_parameters(...)` | Write download parameters to config                |
| `ParametersManager.get_parameters()`    | Read download parameters from config               |
| `PathManager(color)`                    | Create a path manager instance                     |
| `PathManager.set_path(path)`            | Set and validate the download directory            |
| `PathManager.get_path()`                | Get the current download directory                 |

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

| Module                                    | Description                                                 |
| ----------------------------------------- | ----------------------------------------------------------- |
| `fm_dlp_core`                             | Main package with `Download`, `Search`, and utilities       |
| `fm_dlp_core.commands.downloader`         | Download functionality with `Download` and `run_downloader` |
| `fm_dlp_core.commands.search`             | Search functionality with `Search` and `search`             |
| `fm_dlp_core.utils`                       | Shared utilities (colors, constants, config)                |
| `fm_dlp_core.utils.config`                | Configuration management (paths, parameters)                |
| `fm_dlp_core.utils.config.config_manager` | Core config I/O and TOML serialization                      |
| `fm_dlp_core.utils.config.parametrs`      | Parameter management for download configurations            |
| `fm_dlp_core.utils.config.path`           | Path management for download directories                    |
| `fm_dlp_core.utils.colors`                | Terminal color utilities                                    |

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
| `ConfigManager`        | `utils.config.config_manager`         | Low-level TOML config load/update     |
| `TOMLSerializer`       | `utils.config.config_manager`         | Serialize Python dicts to TOML        |
| `ParametersManager`    | `utils.config.parametrs`              | Manage `[parameters]` section         |
| `PathManager`          | `utils.config.path`                   | Manage download path                  |

### Key Functions

| Function                  | Module                        | Description                 |
| ------------------------- | ----------------------------- | --------------------------- |
| `run_downloader`          | `commands.downloader`         | Async download entry point  |
| `search`                  | `commands.search`             | Convenience search function |
| `get_config_dir`          | `utils.config.config_manager` | Get OS-specific config dir  |
| `echo`                    | `utils.output`                | Print with color support    |
| `success/error/info/hint` | `utils.colors`                | Formatted colored messages  |

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
<summary><b>Example 3: Working with Raw Search Data</b></summary>

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
<summary><b>Example 4: Error Handling</b></summary>

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
<summary><b>Example 5: Using Configuration Profiles</b></summary>

```python
from fm_dlp_core.utils.config import ParametersManager

# Save a profile with color=True
ParametersManager(color=True).set_parameters(
    codec="flac", kbps=0, quality="best", jobs=4,
    quiet=False, metadata=True, keep=False, only_video=False,
    cookies="chrome", remote="ejs:github",
)

# Save another profile with color=False
ParametersManager(color=False).set_parameters(
    codec="mp3", kbps=192, quality="720", jobs=2,
    quiet=True, metadata=True, keep=False, only_video=False,
    cookies="firefox", remote="ejs:github",
)

# Load specific profile
params = ParametersManager(color=True).get_parameters()   # flac profile
params_low = ParametersManager(color=False).get_parameters()  # mp3 profile

# Use a specific profile in download
import asyncio
from fm_dlp_core import run_downloader


async def download_with_profile(profile_color: bool):
    params = ParametersManager(color=profile_color).get_parameters()
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
<summary><b>Example 6: URLParser Usage</b></summary>

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
