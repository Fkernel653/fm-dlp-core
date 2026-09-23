import asyncio

from ...utils import (
    BOLD_YELLOW,
    VIDEO_CONTAINERS,
    echo,
    info,
    set_colors,
    styled,
    success,
)
from .config import DownloadConfig
from .options_builder import OptionsBuilder
from .params import DownloadParams
from .url_parser import URLParser


class Download:
    """
    Async YouTube audio/video downloader built on top of yt-dlp.

    This class encapsulates the full download lifecycle: URL parsing,
    configuration resolution (including user-defined config), executor
    selection, concurrent task execution, and lazy loading of heavy
    dependencies (yt-dlp).

    Key features:
        - Supports both audio and video formats. For video and container
          formats, a ProcessPoolExecutor is used (transcoding is CPU-bound),
          while audio downloads use a ThreadPoolExecutor (tasks are mostly
          I/O-bound).
        - Concurrency is throttled by the `jobs` parameter via an
          asyncio.Semaphore, preventing system overload.
        - Download results are exposed as an async iterator (`__aiter__`),
          allowing results to be consumed as they complete.
        - Can be used as an async context manager: on exit, the executor
          pool is gracefully shut down.
        - Supports subtitle download/embedding and arbitrary yt-dlp args.

    Args:
        params (DownloadParams): Download parameters including URL, codec,
            quality, number of jobs, metadata/quiet/keep flags, save path,
            cookies, remote storage, subtitles, and raw yt-dlp args.

    Attributes:
        params (DownloadParams): The original download parameters.
        config (DownloadConfig): Configuration derived from the parameters.
        codec (str): Selected audio/video codec.
        kbps (int): Audio bitrate in kbps.
        quality (str): Desired video quality.
        jobs (int): Maximum number of concurrent downloads.
        quiet (bool): Suppresses progress output when True.
        metadata (bool): Whether to embed metadata into the output file.
        keep (bool): Whether to keep intermediate files.
        only_video (bool): Download video only (no audio).
        cookies (str | None): Path to a cookies file, or None.
        remote (str): Name of the remote storage target (if used).
        subtitles (bool): Whether subtitles should be downloaded.
        subtitle_langs (str): Comma-separated subtitle language codes.
        embed_subs (bool): Whether to embed subtitles into the container.
        auto_subs (bool): Whether to include auto-generated subtitles.
        ytdlp_args (dict[str, Any] | None): Extra raw yt-dlp options.

    Example:
        >>> params = DownloadParams(url="https://youtu.be/...", codec="mp3", ...)
        >>> async with Download(params) as dl:
        ...     async for result in dl:
        ...         print(result)
        ...     # or
        ...     await dl.download_all()
    """

    def __init__(self, params: DownloadParams):
        self.params = params
        self.config = DownloadConfig(params)

        conf = self.config.apply_config()

        self.codec = conf["codec"]
        self.kbps = conf["kbps"]
        self.quality = conf["quality"]
        self.jobs = conf["jobs"]
        self.quiet = conf["quiet"]
        self.metadata = conf["metadata"]
        self.keep = conf["keep"]
        self.only_video = conf["only_video"]
        self.cookies = conf["cookies"]
        self.remote = conf["remote"]
        self.subtitles = conf["subtitles"]
        self.subtitle_langs = conf["subtitle_langs"]
        self.embed_subs = conf["embed_subs"]
        self.auto_subs = conf["auto_subs"]
        self.ytdlp_args = conf["ytdlp_args"]

        if not self.config.save_config():
            return

        self._executor = self._get_executor()
        self._url_list = URLParser(params.url, params.quiet).parse()

        set_colors(params.color)

        self._YoutubeDL = None

    def _get_executor(self):
        from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

        if self.only_video or self.codec in VIDEO_CONTAINERS:
            return ProcessPoolExecutor(max_workers=self.jobs)
        else:
            return ThreadPoolExecutor(max_workers=self.jobs)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._executor.shutdown(wait=True, cancel_futures=False)
        return False

    def __aiter__(self):
        return self._aiter()

    async def _aiter(self):
        sem = asyncio.Semaphore(self.jobs)

        async def download_one(url: str):
            async with sem:
                return await self._download_url(url)

        tasks = [asyncio.create_task(download_one(u)) for u in self._url_list]
        for task in asyncio.as_completed(tasks):
            yield await task

    async def download_all(self) -> None:
        """Download all URLs and echo results as they complete."""
        if not self._url_list:
            return
        async for result in self:
            if result is not None:
                echo(result)

    async def _download_url(self, url: str) -> str | None:
        if self.codec == "wav" and self.metadata:
            self.metadata = False
            if not self.quiet:
                echo(info("WAV format doesn't support metadata embedding"))

        if not self.quiet:
            echo("\n" + styled("Starting: ", BOLD_YELLOW) + url)

        await asyncio.to_thread(self._sync_download, url)

        return f"\n{success(url)}\n" if not self.quiet else None

    def _get_ytdlp(self):
        if self._YoutubeDL is None:
            from yt_dlp import YoutubeDL

            self._YoutubeDL = YoutubeDL
        return self._YoutubeDL

    def _sync_download(self, url: str) -> None:
        """Synchronous download using yt-dlp (runs in thread pool)."""
        options = OptionsBuilder(self.params).build()

        YoutubeDL = self._get_ytdlp()
        with YoutubeDL(options) as ydl:
            _ = ydl.download([url])


async def run_downloader(params: DownloadParams) -> None:
    """Run downloader with given parameters."""
    async with Download(params) as dl:
        try:
            await dl.download_all()
        except Exception:
            ...
