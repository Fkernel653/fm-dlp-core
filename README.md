# fm-dlp-core — Main core by fm-dlp

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/fm-dlp-core.svg)](https://pypi.org/project/fm-dlp-core)
[![License](https://img.shields.io/badge/license-GPLv3-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-lightgrey)]()
[![Ruff](https://img.shields.io/badge/code%20style-ruff-261230?logo=ruff&logoColor=white)](https://docs.astral.sh/ruff)

Core containing utilities for searching from Youtube/YTMusic and downloading audio/video from [1000+ sites](https://github.com/yt-dlp/yt-dlp/supportedsites.md)

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

The `Download` class provides async audio/video downloading capabilities.

#### Basic Usage

```python
import asyncio
from fm_dlp_core.commands.downloader import Download, run_downloader

# Using the convenience function
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

asyncio.run(main())
```

#### Advanced Usage with Context Manager

```python
import asyncio
from fm_dlp_core.commands.downloader import Download

async def main():
    async with Download(
        url="https://www.youtube.com/watch?v=example",
        codec="mp3",
        kbps=320,
        quality="1080p",
        jobs=2,
        quiet=True,
        metadata=True,
        keep=True,
        save=False,
        use_config=False,
        path="./downloads",
        only_video=False,
        cookies="chrome",
        color=True,
    ) as downloader:
        await downloader.download_all()

asyncio.run(main())
```

#### Download Multiple URLs

You can provide multiple URLs separated by commas, spaces, or from a file:

```python
# Comma-separated URLs
url = "url1,url2,url3"

# Space-separated URLs
url = "url1 url2 url3"

# File containing URLs (one per line)
url = "urls.txt"
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | `str` | URL(s) to download (comma/space separated or path to file) |
| `codec` | `str` | Audio codec or video container (`mp3`, `aac`, `flac`, `opus`, `mp4`, `mkv`, etc.) |
| `kbps` | `int` | Audio bitrate in kbps (e.g., 128, 192, 320) |
| `quality` | `str` | Video quality (`best`, `worst`, `1080p`, `720p`, etc.) |
| `jobs` | `int` | Maximum concurrent downloads |
| `quiet` | `bool` | Suppress output messages |
| `metadata` | `bool` | Embed metadata and thumbnail |
| `keep` | `bool` | Keep original downloaded file after conversion |
| `save` | `bool` | Save parameters to config file |
| `use_config` | `bool` | Load parameters from config file |
| `path` | `str` | Download directory path |
| `only_video` | `bool` | Download video only (no audio extraction) |
| `cookies` | `str\|None` | Path to cookies file or browser name (`chrome`, `firefox`, etc.) |
| `color` | `bool` | Enable colored output |
| `encoding` | `str` | File encoding (default: utf-8) |

---

### 🔍 Search

The `Search` class provides search functionality for YouTube and YouTube Music.

#### Basic Usage

```python
from fm_dlp_core.commands.search import search

# Search YouTube Music for tracks
for result in search(
    query="Imagine Dragons",
    limit=5,
    yt_video=False,      # Search YouTube Music
    album=False,          # Search for tracks (not albums)
    raw=False,            # Formatted output
    only_url=False,       # Show full details
    color=True,
):
    print(result)
```

#### Search YouTube Videos

```python
# Search YouTube for videos
for result in search(
    query="Python tutorial",
    limit=3,
    yt_video=True,        # Search YouTube videos
    album=False,
    raw=False,
    only_url=False,
    color=True,
):
    print(result)
```

#### Get Only URLs

```python
# Get only URLs for batch processing
urls = []
for url in search(
    query="lofi hip hop",
    limit=10,
    yt_video=False,
    album=False,
    raw=False,
    only_url=True,        # Return only URLs
    color=False,
):
    urls.append(url)
```

#### Raw JSON Output

```python
# Get raw dictionary data
for entry in search(
    query="Taylor Swift",
    limit=2,
    yt_video=False,
    album=False,
    raw=True,             # Raw Python dicts
    only_url=False,
    color=False,
):
    print(entry)  # Prints dict representation
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | Search query string |
| `limit` | `int` | Maximum number of results |
| `yt_video` | `bool` | Search YouTube videos (False = YouTube Music) |
| `album` | `bool` | Search for albums (False = tracks) |
| `raw` | `bool` | Output raw Python dicts instead of formatted strings |
| `only_url` | `bool` | Output only URLs without formatting |
| `color` | `bool` | Enable colored output |

---

### ⚙️ Configuration

The `config` module provides persistent storage for download parameters and path settings.

#### Saving Parameters

```python
from fm_dlp_core.utils.config.parametrs import set_parameters

set_parameters(
    codec="mp3",
    kbps=192,
    quality="720p",
    jobs=4,
    quiet=False,
    metadata=True,
    keep=False,
    only_video=False,
    cookies=None,
    color=True,
)
```

#### Loading Parameters

```python
from fm_dlp_core.utils.config.parametrs import get_parameters

params = get_parameters(color=True)
print(params)
# {'codec': 'mp3', 'kbps': 192, 'quality': '720p', ...}
```

#### Setting Download Path

```python
from fm_dlp_core.utils.config.path import set_path, get_path

# Set and save download path
set_path("./my_downloads", color=True)

# Get current download path
path = get_path(color=True)
print(f"Downloading to: {path}")
```

---

### 🎨 Output Formatting

The `colors` module provides styled output functions.

```python
from fm_dlp_core.utils import echo
from fm_dlp_core.utils.colors import success, error, info, hint, set_colors

# Enable/disable colors
set_colors(True)  # Enable colors
set_colors(False) # Disable colors

# Formatted messages
echo(success("Download completed!"))
echo(error("Failed to download"))
echo(info("Processing file..."))
echo(hint("Use --help for more options"))

# Custom styled text
from fm_dlp_core.utils.colors import styled, BOLD_CYAN
echo(styled("Custom message", BOLD_CYAN))
```

---

### 📋 Supported Codecs

#### Audio Codecs
- `mp3`, `aac`, `flac`, `m4a`, `opus`, `vorbis`, `wav`, `alac`

#### Video Containers
- `mp4`, `mov`, `mkv`, `webm`, `avi`, `flv`

```python
from fm_dlp_core.utils import ALL_CODECS, AUDIO_CODECS, VIDEO_CONTAINERS

print(f"All codecs: {ALL_CODECS}")
print(f"Audio codecs: {AUDIO_CODECS}")
print(f"Video containers: {VIDEO_CONTAINERS}")
```

---

## 💡 Examples

### Download YouTube Video as MP4

```python
import asyncio
from fm_dlp_core.commands.downloader import run_downloader

asyncio.run(run_downloader(
    url="https://www.youtube.com/watch?v=video_id",
    codec="mp4",
    kbps=0,  # Not used for video
    quality="1080p",
    jobs=1,
    quiet=False,
    metadata=False,
    keep=False,
    save=False,
    use_config=False,
    path="./videos",
    only_video=True,
    cookies=None,
    color=True,
))
```

### Batch Download Audio with Metadata

```python
import asyncio
from fm_dlp_core.commands.downloader import Download

async def batch_download():
    urls = [
        "https://music.youtube.com/watch?v=id1",
        "https://music.youtube.com/watch?v=id2",
        "https://music.youtube.com/watch?v=id3",
    ]
    
    async with Download(
        url=",".join(urls),
        codec="flac",
        kbps=0,  # Lossless
        quality="best",
        jobs=3,
        quiet=False,
        metadata=True,
        keep=False,
        save=False,
        use_config=False,
        path="./music",
        only_video=False,
        cookies=None,
        color=True,
    ) as downloader:
        await downloader.download_all()

asyncio.run(batch_download())
```

### Search and Download Automation

```python
import asyncio
from fm_dlp_core.commands.search import search
from fm_dlp_core.commands.downloader import Download

async def search_and_download():
    # Search for tracks
    urls = []
    for result in search(
        query="chill beats",
        limit=5,
        yt_video=False,
        album=False,
        raw=False,
        only_url=True,
        color=True,
    ):
        urls.append(result)
    
    if urls:
        # Download found tracks
        async with Download(
            url=" ".join(urls),
            codec="mp3",
            kbps=320,
            quality="best",
            jobs=3,
            quiet=False,
            metadata=True,
            keep=False,
            save=False,
            use_config=False,
            path="./downloads",
            only_video=False,
            cookies=None,
            color=True,
        ) as downloader:
            await downloader.download_all()

asyncio.run(search_and_download())
```

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
