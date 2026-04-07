import logging
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class PlaylistParser:
    def __init__(self, content: str, base_url: str):
        self.content = content
        self.base_url = base_url

    def is_master_playlist(self) -> bool:
        return "#EXT-X-STREAM-INF" in self.content

    def parse_master(self):
        variants = []

        lines = self.content.splitlines()

        for i, line in enumerate(lines):
            if line.startswith("#EXT-X-STREAM-INF"):
                try:
                    url = lines[i + 1].strip()

                    variants.append({"info": line, "url": self._build_url(url)})

                except IndexError:
                    logger.warning("Malformed playlist: missing URL after stream info")

        logger.debug(f"Found {len(variants)} variants")

        return variants

    def _build_url(self, path: str) -> str:
        return urljoin(self.base_url, path)
