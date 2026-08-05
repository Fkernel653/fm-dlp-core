"""YouTube search handlers."""

from ...utils.colors import set_colors
from .formatters import ResultFormatter
from .providers import Generator, YouTubeMusicProvider, YouTubeProvider


class Search:
    """Handles searching across YouTube and YouTube Music."""

    def __init__(
        self,
        query: str,
        limit: int,
        yt_video: bool,
        album: bool,
        raw: bool,
        only_url: bool,
        color: bool,
    ):
        """Initialize search with query parameters.

        Args:
            query: Search query string.
            limit: Maximum number of results.
            yt_video: Search YouTube videos instead of YouTube Music.
            album: Search for albums instead of tracks.
            raw: Output raw Python dicts instead of formatted strings.
            only_url: Output only URLs without formatting.
            color: Colored output.
        """
        self.query = query
        self.limit = limit
        self.yt_video = yt_video
        self.raw = raw
        self.only_url = only_url
        self.is_track = not album

        set_colors(color)

        self.error_prefix = "Search Error: "
        self.formatter = ResultFormatter(color, self.error_prefix)
        self.yt_provider = YouTubeProvider(color, self.error_prefix, self.formatter)
        self.ytm_provider = YouTubeMusicProvider(
            color, self.error_prefix, self.formatter
        )

    def search(self) -> Generator[str, None, None] | str:
        """Perform search using appropriate provider."""
        if self.yt_video:
            try:
                yield from self.yt_provider.search(
                    self.query,
                    self.limit,
                    self.is_track,
                    self.raw,
                    self.only_url,
                )
            except Exception:
                return ""
        else:
            from requests.exceptions import ReadTimeout
            from urllib3.exceptions import ReadTimeoutError

            try:
                yield from self.ytm_provider.search(
                    self.query,
                    self.limit,
                    self.is_track,
                    self.raw,
                    self.only_url,
                )
            except (
                ReadTimeoutError,
                ReadTimeout,
                TimeoutError,
            ):
                yield self.formatter.fmt_error("Connection timeout")
            except Exception as e:
                yield self.formatter.fmt_error(str(e))


def search(
    query: str,
    limit: int,
    yt_video: bool,
    album: bool,
    raw: bool,
    only_url: bool,
    color: bool,
) -> Generator[str, None, None] | str:
    """Search YouTube or YouTube Music."""
    s = Search(query, limit, yt_video, album, raw, only_url, color)
    return s.search()
