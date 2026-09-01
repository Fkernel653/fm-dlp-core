"""Search providers for YouTube and YouTube Music."""

from abc import ABC, abstractmethod
from collections.abc import Generator
from itertools import islice
from typing import Any, override

from .formatters import ResultFormatter


class BaseProvider(ABC):
    """
    Abstract base class for search providers (YouTube and YouTube Music).

    Provides a generic search workflow with template methods that concrete
    providers must implement:
    1. Search extraction via `_extract_results`
    2. Entry formatting via `_fmt_entry`
    3. URL extraction via `_extract_url`
    4. Empty result handling via `_get_empty_message`

    The `search` method orchestrates the common flow: fetch results, filter
    invalid entries, and yield formatted output or raw data based on flags.
    """

    formatter: ResultFormatter

    def __init__(
        self, color: bool, error_prefix: str, formatter: ResultFormatter | None = None
    ):
        self.formatter = formatter or ResultFormatter(color, error_prefix)

    @abstractmethod
    def _extract_results(self, query: str, limit: int, is_track: bool) -> list[Any]:
        """Extract search results from provider."""

    @abstractmethod
    def _fmt_entry(self, entry: dict[str, Any], num: int, is_track: bool) -> str | None:
        """Format a single search entry."""

    @abstractmethod
    def _extract_url(self, entry: dict[str, Any], is_track: bool) -> str | None:
        """Extract URL from search entry."""

    @abstractmethod
    def _get_empty_message(self, query: str, is_track: bool) -> str:
        """Get message when no results found."""

    def search(
        self,
        query: str,
        limit: int,
        is_track: bool,
        raw: bool,
        only_url: bool,
    ) -> Generator[str, None, None]:
        """
        Generic search method that handles common logic across providers.

        Orchestrates the complete search workflow:
        1. Calls `_extract_results` to fetch entries from the provider
        2. If no results → yields an empty message and returns
        3. If `raw` is True → yields string representations of entries
        4. Otherwise, iterates through entries up to `limit`:
            - Extracts URL via `_extract_url`
            - Skips entries without a URL
            - If `only_url` → yields the URL directly
            - Otherwise → formats the entry via `_fmt_entry`
        5. Stops early if no more results

        Args:
            query (str): Search query string.
            limit (int): Maximum number of results to return.
            is_track (bool): True for tracks/videos, False for albums/playlists.
            raw (bool): If True, yield raw dictionary representations.
            only_url (bool): If True, yield only URLs without formatting.

        Yields:
            str: Formatted results, URLs, raw data, or empty messages.
        """
        results = self._extract_results(query, limit, is_track)

        if not results:
            yield self._get_empty_message(query, is_track)
            return

        if raw:
            for entry in islice(results, limit):
                yield str(entry) + "\n"
            return

        for num, entry in enumerate(islice(results, limit), 1):
            url = self._extract_url(entry, is_track)

            if not url:
                continue

            if only_url:
                yield url
            else:
                formatted = self._fmt_entry(entry, num, is_track)
                if formatted:
                    yield formatted


class YouTubeProvider(BaseProvider):
    """
    Search provider for YouTube videos and playlists using yt-dlp.

    Uses yt-dlp's `extract_flat` mode to perform efficient searches without
    downloading any content. Supports searching for videos (`is_track=True`)
    and playlists (`is_track=False`). Results include standard YouTube
    metadata: title, channel, view count, duration, and video ID.
    """

    @staticmethod
    def _ytdl_opts() -> dict[str, Any]:
        """Get yt-dlp options for YouTube extraction."""
        return {
            "quiet": True,
            "extract_flat": True,
            "cachedir": False,
            "extractor_retries": 0,
            "extractor_args": {
                "youtube": {
                    "player_client": ["web", "ios"],
                    "player_skip": ["configs", "js", "webpage", "authcheck"],
                },
            },
        }

    def _build_search_query(self, query: str, limit: int, is_track: bool) -> str:
        search_type = "video" if is_track else "playlist"
        return f"ytsearch{limit}:{search_type}:{query}"

    @override
    def _extract_results(self, query: str, limit: int, is_track: bool) -> list[Any]:
        from ...utils import get_ytdlp

        YoutubeDL = get_ytdlp()
        with YoutubeDL(self._ytdl_opts()) as ydl:
            info = ydl.extract_info(
                self._build_search_query(query, limit, is_track), download=False
            )
            return info.get("entries", [])

    @override
    def _extract_url(self, entry: dict[str, Any], is_track: bool) -> str | None:
        if v_id := entry.get("id"):
            return "https://youtu.be/" + v_id
        return None

    @override
    def _fmt_entry(self, entry: dict[str, Any], num: int, is_track: bool) -> str | None:
        return self.formatter.fmt_result(
            num,
            title=entry.get("title", "Unknown Video"),
            artist=entry.get("channel", "Unknown Channel"),
            url=self._extract_url(entry, is_track),
            is_yt_video=True,
            is_track=is_track,
            views=self.formatter.fmt_views(entry.get("view_count")),
            duration=self.formatter.fmt_duration(entry.get("duration")),
        )

    @override
    def _get_empty_message(self, query: str, is_track: bool) -> str:
        return f"No videos matching '{query}'\n"


class YouTubeMusicProvider(BaseProvider):
    """
    Search provider for YouTube Music tracks and albums using ytmusicapi.

    Uses the ytmusicapi library to search YouTube Music's catalog:
    - Tracks (songs) include: title, artist(s), album, view count, duration
    - Albums include: title, artist(s), year, playlist ID
    Both result types include a URL to the content on music.youtube.com.
    """

    @override
    def _extract_results(self, query: str, limit: int, is_track: bool) -> list[Any]:
        from ytmusicapi import YTMusic

        search_type = "songs" if is_track else "albums"
        return YTMusic().search(query=query, limit=limit, filter=search_type)

    @override
    def _extract_url(self, entry: dict[str, Any], is_track: bool) -> str | None:
        if is_track and (t_id := entry.get("videoId")):
            return "https://music.youtube.com/watch?v=" + t_id
        elif pl_id := entry.get("playlistId"):
            return "https://music.youtube.com/playlist?list=" + pl_id
        return None

    @override
    def _fmt_entry(self, entry: dict[str, Any], num: int, is_track: bool) -> str | None:
        if is_track:
            return self.formatter.fmt_result(
                num=num,
                title=entry.get("title", "Unknown Track"),
                artist=self.formatter.extract_artist(entry),
                album=entry.get("album", {}).get("name", "Unknown Album"),
                url=self._extract_url(entry, is_track),
                is_yt_video=False,
                is_track=True,
                views=self.formatter.fmt_views(entry.get("views")),
                duration=self.formatter.fmt_duration(entry.get("duration")),
            )
        else:
            return self.formatter.fmt_result(
                num=num,
                title=entry.get("title", "Unknown Album"),
                artist=self.formatter.extract_artist(entry),
                url=self._extract_url(entry, is_track),
                is_yt_video=False,
                is_track=False,
                year=entry.get("year", "N/A"),
            )

    @override
    def _get_empty_message(self, query: str, is_track: bool) -> str:
        result_type = "tracks" if is_track else "albums"
        return f"No {result_type} found for '{query}'\n"
