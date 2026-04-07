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

                    # Extract fields from the tag
                    info = self._parse_stream_info(line)

                    variants.append({
                        "url": self._build_url(url),
                        "name": info.get("NAME"),
                        "resolution": info.get("RESOLUTION"),
                        "bandwidth": info.get("BANDWIDTH")
                    })

                except IndexError:
                    logger.warning("Malformed playlist: missing URL after stream info")

        logger.debug(f"Found {len(variants)} variants")
        return variants
    
    def parse_media(self):
        segments = []
        lines = self.content.splitlines()

        for i, line in enumerate(lines):
            if line.startswith("#EXTINF"):
                try:
                    url = lines[i + 1].strip()
                    segments.append(self._build_url(url))
                except IndexError:
                    logger.warning("Malformed playlist: missing segment URL")

        logger.debug(f"Found {len(segments)} segments")
        return segments
        
    def _parse_stream_info(self, line: str) -> dict:
        # Remove prefix
        parts = line.replace("#EXT-X-STREAM-INF:", "").split(",")

        data = {}

        for part in parts:
            if "=" in part:
                key, value = part.split("=", 1)
                data[key] = value.strip().strip('"')

        return data


    def _build_url(self, path: str) -> str:
        return urljoin(self.base_url, path)
