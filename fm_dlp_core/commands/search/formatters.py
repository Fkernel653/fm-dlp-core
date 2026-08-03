"""Result formatting utilities for search results."""

from ...utils.colors import BOLD_CYAN, BOLD_RED, BOLD_WHITE, GRAY, RESET, WHITE


class ResultFormatter:
    """Format search results with optional metadata and colors."""

    def __init__(self, color: bool, error_prefix: str):
        """Initialize formatter with color settings."""
        self.color = color
        self.error_prefix = error_prefix
        self._c = {
            "bold_cyan": BOLD_CYAN if color else "",
            "bold_red": BOLD_RED if color else "",
            "bold_white": BOLD_WHITE if color else "",
            "gray": GRAY if color else "",
            "white": WHITE if color else "",
            "reset": RESET if color else "",
        }

    @staticmethod
    def fmt_views(v: str | int | None) -> str:
        """Format view count with commas."""
        if v is None:
            return "N/A"

        if isinstance(v, str):
            return v

        return f"{int(float(v)):,}"

    @staticmethod
    def fmt_duration(d: str | float | None) -> str:
        """Format duration from seconds to MM:SS or HH:MM:SS."""
        if d is None:
            return "N/A"

        d_str = str(d)
        if ":" in d_str:
            return d_str

        s = int(d)
        h, remainder = divmod(s, 3600)
        m, s = divmod(remainder, 60)

        return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

    @staticmethod
    def extract_artist(item: dict) -> str:
        """Extract artist name from YouTube Music response."""
        artists = item.get("artists", [])
        return artists[0].get("name", "Unknown Artist") if artists else "Unknown Artist"

    def fmt_result(
        self,
        num: int,
        title: str,
        artist: str,
        url: str | None,
        is_yt_video: bool,
        is_track: bool,
        **kwargs,
    ) -> str:
        """Format a single search result with optional metadata."""
        c = self._c
        w = c["white"]
        g = c["gray"]

        tree = f"    {g}├─"
        corner = f"    {g}└─"
        sep = f" {g}│{w} "
        div = f"       {g}{'─' * 50}{c['reset']}\n"

        lines = [f"\n{c['bold_cyan']}{num}. {c['bold_white']}{title}"]

        if is_yt_video:
            views = kwargs.get("views", "N/A")
            duration = kwargs.get("duration", "N/A")

            lines.append(f"{tree} {w + artist}")
            lines.append(f"{tree} {w + views}{sep}{w + duration}")

        elif is_track:
            album = kwargs.get("album", "Unknown Album")
            views = kwargs.get("views", "N/A")
            duration = kwargs.get("duration", "N/A")

            lines.extend(
                [
                    f"{tree} {w + artist}",
                    f"{tree} {w + album}",
                    f"{tree} {w + views}{sep}{w + duration}",
                ]
            )

        else:
            year = kwargs.get("year", "N/A")
            lines.extend([f"{tree} {w + artist}", f"{tree} {w + year}"])
        if url:
            lines.append(f"{corner} {c['bold_red']}{url}")
        lines.append(div)

        return "\n".join(lines)

    def fmt_error(self, error: str) -> str:
        """Format error message."""
        return f"\n{BOLD_RED}{self.error_prefix}{RESET}{error}\n"
