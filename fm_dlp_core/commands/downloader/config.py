"""Configuration handling for downloader."""

from typing import final

from ...utils import DownloadParams
from ...utils.config.parametrs import get_parameters, set_parameters


@final
class DownloadConfig:
    """Configuration container for download settings."""

    def __init__(
        self,
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
        color: bool,
    ):
        self.url = url
        self.codec = codec
        self.kbps = kbps
        self.quality = quality
        self.jobs = jobs
        self.quiet = quiet
        self.metadata = metadata
        self.keep = keep
        self.save = save
        self.use_config = use_config
        self.path = path
        self.only_video = only_video
        self.cookies = cookies
        self.color = color

    def apply_config(self) -> DownloadParams:
        """
        Apply saved configuration settings if requested and return parameters dict.

        If `use_config` is True, this method retrieves previously saved parameters
        from the configuration storage and merges them with the current instance
        values, giving priority to saved values. If `use_config` is False or no
        saved configuration exists, the current instance values are returned unchanged.

        Returns:
            dict[str, Any]: A dictionary containing the final parameters to be used
                for downloading. Keys include: codec, kbps, quality, jobs, quiet,
                metadata, keep, only_video, and cookies.
        """
        if self.use_config:
            params = get_parameters(self.color)
            return {
                "codec": params.get("codec", self.codec),
                "kbps": params.get("kbps", self.kbps),
                "quality": params.get("quality", self.quality),
                "jobs": params.get("jobs", self.jobs),
                "quiet": params.get("quiet", self.quiet),
                "metadata": params.get("metadata", self.metadata),
                "keep": params.get("keep", self.keep),
                "only_video": params.get("only_video", self.only_video),
                "cookies": params.get("cookies", self.cookies),
            }
        return {
            "codec": self.codec,
            "kbps": self.kbps,
            "quality": self.quality,
            "jobs": self.jobs,
            "quiet": self.quiet,
            "metadata": self.metadata,
            "keep": self.keep,
            "only_video": self.only_video,
            "cookies": self.cookies,
        }

    def save_config(self) -> bool:
        """
        Save current download settings to the persistent configuration file.

        This method persists the current instance parameters (codec, quality, jobs,
        etc.) to the user's configuration storage so they can be reused in future
        sessions via the `--use-config` option. The method is only executed if
        the `save` flag is True.

        Returns:
            bool: True if configuration was saved successfully or if `save` is False
                (no operation needed), False if an error occurred during saving.
        """
        if self.save:
            return set_parameters(
                self.codec,
                self.kbps,
                self.quality,
                self.jobs,
                self.quiet,
                self.metadata,
                self.keep,
                self.only_video,
                self.cookies,
                self.color,
            )
        return True
