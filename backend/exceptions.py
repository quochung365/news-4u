class DownloadException(Exception):
    """Exception raised for errors in the downloading process."""
    def __init__(self, url: str, msg: str = "Failed to download the page"):
        self.url = url
        self.msg = msg
        super().__init__(f"{msg}: {url}")