from dataclasses import dataclass


@dataclass
class DownloadParams:
    """
    Data container for all download configuration parameters.

    Aggregates all settings required for a download operation: URL, format
    preferences (codec, bitrate, quality), output handling (path, keep, save),
    and authentication (cookies). All fields are required at instantiation
    to ensure explicit configuration.

    Attributes:
        url: Target YouTube/YouTube Music URL.
        codec: Audio format (mp3, m4a, flac, wav, opus, etc.).
        kbps: Audio bitrate in kbps.
        quality: Video quality preset (e.g., '1080p', '720p', 'best').
        jobs: Number of concurrent download workers.
        quiet: Suppress console output if True.
        metadata: Embed tags and thumbnails if True.
        keep: Keep intermediate files after download if True.
        save: Persist configuration for future use if True.
        use_config: Load settings from config file if True.
        path: Output directory path.
        only_video: Download video only (skip audio extraction) if True.
        cookies: Path to Netscape-format cookies file (optional).
        remote: Remote destination path for uploads (optional).
        color: Enable colored console output if True.
    """

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
