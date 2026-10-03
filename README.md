# fm-dlp-core — Core Library for YouTube & 1000+ Sites

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=fff&style=for-the-badge)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/fm-dlp-core?style=for-the-badge&logo=pypi&logoColor=fff&label=PyPI&color=007ec6)](https://pypi.org/project/fm-dlp-core)
[![License](https://img.shields.io/badge/License-AGPLv3-00b96b?style=for-the-badge&logo=gnu&logoColor=white)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-9cf?style=for-the-badge)](<>)
[![Ruff](https://img.shields.io/badge/Code%20Style-Ruff-ff69b4?logo=ruff&logoColor=fff&style=for-the-badge)](https://docs.astral.sh/ruff)

**fm-dlp-core** is a powerful Python library for searching and downloading content from YouTube, YouTube Music, and over 1000+ supported sites. Built on top of yt-dlp, it provides a clean, async-first API with rich features including concurrent downloads, metadata embedding, subtitle download/embedding, arbitrary yt-dlp args passthrough, and flexible output formatting.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Requirements](#requirements)
- [Core Concepts](#core-concepts)
  - [Async-First Design](#async-first-design)
  - [Configuration Persistence](#configuration-persistence)
  - [Provider Pattern](#provider-pattern)
  - [Layered yt-dlp Options](#layered-yt-dlp-options)
- [Downloading Content](#downloading-content)
  - [Overview](#overview)
  - [DownloadParams Class](#downloadparams-class)
  - [Download Parameters Reference](#download-parameters-reference)
  - [Supported Codecs](#supported-codecs)
  - [Executor Selection](#executor-selection)
- [Searching Content](#searching-content)
  - [Overview](#overview-1)
  - [Search Parameters](#search-parameters)
  - [Output Modes](#output-modes)
- [Configuration](#configuration)
  - [Config file location](#config-file-location)
  - [Custom config file](#custom-config-file)
  - [Usage](#usage)
  - [Low-level API](#low-level-api)
- [API Reference](#api-reference)
  - [Core Package](#core-package)
  - [Key Classes](#key-classes)
  - [Key Functions](#key-functions)
- [Download Output Examples](#download-output-examples)
- [Search Output Examples](#search-output-examples)
  - [Format Elements](#format-elements)
- [License & Acknowledgments](#license--acknowledgments)

---

## Quick Start

```python
import asyncio
from fm_dlp_core import Search, run_downloader
from fm_dlp_core.commands.downloader import DownloadParams

# 1. Search for a track
for result in Search("Sewerslvt", limit=3, yt_video=False, album=False).search():
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
            ffmpeg_path=None,
            config_file=None,
            only_video=False,
            cookies=None,
            remote=None,
            color=True,
            subtitles=False,
            subtitle_langs="en",
            embed_subs=False,
            auto_subs=False,
            ytdlp_args=None,
        )
    )
)
```

---

## Installation

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

## Requirements

- **Python 3.11+** - TOML support required
- **FFmpeg** - Required for audio/video processing and subtitle embedding. Install via:
  - **macOS:** `brew install ffmpeg`
  - **Linux:**
    - **Debian:** `sudo apt install ffmpeg`
    - **Fedora:** `sudo dnf install ffmpeg`
    - **Arch Linux:** `sudo pacman -S ffmpeg`
  - **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

  If FFmpeg is not on `PATH`, pass `ffmpeg_path` to `DownloadParams`.

---

## Core Concepts

### Async-First Design

All download operations are asynchronous, allowing you to run multiple downloads concurrently without blocking your application.

### Configuration Persistence

Settings like codec, bitrate, quality, subtitle preferences, FFmpeg path, and download path can be saved to a TOML file and reused across sessions. A custom config file can be supplied via `config_file`.

### Provider Pattern

Search functionality is built on a provider pattern, making it easy to add support for new platforms by subclassing `BaseProvider`.

### Layered yt-dlp Options

The `OptionsBuilder` assembles options in priority order:

1. Base options (output template, concurrency, retries, `ffmpeg_location`)
2. Color / cookies / remote configuration
3. Codec-specific options (audio extraction, video conversion)
4. Subtitle options (if `subtitles=True`)
5. **User-provided `ytdlp_args`** — merged last, highest priority (`postprocessors` are extended, not replaced)

---

## Downloading Content

### Overview

The download system supports:

- **Audio extraction** in 8 formats (MP3, AAC, FLAC, M4A, Opus, Vorbis, WAV, ALAC)
- **Video download** in MP4, MKV, WebM, MOV, AVI, FLV with quality selection
- **Batch downloads** from multiple URLs or text files
- **Concurrent downloads** with configurable job limits
- **Metadata embedding** with thumbnails
- **Subtitle download**, including **auto-generated** subtitles, and **embedding** into the video container
- **Custom FFmpeg location** via `ffmpeg_path`
- **Custom config file** via `config_file`
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
    ffmpeg_path=None,
    config_file=None,
    only_video=True,
    cookies="chrome",
    remote="github",
    color=True,
    subtitles=True,
    subtitle_langs="en,ru",
    embed_subs=True,
    auto_subs=False,
    ytdlp_args={
        "retries": 10,
        "fragment_retries": 10,
        "subtitlesformat": "srt/best",
        "postprocessors": [{"key": "FFmpegMetadata"}],
    },
)
```

### Download Parameters Reference

| Parameter        | Type                        | Description                                                                                                                                    |
| ---------------- | --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`            | `str`                       | URL(s) to download (comma/space separated or path to file)                                                                                     |
| `codec`          | `str`                       | Output format (see Supported Codecs)                                                                                                           |
| `kbps`           | `int`                       | Audio bitrate in kbps. Use `0` for lossless formats (FLAC, WAV, ALAC)                                                                          |
| `quality`        | `str`                       | Video quality: `"best"`, `"worst"`, `"1080"`, `"1080p"`, or custom format filter                                                               |
| `jobs`           | `int`                       | Number of concurrent downloads (also controls thread/process pool size)                                                                        |
| `quiet`          | `bool`                      | Suppress output messages                                                                                                                       |
| `metadata`       | `bool`                      | Embed metadata and thumbnail. **Note:** Automatically disabled for WAV format (not supported)                                                  |
| `keep`           | `bool`                      | Keep original downloaded file (video file when extracting audio)                                                                               |
| `save`           | `bool`                      | Save parameters to config                                                                                                                      |
| `use_config`     | `bool`                      | Load parameters from config. Saved values take priority over instance values                                                                   |
| `path`           | `str`                       | Download directory                                                                                                                             |
| `ffmpeg_path`    | `str \| None`               | Path to FFmpeg binary or directory containing `ffmpeg`/`ffprobe`. Passed to yt-dlp as `ffmpeg_location`. If `None`, yt-dlp searches `PATH`     |
| `config_file`    | `str \| None`               | Path to a custom TOML config file. Overrides the platform-specific default. Must end with `.toml`; otherwise the default is used               |
| `only_video`     | `bool`                      | Download video only (skip audio extraction). Uses `ProcessPoolExecutor` for video processing                                                   |
| `cookies`        | `str \| None`               | Cookies file path or browser name (`"chrome"`, `"firefox"`, `"edge"`, `"opera"`). Uses cookiefile if path exists, otherwise cookiesfrombrowser |
| `remote`         | `str \| None`               | External JavaScript components source for bypassing anti-bot protections. Valid values: `"github"` (yt-dlp repo) or `"npm"` (NPM registry)     |
| `color`          | `bool`                      | Enable colored output                                                                                                                          |
| `subtitles`      | `bool`                      | Download subtitles (`writesubtitles`). Requires FFmpeg for embedding                                                                           |
| `subtitle_langs` | `str \| None`               | Comma-separated subtitle language codes, e.g. `"en,ru,ja"` → `subtitleslangs`                                                                  |
| `embed_subs`     | `bool`                      | Embed subtitles into the video container (`FFmpegEmbedSubtitle`). Only for video containers (mp4, mkv, webm, mov)                              |
| `auto_subs`      | `bool`                      | Include auto-generated subtitles (`writeautomaticsub`)                                                                                         |
| `ytdlp_args`     | `dict[str, object] \| None` | Extra raw yt-dlp options (snake_case). Merged last; `postprocessors` are **extended**, other keys **override**                                 |

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

## Searching Content

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
<summary><b>Click for examples</b></summary>

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
    query="Psychology",
    limit=5,
    yt_video=True,  # Use YouTube (videos)
    album=False,
).search():
    print(result)
```

---

**URL-Only Output**

```python
import asyncio
from fm_dlp_core import Search, run_downloader
from fm_dlp_core.commands.downloader import DownloadParams

# Get only URLs
urls = list(Search("breakcore", limit=10, only_url=True).search())

# Chain search → download
urls = list(Search("chill beats", limit=5, only_url=True).search())
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
                ffmpeg_path=None,
                config_file=None,
                only_video=False,
                cookies=None,
                remote=None,
                color=True,
                subtitles=False,
                subtitle_langs=None,
                embed_subs=False,
                auto_subs=False,
                ytdlp_args=None,
            )
        )
    )
```

</details>

---

## Configuration

Download settings can be persisted to a TOML file and reused across sessions. This covers codec, bitrate, quality, jobs, metadata/keep flags, cookies, remote, subtitles, raw yt-dlp args, FFmpeg path, and the default download directory.

### Config file location

| Platform    | Path                                               |
| ----------- | -------------------------------------------------- |
| **Windows** | `%LOCALAPPDATA%\fm-dlp\config.toml`                |
| **macOS**   | `~/Library/Application Support/fm-dlp/config.toml` |
| **Linux**   | `~/.config/fm-dlp/config.toml`                     |

### Custom config file

Pass `config_file` to `DownloadParams` to use a custom TOML file instead of the platform-specific default:

```python
DownloadParams(
    url="...",
    # ...
    config_file="/path/to/my-config.toml",
)
```

Rules:

- `config_file` must end with `.toml`. Otherwise, a warning is shown and the default config file is used.
- Both `save=True` and `use_config=True` respect `config_file`.
- Tilde (`~`) is expanded to the user's home directory.
- `config_file` is optional; when `None`, the platform-specific default is used.

### Usage

Save parameters with `save=True`, load them back with `use_config=True`.

```python
import asyncio
from fm_dlp_core import run_downloader
from fm_dlp_core.commands.downloader import DownloadParams

# Save current parameters (URL is not persisted)
asyncio.run(
    run_downloader(
        DownloadParams(
            url="https://youtube.com/watch?v=...",
            codec="flac", kbps=0, quality="best", jobs=4,
            quiet=False, metadata=True, keep=False,
            save=True, use_config=False,
            path="./music", ffmpeg_path=None, config_file=None,
            only_video=False, cookies=None, remote=None, color=True,
            subtitles=True, subtitle_langs="en,ru",
            embed_subs=True, auto_subs=False, ytdlp_args=None,
        )
    )
)

# Load saved parameters on the next run
asyncio.run(
    run_downloader(
        DownloadParams(
            url="https://youtube.com/watch?v=...",
            # any values here are overridden by the saved config
            codec="mp3", kbps=0, quality="best", jobs=1,
            quiet=False, metadata=True, keep=False,
            save=False, use_config=True,
            path="./downloads", ffmpeg_path=None, config_file=None,
            only_video=False, cookies=None, remote=None, color=True,
            subtitles=False, subtitle_langs=None,
            embed_subs=False, auto_subs=False, ytdlp_args=None,
        )
    )
)
```

Using a custom config file for both save and load:

```python
# Save to a custom config file
DownloadParams(
    url="...",
    # ...
    save=True,
    config_file="~/.config/my-fm-dlp/music.toml",
)

# Load from the same custom config file
DownloadParams(
    url="...",
    # ...
    use_config=True,
    config_file="~/.config/my-fm-dlp/music.toml",
)
```

### Low-level API

For direct file manipulation, use `ConfigManager`, `ParametersManager`, and `PathManager` from `fm_dlp_core.utils.config`. All three accept a `ConfigParams` instance that carries `quiet`, `color`, and `config_file`.

```python
from fm_dlp_core.utils.config import ConfigManager, ConfigParams

params = ConfigParams(color=True, config_file=None)
manager = ConfigManager(params)
config = manager.load_config()
manager.update_config(config)
```

---

## API Reference

### Core Package

| Module                                    | Description                                                 |
| ----------------------------------------- | ----------------------------------------------------------- |
| `fm_dlp_core`                             | Main package with `Download`, `Search`, and utilities       |
| `fm_dlp_core.commands.downloader`         | Download functionality with `Download` and `run_downloader` |
| `fm_dlp_core.commands.search`             | Search functionality with `Search`                          |
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
| `ConfigParams`         | `utils.config.params`                 | Shared config parameters              |
| `TOMLSerializer`       | `utils.config.config_manager`         | Serialize Python dicts to TOML        |
| `ParametersManager`    | `utils.config.parametrs`              | Manage `[parameters]` section         |
| `PathManager`          | `utils.config.path`                   | Manage download path                  |

### Key Functions

| Function                  | Module                | Description                |
| ------------------------- | --------------------- | -------------------------- |
| `run_downloader`          | `commands.downloader` | Async download entry point |
| `echo`                    | `utils`               | Print with color support   |
| `success/error/info/hint` | `utils.colors`        | Formatted colored messages |

---

## Download Output Examples

<details>
<summary>Example Output</summary>

```text

Starting: https://music.youtube.com/watch?v=DVDiOMoW0wU
[youtube] Extracting URL: https://music.youtube.com/watch?v=DVDiOMoW0wU
[youtube] DVDiOMoW0wU: Downloading webpage
[youtube] DVDiOMoW0wU: Downloading visionos player API JSON
[youtube] DVDiOMoW0wU: Downloading m3u8 information
[info] DVDiOMoW0wU: Downloading 1 format(s): 251
[info] There are no subtitles for the requested languages
[info] Downloading video thumbnail 41 ...
[info] Writing video thumbnail 41 to: /home/kernel/Music/A Dream.webp
[download] Destination: /home/kernel/Music/A Dream.webm
[download] 100% of 2.55MiB in 00:00:00 at 2.73MiB/s
[ExtractAudio] Destination: /home/kernel/Music/A Dream.opus
Deleting original file /home/kernel/Music/A Dream.webm (pass -k to keep)
[Metadata] Adding metadata to "/home/kernel/Music/A Dream.opus"
[ThumbnailsConvertor] Converting thumbnail "/home/kernel/Music/A Dream.webp" to png
[EmbedThumbnail] mutagen: Adding thumbnail to "/home/kernel/Music/A Dream.opus"

Success: https://music.youtube.com/watch?v=DVDiOMoW0wU

```

And the corresponding Python call:

```python
asyncio.run(
    run_downloader(
        DownloadParams(
            url="https://music.youtube.com/watch?v=DVDiOMoW0wU",
            codec="opus",
            kbps=256,
            quality="best",
            jobs=1,
            quiet=False,
            metadata=True,
            keep=False,
            save=False,
            use_config=False,
            path="/home/kernel/Music",
            ffmpeg_path=None,
            config_file=None,
            only_video=False,
            cookies=None,
            remote=None,
            subtitles=False,
            subtitle_langs=None,
            embed_subs=False,
            auto_subs=False,
            color=False,
            ytdlp_args=None,
        )
    )
)
```

</details>

---

## Search Output Examples

Examples of formatting search results from different sources. Click each example to expand.

<details>
<summary>YTMusic (Track)</summary>

```

    1. A Dream
        ├─ Flatsound
        ├─ Somewhere in the Distance, Somewhere Toward the Mountains
        ├─ 4M │ 2:51
        └─ https://music.youtube.com/watch?v=DVDiOMoW0wU
          ──────────────────────────────────────────────────

    N. Title
        ├─ Artist
        ├─ Album
        ├─ Views │ Duration
        └─ URL
           ──────────────────────────────────────────────────

```

</details>

<details>
<summary>YTMusic (Album)</summary>

```

    1. Skitzofrenia Simulation
        ├─ Sewerslvt
        ├─ 2021
        └─ https://music.youtube.com/playlist?list=OLAK5uy_kXLBb5YlVizbrgXAHwTgarL5HYC3usuYA
          ──────────────────────────────────────────────────

    N. Title
        ├─ Artist
        ├─ Year
        └─ URL
           ──────────────────────────────────────────────────

```

</details>

<details>
<summary>YouTube (Video)</summary>

```

    1. Silence , I'm Dying.
        ├─ Willix
        ├─ 587,740 │ 2:05
        └─ https://youtu.be/oSOaz5yaBM8
          ──────────────────────────────────────────────────

    N. Title
        ├─ Artist
        ├─ Views │ Duration
        └─ URL
           ──────────────────────────────────────────────────

```

</details>

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

## License & Acknowledgments

[AGPLv3 License](LICENSE) — Built with:

| Library                                             | Purpose                                |
| --------------------------------------------------- | -------------------------------------- |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp)          | Download engine supporting 1000+ sites |
| [ytmusicapi](https://github.com/sigma67/ytmusicapi) | YouTube Music search API               |
| [mutagen](https://github.com/quodlibet/mutagen)     | Metadata tagging for audio files       |

**Author:** [Fkernel653](https://github.com/Fkernel653)

**Project:** [GitHub](https://github.com/Fkernel653/fm-dlp-core) • [PyPI](https://pypi.org/project/fm-dlp-core)
