"""Main downloader class."""

import asyncio
from collections.abc import AsyncIterator
from types import TracebackType
from typing import final

from ...utils import VIDEO_CONTAINERS, echo
from ...utils.colors import BOLD_YELLOW, info, set_colors, styled, success
from .. import get_ytdlp
from .config import DownloadConfig
from .options_builder import OptionsBuilder
from .params import DownloadParams
from .url_parser import URLParser


@final
class Download:
    """Async YouTube audio/video downloader."""

    def __init__(self, params: DownloadParams):
        """Initialize downloader with configuration."""
        self.params = params
        self.config = DownloadConfig(params)

        applied = self.config.apply_config()

        self.codec: str = applied["codec"]
        self.kbps: int = applied["kbps"]
        self.quality: str = applied["quality"]
        self.jobs: int = applied["jobs"]
        self.quiet: bool = applied["quiet"]
        self.metadata: bool = applied["metadata"]
        self.keep: bool = applied["keep"]
        self.only_video: bool = applied["only_video"]
        self.cookies: str = applied["cookies"]
        self.remote: str = applied["remote"]

        if not self.config.save_config():
            return

        self._executor = self._get_executor()
        self._url_list = URLParser(params.url, params.quiet).parse()

        set_colors(params.color)

    def _get_executor(self):
        """
        Select the appropriate executor type based on the download task.

        Returns a ProcessPoolExecutor for video downloads or container formats
        (which benefit from CPU parallelism for transcoding), and a ThreadPoolExecutor
        for audio downloads (which are typically I/O-bound and work better with
        threading). The number of workers is determined by the `jobs` parameter.

        Returns:
            ProcessPoolExecutor | ThreadPoolExecutor: An executor instance suitable
                for the current download task type.
        """
        from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

        if self.only_video or self.codec in VIDEO_CONTAINERS:
            return ProcessPoolExecutor(max_workers=self.jobs)
        else:
            return ThreadPoolExecutor(max_workers=self.jobs)

    async def __aenter__(self):
        """Enter the async context manager and return the downloader instance."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ):
        """Cleanup thread pool executor on context exit."""
        self._executor.shutdown(wait=True, cancel_futures=False)
        return False

    def __aiter__(self):
        """Return async iterator for download results."""
        return self._aiter()

    async def _aiter(self) -> AsyncIterator[str | None]:
        """Async iterator yielding download results with concurrency control."""
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
        """
        Download a single URL asynchronously and return a status message.

        This method handles the complete download process for a single URL,
        including:
        - Disabling metadata embedding for WAV format (not supported)
        - Logging progress information if not in quiet mode
        - Offloading the synchronous yt-dlp download to a thread/process pool

        Args:
            url (str): The YouTube URL to download.

        Returns:
            str | None: A formatted success message if not in quiet mode,
                otherwise None. Returns None if the download fails or is quiet.
        """
        if self.codec == "wav" and self.metadata:
            self.metadata = False
            if not self.quiet:
                echo(info("WAV format doesn't support metadata embedding"))

        if not self.quiet:
            echo("\n" + styled("Starting: ", BOLD_YELLOW) + url)

        await asyncio.to_thread(self._sync_download, url)

        return f"\n{success(url)}\n" if not self.quiet else None

    def _sync_download(self, url: str) -> None:
        """Synchronous download using yt-dlp (runs in thread pool)."""
        options = OptionsBuilder(self.params).build()

        YoutubeDL = get_ytdlp()
        with YoutubeDL(options) as ydl:
            _ = ydl.download([url])


async def run_downloader(
    url: str,
    codec: str,
    kbps: int,
    quality: str,
    jobs: int,
    quiet: bool,
    metadata: bool,
    keep: bool,
    save: bool,
    use_config: bool,
    path: str,
    only_video: bool,
    cookies: str | None,
    remote: str,
    color: bool,
) -> None:
    """Run downloader with given parameters."""

    params = DownloadParams(
        url=url,
        codec=codec,
        kbps=kbps,
        quality=quality,
        jobs=jobs,
        quiet=quiet,
        metadata=metadata,
        keep=keep,
        save=save,
        use_config=use_config,
        path=path,
        only_video=only_video,
        cookies=cookies,
        remote=remote,
        color=color,
    )

    async with Download(params) as dl:
        try:
            await dl.download_all()
        except Exception:
            ...
