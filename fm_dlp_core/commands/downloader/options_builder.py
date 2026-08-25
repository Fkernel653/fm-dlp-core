"""Build yt-dlp options."""

from pathlib import Path
from typing import Any, final

from ...utils import AUDIO_CODECS, VIDEO_CONTAINER_AUDIO_MAP, VIDEO_CONTAINERS


@final
class OptionsBuilder:
    """Build yt-dlp options dictionary."""

    def __init__(
        self,
        codec: str,
        kbps: int,
        quality: str,
        jobs: int,
        quiet: bool,
        metadata: bool,
        keep: bool,
        only_video: bool,
        cookies: str | None,
        path: str,
        color: bool,
    ):
        self.codec = codec
        self.kbps = kbps
        self.quality = quality
        self.jobs = jobs
        self.quiet = quiet
        self.metadata = metadata
        self.keep = keep
        self.only_video = only_video
        self.cookies = cookies
        self.path = path
        self.color = color

    def _parse_quality(self) -> str:
        """
        Parse the quality string into a yt-dlp format filter expression.

        Supports the following formats:
        - "best" → returns "bestvideo" (highest available video quality)
        - "worst" → returns "worstvideo" (lowest available video quality)
        - Numeric height (e.g., "1080") → selects best video with height ≤ that value
        - Height with "p" suffix (e.g., "1080p") → same as numeric (strips "p")
        - Any other string → returned as-is (treated as custom format filter)

        Returns:
            str: A format filter string compatible with yt-dlp's --format option.
        """
        if self.quality == "best":
            return "bestvideo"
        if self.quality == "worst":
            return "worstvideo"

        if self.quality.isdigit():
            height = self.quality
            return f"bestvideo[height<={height}]"

        elif self.quality.endswith("p") and self.quality[:-1].isdigit():
            height = self.quality[:-1]
            return f"bestvideo[height<={height}]"

        return self.quality

    def build(self) -> dict[str, Any]:
        """
        Build a complete yt-dlp options dictionary for the download.

        Constructs the full set of options for yt-dlp by:
        1. Setting base options (output template, concurrent downloads, retries)
        2. Configuring color output based on the `color` flag
        3. Adding cookie handling (from file or browser) if provided
        4. Delegating to specialized builders for video-only or audio download
           configurations with appropriate codec conversions and post-processors

        Returns:
            dict[str, Any]: A complete yt-dlp options dictionary ready to be passed
                to the YoutubeDL constructor.
        """
        base_opts: dict[str, Any] = {
            "quiet": self.quiet,
            "no_warnings": self.quiet,
            "outtmpl": str(Path(self.path) / "%(title)s.%(ext)s"),
            "concurrent_downloads": self.jobs,
            "concurrent_fragment_downloads": self.jobs,
            "extractor_retries": 3,
            "postprocessors": [],
            "keepvideo": self.keep,
        }

        if not self.color:
            base_opts["color"] = "never"

        self._add_cookies(base_opts)

        if self.only_video:
            self._build_video_opts(base_opts)
        else:
            self._build_audio_opts(base_opts)

        return base_opts

    def _add_cookies(self, opts: dict[str, Any]) -> None:
        """Add cookie configuration to options."""
        if self.cookies:
            cookie_path = Path(self.cookies)
            if cookie_path.is_file():
                opts["cookiefile"] = str(cookie_path)
            else:
                opts["cookiesfrombrowser"] = (self.cookies,)

    def _build_video_opts(self, opts: dict[str, Any]) -> None:
        """Build options for video-only download."""
        opts["format"] = self._parse_quality()

        if self.codec in VIDEO_CONTAINERS:
            opts["postprocessors"].append(
                {
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": self.codec,
                }
            )

    def _build_audio_opts(self, opts: dict[str, Any]) -> None:
        """Build options for audio download."""

        if self.codec in AUDIO_CODECS:
            self._build_audio_only_opts(opts)
        elif self.codec in VIDEO_CONTAINERS:
            self._build_video_with_audio_opts(opts)

    def _build_audio_only_opts(self, opts: dict[str, Any]) -> None:
        """Build options for audio-only download."""
        opts["format"] = "bestaudio/best"
        opts["postprocessors"].append(
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": self.codec,
                "preferredquality": str(self.kbps),
            }
        )

        if self.metadata:
            opts["postprocessors"].extend(
                [
                    {"key": "FFmpegMetadata"},
                    {"key": "EmbedThumbnail"},
                ]
            )
            opts["embedmetadata"] = True
            opts["writethumbnail"] = True

    def _build_video_with_audio_opts(self, opts: dict[str, Any]) -> None:
        """Build options for video download with audio."""
        audio_ext = VIDEO_CONTAINER_AUDIO_MAP[self.codec]

        opts["format"] = f"{self._parse_quality()}+bestaudio[ext={audio_ext}]/best"

        opts["postprocessors"].append(
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": self.codec,
            }
        )
