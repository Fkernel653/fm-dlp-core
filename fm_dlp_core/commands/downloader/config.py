from ...utils.config.parametrs import ParametersManager
from .params import DownloadParams


class DownloadConfig:
    """Configuration container for download settings."""

    def __init__(self, params: DownloadParams):
        self.params = params
        self.params_manager = ParametersManager(params.color)

    def apply_config(self) -> dict[str, str | int | bool | None]:
        """
        Apply saved configuration settings if requested and return parameters dict.

        If `use_config` is True, this method retrieves previously saved parameters
        from the configuration storage and merges them with the current instance
        values, giving priority to saved values. If `use_config` is False or no
        saved configuration exists, the current instance values are returned unchanged.

        Returns:
            dict[str, str | int | bool | None]: A dictionary containing the final parameters to be used
                for downloading. Keys include: codec, kbps, quality, jobs, quiet,
                metadata, keep, only_video, cookies and remote.
        """
        if self.params.use_config:
            conf = self.params_manager.get_parameters()
            return {
                "codec": conf.get("codec", self.params.codec),
                "kbps": conf.get("kbps", self.params.kbps),
                "quality": conf.get("quality", self.params.quality),
                "jobs": conf.get("jobs", self.params.jobs),
                "quiet": conf.get("quiet", self.params.quiet),
                "metadata": conf.get("metadata", self.params.metadata),
                "keep": conf.get("keep", self.params.keep),
                "only_video": conf.get("only_video", self.params.only_video),
                "cookies": conf.get("cookies", self.params.cookies),
                "remote": conf.get("remote", self.params.remote),
            }
        return {
            "codec": self.params.codec,
            "kbps": self.params.kbps,
            "quality": self.params.quality,
            "jobs": self.params.jobs,
            "quiet": self.params.quiet,
            "metadata": self.params.metadata,
            "keep": self.params.keep,
            "only_video": self.params.only_video,
            "cookies": self.params.cookies,
            "remote": self.params.remote,
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
        if self.params.save:
            return self.params_manager.set_parameters(
                self.params.codec,
                self.params.kbps,
                self.params.quality,
                self.params.jobs,
                self.params.quiet,
                self.params.metadata,
                self.params.keep,
                self.params.only_video,
                self.params.cookies,
                self.params.remote,
            )
        return True
