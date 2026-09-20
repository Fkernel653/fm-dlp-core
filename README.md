# fm-dlp-core — Core Library for YouTube & 1000+ Sites

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=fff&style=for-the-badge)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/fm-dlp-core?style=for-the-badge&logo=pypi&logoColor=fff&label=PyPI&color=007ec6)](https://pypi.org/project/fm-dlp-core)
[![License](https://img.shields.io/badge/License-AGPLv3-00b96b?style=for-the-badge&logo=gnu&logoColor=white)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-9cf?style=for-the-badge)](<>)
[![Ruff](https://img.shields.io/badge/Code%20Style-Ruff-ff69b4?logo=ruff&logoColor=fff&style=for-the-badge)](https://docs.astral.sh/ruff)

**fm-dlp-core** is a powerful Python library for searching and downloading content from YouTube, YouTube Music, and over 1000+ supported sites. Built on top of yt-dlp, it provides a clean, async-first API with rich features including concurrent downloads, metadata embedding, subtitle download/embedding, arbitrary yt-dlp args passthrough, and flexible output formatting.

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Requirements](#-requirements)
- [Core Concepts](#-core-concepts)
- [Downloading Content](#-downloading-content)
  - [Subtitles](#-subtitles)
  - [Raw yt-dlp Arguments](#-raw-yt-dlp-arguments)
- [Searching Content](#-searching-content)
- [Configuration](#-configuration)
- [API Reference](#-api-reference)
- [License & Acknowledgments](#-license--acknowledgments)

---

## 🚀 Quick Start

```python
import asyncio
from fm_dlp_core import search, run_downloader
from fm_dlp_core.commands.downloader import DownloadParams

# 1. Search for a track
for result in search("Sewerslvt", limit=3, yt_video=False, album=False):
    print(result)

# 2. Download a track
asyncio.run(
    run_downloader(
        DownloadParams(
            url="https://music.youtube.com/watch?v=y55fzyXZDSE",
            codec="mp3",
            kbps=320,
            quality="best",
            jobs=4,
            quiet=False,
            metadata=True,
            keep=False,
            save=False,
            use_config=False,
            path="./music",
            only_video=False,
            cookies=None,
            remote=None,
            color=True,
        )
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
- **FFmpeg** - Required for audio/video processing and subtitle embedding. Install via:
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

Settings like codec, bitrate, quality, subtitle preferences, and download path can be saved to a TOML file and reused across sessions.

### Provider Pattern

Search functionality is built on a provider pattern, making it easy to add support for new platforms by subclassing `BaseProvider`.

### Layered yt-dlp Options

The `OptionsBuilder` assembles options in priority order:

1. Base options (output template, concurrency, retries)
2. Color / cookies / remote configuration
3. Codec-specific options (audio extraction, video conversion)
4. Subtitle options (if `subtitles=True`)
5. **User-provided `ytdlp_args`** — merged last, highest priority (`postprocessors` are extended, not replaced)

---

## 🎵 Downloading Content

### Overview

The download system supports:

- **Audio extraction** in 8 formats (MP3, AAC, FLAC, M4A, Opus, Vorbis, WAV, ALAC)
- **Video download** in MP4, MKV, WebM, MOV, AVI, FLV with quality selection
- **Batch downloads** from multiple URLs or text files
- **Concurrent downloads** with configurable job limits
- **Metadata embedding** with thumbnails
- **Subtitle download**, including **auto-generated** subtitles, and **embedding** into the video container
- **Arbitrary yt-dlp arguments** passthrough for advanced use cases

### DownloadParams Class

All download parameters are encapsulated in the `DownloadParams` dataclass:

```python
from fm_dlp_core.commands.downloader import DownloadParams

params = DownloadParams(
    url="https://youtube.com/watch?v=...",
    codec="mp4",
    kbps=0,
    quality="1080p",
    jobs=4,
    quiet=False,
    metadata=True,
    keep=False,
    save=False,
    use_config=False,
    path="./downloads",
    only_video=True,
    cookies="chrome",
    remote="ejs:github",
    color=True,
    # --- Subtitles ---
    subtitles=True,
    subtitle_langs="en,ru",
    embed_subs=True,
    auto_subs=False,
    # --- Raw yt-dlp args ---
    ytdlp_args={
        "retries": 10,
        "fragment_retries": 10,
        "subtitlesformat": "srt/best",
        "postprocessors": [{"key": "FFmpegMetadata"}],
    },
)
```

### Download Parameters Reference

| Parameter        | Type                        | Description                                                                                                                                        |
| ---------------- | --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`            | `str`                       | URL(s) to download (comma/space separated or path to file)                                                                                         |
| `codec`          | `str`                       | Output format (see Supported Codecs)                                                                                                               |
| `kbps`           | `int`                       | Audio bitrate in kbps. Use `0` for lossless formats (FLAC, WAV, ALAC)                                                                              |
| `quality`        | `str`                       | Video quality: `"best"`, `"worst"`, `"1080"`, `"1080p"`, or custom format filter                                                                   |
| `jobs`           | `int`                       | Number of concurrent downloads (also controls thread/process pool size)                                                                            |
| `quiet`          | `bool`                      | Suppress output messages                                                                                                                           |
| `metadata`       | `bool`                      | Embed metadata and thumbnail. **Note:** Automatically disabled for WAV format (not supported)                                                      |
| `keep`           | `bool`                      | Keep original downloaded file (video file when extracting audio)                                                                                   |
| `save`           | `bool`                      | Save parameters to config (requires `color` parameter for config key)                                                                              |
| `use_config`     | `bool`                      | Load parameters from config. Saved values take priority over instance values. Config key uses the `color` parameter value                          |
| `path`           | `str`                       | Download directory                                                                                                                                 |
| `only_video`     | `bool`                      | Download video only (skip audio extraction). Uses `ProcessPoolExecutor` for video processing                                                       |
| `cookies`        | `str \| None`               | Cookies file path or browser name (`"chrome"`, `"firefox"`, `"edge"`, `"opera"`). Uses cookiefile if path exists, otherwise cookiesfrombrowser     |
| `remote`         | `str \| None`               | External JavaScript components source for bypassing anti-bot protections. Valid values: `"ejs:github"` (yt-dlp repo) or `"ejs:npm"` (NPM registry) |
| `color`          | `bool`                      | Enable colored output. Also used as the configuration key identifier for storing/retrieving settings                                               |
| `subtitles`      | `bool`                      | Download subtitles (`writesubtitles`). Requires FFmpeg for embedding                                                                               |
| `subtitle_langs` | `str`                       | Comma-separated subtitle language codes, e.g. `"en,ru,ja"` → `subtitleslangs`                                                                      |
| `embed_subs`     | `bool`                      | Embed subtitles into the video container (`FFmpegEmbedSubtitle`). Only for video containers (mp4, mkv, webm, mov)                                  |
| `auto_subs`      | `bool`                      | Include auto-generated subtitles (`writeautomaticsub`)                                                                                             |
| `ytdlp_args`     | `dict[str, object] \| None` | Extra raw yt-dlp options (snake_case). Merged last; `postprocessors` are **extended**, other keys **override**                                     |

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

---

### 📝 Subtitles

Subtitles can be downloaded alongside video/audio, saved as separate files, or embedded directly into the video container.

#### How it works

| Flag              | yt-dlp option(s)                                           | Effect                                           |
| ----------------- | ---------------------------------------------------------- | ------------------------------------------------ |
| `subtitles=True`  | `writesubtitles=True`, `subtitleslangs=[...]`              | Downloads subtitle files for the given languages |
| `auto_subs=True`  | `writeautomaticsub=True`                                   | Includes auto-generated subtitles                |
| `embed_subs=True` | `embedsubtitles=True`, postprocessor `FFmpegEmbedSubtitle` | Muxes subtitles into the video container         |

> ⚠️ **Embedding caveats**
>
> - Requires FFmpeg.
> - Only makes sense for **video** codecs (`mp4`, `mkv`, `webm`, `mov`) or when `only_video=True`.
> - For audio-only codecs (mp3, flac, etc.) `embed_subs` is silently skipped.

#### Language selection

`subtitle_langs` is a **comma-separated** string, e.g. `"en,ru,ja"`. Whitespace is stripped. If empty, defaults to `["en"]`.

<details>
<summary><b>📖 Subtitle examples</b></summary>

**Download video with English + Russian subtitles embedded into MKV**

```python
from fm_dlp_core.commands.downloader import Download, DownloadParams

params = DownloadParams(
    url="https://youtube.com/watch?v=VIDEO_ID",
    codec="mkv",
    kbps=0,
    quality="1080p",
    jobs=1,
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
    subtitles=True,
    subtitle_langs="en,ru",
    embed_subs=True,
    auto_subs=False,
)

async with Download(params) as dl:
    await dl.download_all()
```

---

**Download audio with subtitles saved as separate .srt files**

```python
params = DownloadParams(
    url="https://youtube.com/watch?v=VIDEO_ID",
    codec="mp3",
    kbps=320,
    quality="best",
    jobs=2,
    quiet=False,
    metadata=True,
    keep=False,
    save=False,
    use_config=False,
    path="./audio",
    only_video=False,
    cookies=None,
    remote=None,
    color=True,
    subtitles=True,
    subtitle_langs="en",
    embed_subs=False,   # audio → embedding is skipped anyway
    auto_subs=True,     # include auto-generated
)
```

</details>

---

### 🧩 Raw yt-dlp Arguments

For anything not covered by the high-level API, you can pass arbitrary yt-dlp options via `ytdlp_args`.

#### Rules

- Keys are **snake_case** yt-dlp option names (the same keys used by `YoutubeDL(opts)`).
- Options are merged **last** into the built options dict → they **override** existing values.
- **Exception:** `postprocessors` are **extended** (built-in postprocessors are preserved) rather than replaced.

<details>
<summary><b>📖 yt-dlp args examples</b></summary>

**Add retries and a custom subtitle format**

```python
params = DownloadParams(
    # ... required fields ...
    ytdlp_args={
        "retries": 10,
        "fragment_retries": 10,
        "subtitlesformat": "srt/best",
    },
)
```

**Extend postprocessors without losing built-ins**

```python
params = DownloadParams(
    # ... required fields ...
    ytdlp_args={
        "postprocessors": [
            {"key": "FFmpegMetadata"},
            {"key": "SponsorBlock", "categories": ["sponsor"]},
        ],
    },
)
# Built-in postprocessors (e.g. FFmpegExtractAudio / FFmpegVideoConvertor)
# are preserved and the custom ones are appended.
```

**Rate-limit requests**

```python
params = DownloadParams(
    # ... required fields ...
    ytdlp_args={
        "sleep_interval_requests": 1,
        "sleep_interval": 2,
        "max_sleep_interval": 5,
    },
)
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
<summary><b>📖 Click for examples</b></summary>

**YouTube Music Search (Tracks)**

```python
from fm_dlp_core import Search

for result in Search(
    query="Sewerslvt",
    limit=5,
    yt_video=False,  # Use YouTube Music
    album=False,     # Search for tracks
    color=True,
).search():
    print(result)
```

---

**YouTube Video Search**

```python
for result in Search(
    query="Python tutorial",
    limit=5,
    yt_video=True,  # Use YouTube (videos)
    album=False,
).search():
    print(result)
```

---

**URL-Only Output**

```python
from fm_dlp_core.commands.downloader import DownloadParams

# Get only URLs
urls = list(search("breakcore", limit=10, only_url=True))

# Chain search → download
urls = list(search("chill beats", limit=5, only_url=True))
if urls:
    asyncio.run(
        run_downloader(
            DownloadParams(
                url=" ".join(urls),
                codec="mp3",
                kbps=320,
                quality="best",
                jobs=4,
                quiet=False,
                metadata=True,
                keep=False,
                save=False,
                use_config=False,
                path="./music",
                only_video=False,
                cookies=None,
                remote=None,
                color=True,
            )
        )
    )
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
- **Subtitle preferences** — Persist subtitle/auto-sub/embed settings and languages
- **Raw yt-dlp args** — Persist advanced overrides

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

### TOMLSerializer Class

The `TOMLSerializer` class converts Python data structures into TOML string representation. It is used internally by `ConfigManager.update_config()`.

```python
from fm_dlp_core.utils.config import TOMLSerializer

data = {
    "path": "/downloads",
    "parameters": {
        "codec": "mp3",
        "kbps": 320,
        "quality": "best",
        "subtitles": True,
        "subtitle_langs": "en,ru",
        "embed_subs": True,
        "auto_subs": False,
    },
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
# subtitles = true
# subtitle_langs = "en,ru"
# embed_subs = true
# auto_subs = false
#
```

**Supported types:**

| Python Type | TOML Output         |
| ----------- | ------------------- |
| `str`       | `"value"`           |
| `int`       | `value`             |
| `bool`      | `true`              |
| `dict`      | `{ key = "value" }` |

### ParametersManager Class

Manages the `[parameters]` section — codec, bitrate, quality, jobs, boolean flags, cookies, remote URL, subtitles, and raw yt-dlp args.

> **Note:** `set_parameters()` now accepts a single `DownloadParams` instance.

```python
from fm_dlp_core.commands.downloader import DownloadParams
from fm_dlp_core.utils.config import ParametersManager

manager = ParametersManager(color=True)

# Save parameters (pass a DownloadParams instance)
manager.set_parameters(
    DownloadParams(
        url="",  # URL is intentionally not persisted
        codec="mp4",
        kbps=0,
        quality="1080p",
        jobs=4,
        quiet=False,
        metadata=True,
        keep=False,
        save=True,
        use_config=False,
        path="./videos",
        only_video=True,
        cookies="firefox",
        remote="ejs:github",
        color=True,
        subtitles=True,
        subtitle_langs="en,ru",
        embed_subs=True,
        auto_subs=False,
        ytdlp_args={"retries": 10},
    )
)

# Retrieve parameters
params = manager.get_parameters()
print(params["codec"])           # 'mp4'
print(params["subtitles"])       # True
print(params["subtitle_langs"])  # 'en,ru'
```

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

### Configuration Functions

| Function                                | Module                   | Description                              |
| --------------------------------------- | ------------------------ | ---------------------------------------- |
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

2. **Error Handling**
   - Gracefully handles corrupted config files with colored error messages
   - Automatically creates new config file if corrupted or missing
   - Permission errors and OS errors are caught and reported

3. **Atomic Operations**
   - Configuration file operations create parent directories as needed
   - Writes are performed via `Path.write_text()` with UTF-8 encoding

### Configuration Profiles

The configuration system supports multiple profiles using the `color` parameter as the key.

<details>
<summary><b>📖 Click for examples</b></summary>

**Loading Configuration with Caching**

```python
from fm_dlp_core.utils.config import ConfigManager

manager = ConfigManager(color=True)

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
        "subtitles": True,
        "subtitle_langs": "en,ru",
    },
}
success = manager.update_config(new_config)
if success:
    print("Configuration updated successfully")
    # Cache is automatically cleared
```

**Automatic Profile Management**

```python
from fm_dlp_core.commands.downloader import DownloadParams
from fm_dlp_core.utils.config import ParametersManager

# Save different profiles (keyed by the color flag)
ParametersManager(color=True).set_parameters(
    DownloadParams(
        url="", codec="flac", kbps=0, quality="best", jobs=8,
        quiet=False, metadata=True, keep=False, save=True, use_config=False,
        path="./music", only_video=False, cookies=None, remote=None, color=True,
        subtitles=True, subtitle_langs="en,ru", embed_subs=True, auto_subs=False,
    )
)

ParametersManager(color=False).set_parameters(
    DownloadParams(
        url="", codec="aac", kbps=128, quality="720p", jobs=2,
        quiet=True, metadata=True, keep=False, save=True, use_config=False,
        path="./mobile", only_video=False, cookies=None, remote=None, color=False,
        subtitles=False, subtitle_langs="en", embed_subs=False, auto_subs=False,
    )
)

# Load specific profiles
print(f"High quality: {ParametersManager(color=True).get_parameters()}")
print(f"Mobile quality: {ParametersManager(color=False).get_parameters()}")
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
subtitles = true
subtitle_langs = "en,ru"
embed_subs = false
auto_subs = true

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
subtitles = false
subtitle_langs = "en"
embed_subs = false
auto_subs = false
```

---

**Using Configuration in Downloads**

```python
import asyncio
from fm_dlp_core import run_downloader
from fm_dlp_core.commands.downloader import DownloadParams

# This will automatically load saved config if use_config=True
asyncio.run(
    run_downloader(
        DownloadParams(
            url="https://youtube.com/watch?v=...",
            codec="mp3",       # Will be overridden by saved config if use_config=True
            kbps=0,
            quality="best",
            jobs=1,
            quiet=False,
            metadata=True,
            keep=False,
            save=False,
            use_config=True,
            path="./downloads",
            only_video=False,
            cookies=None,
            remote=None,
            color=True,        # Determines which profile to load
        )
    )
)

# Save current parameters for future use
asyncio.run(
    run_downloader(
        DownloadParams(
            url="https://youtube.com/watch?v=...",
            codec="flac",
            kbps=0,
            quality="best",
            jobs=4,
            quiet=False,
            metadata=True,
            keep=False,
            save=True,         # Save these parameters
            use_config=False,
            path="./music",
            only_video=False,
            cookies=None,
            remote=None,
            color=True,
            subtitles=True,
            subtitle_langs="en,ru",
            embed_subs=True,
            auto_subs=False,
            ytdlp_args={"retries": 10},
        )
    )
)
```

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

| Function                  | Module                | Description                 |
| ------------------------- | --------------------- | --------------------------- |
| `run_downloader`          | `commands.downloader` | Async download entry point  |
| `search`                  | `commands.search`     | Convenience search function |
| `echo`                    | `utils`               | Print with color support    |
| `success/error/info/hint` | `utils.colors`        | Formatted colored messages  |

---

## 🛠️ Output Formatting

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

| Element            | Description                               |
| ------------------ | ----------------------------------------- |
| `N.`               | Sequential number of search result        |
| `Title`            | Track, album, or video title              |
| `Artist`           | Artist or channel name                    |
| `├─└─│`            | Tree branch characters                    |
| `Views │ Duration` | View count and length (MM:SS or HH:MM:SS) |
| `URL`              | Direct link to content                    |
| `───`              | Visual separator line                     |

---

## 📄 License & Acknowledgments

AGPLv3 License — Built with:

| Library                                             | Purpose                                |
| --------------------------------------------------- | -------------------------------------- |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp)          | Download engine supporting 1000+ sites |
| [ytmusicapi](https://github.com/sigma67/ytmusicapi) | YouTube Music search API               |
| [mutagen](https://github.com/quodlibet/mutagen)     | Metadata tagging for audio files       |

**Author:** [Fkernel653](https://github.com/Fkernel653)

**Project:** [GitHub](https://github.com/Fkernel653/fm-dlp-core) • [PyPI](https://pypi.org/project/fm-dlp-core)
