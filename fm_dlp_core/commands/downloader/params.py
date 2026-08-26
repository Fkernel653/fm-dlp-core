from dataclasses import dataclass


@dataclass
class DownloadParams:
    url: str
    codec: str
    kbps: int
    quality: str
    jobs: int
    quiet: bool
    metadata: bool
    keep: bool
    save: bool
    use_config: bool
    path: str
    only_video: bool
    cookies: str | None
    remote: str | None
    color: bool
