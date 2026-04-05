import logging
import requests


logger = logging.getLogger(__name__)


class PlaylistFetcher:
    def __init__(self, url: str, auth_token: str = None):
        self.url = url
        self.auth_token = auth_token

    def fetch(self) -> str:
        

        headers = {}

        # ------------------------
        # Auth Handling
        # ------------------------
		
		# Attempts to use Auth if provided
		
		# DO NOT LOG AUTH
        if self.auth_token:
            headers["Authorization"] = f"OAuth {self.auth_token}"
            logger.debug("Using OAuth token for request")

        try:
            logger.info(f"Fetching playlist: {self.url}")

            response = requests.get(
                self.url,
                headers=headers,
                timeout=10
            )

            response.raise_for_status()

            logger.debug(f"Playlist fetched successfully ({len(response.text)} bytes)")

            return response.text

        except requests.exceptions.Timeout:
            logger.error("Request timed out")
            raise

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            raise

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise