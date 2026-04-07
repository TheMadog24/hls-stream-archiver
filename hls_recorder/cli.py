import argparse
import logging
from hls_recorder.logger import setup_logger
from hls_recorder.logger import log_verbose, log_debug
from hls_recorder.playlist import PlaylistFetcher
from hls_recorder.parser import PlaylistParser
from hls_recorder.quality import select_variant


def parse_args():
    parser = argparse.ArgumentParser(description="HLS Stream Recorder")

    # ------------------------
    # Arguments
    # ------------------------

    parser.add_argument("url", help="HLS playlist URL")

    # ------------------------
    # Auth options
    # ------------------------

    # Auth options are mutually exclusive
    # Only 1 or the other, not both
    # manually entered OAuth or OAuth read from specified file

    auth_group = parser.add_mutually_exclusive_group()

    auth_group.add_argument("--auth-token", help="Twitch OAuth token")

    auth_group.add_argument("--auth-file", help="Path to auth JSON file")

    # ------------------------
    # Logging
    # ------------------------

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    parser.add_argument("--debug", action="store_true", help="Enable debug output")

    parser.add_argument("--log-file", help="Write logs to file")
    
    parser.add_argument("--quality", default="best", help="Stream quality (e.g. best, 1080, 720, 480)")

    return parser.parse_args()
    

def main():
    args = parse_args()
    
    is_verbose = args.verbose
    is_debug = args.debug

    # ------------------------
    # Setup logging
    # ------------------------

    setup_logger(verbose=args.verbose, debug=args.debug, log_file=args.log_file)

    logger = logging.getLogger(__name__)

    # ------------------------
    # Basic startup log
    # ------------------------

    logger.info("Starting HLS Recorder")
    logger.debug(f"Arguments: {args}")

    # Auth handling
    # Auth should never be logged in plain text
    # Either masked, hidden or skipped/blanked

    if args.auth_token:
        logger.info("[Auth] Token provided (masked)")
    elif args.auth_file:
        logger.info(f"[Auth] Using auth file: {args.auth_file}")
    else:
        logger.info("[Auth] No authentication provided (fallback mode)")

    # Next step

    logger.info(f"Target URL: {args.url}")

    # ------------------------
    # Playlist Fetching
    # ------------------------

    fetcher = PlaylistFetcher(
        url=args.url,
        auth_token=args.auth_token,
        verbose=is_verbose,
        debug=is_debug
    )

    try:
        if is_verbose or is_debug:
            logger.info(f"Fetching playlist: {args.url}")
            
        playlist_text = fetcher.fetch()
        logger.info("Playlist found")
        

        # Prints what it sees
        logger.debug("Playlist preview:")
        for line in playlist_text.splitlines()[:10]:
            logger.debug(line)

    except Exception as e:
        logger.error(f"Failed to fetch playlist: {e}")
        if is_debug:
            logger.debug("Full exception:", exc_info=True)
        return

    parser = PlaylistParser(playlist_text, args.url)

    if parser.is_master_playlist():
        variants = parser.parse_master()
		
		
        if is_verbose or is_debug:
            logger.info("Detected master playlist")
            logger.info(f"Found {len(variants)} variants")

        if is_debug:
            for v in variants:
                logger.debug(f"Variant: {v['url']}")

        # ------------------------
        # Quality Selection
        # ------------------------

        selected_variant, match_type = select_variant(variants, args.quality)

        best_variant = selected_variant["url"]
        quality = selected_variant.get("name", args.quality)
        resolution = selected_variant.get("resolution", "unknown")
        
        if is_verbose:
            logger.info(f"Requested quality: {args.quality}")
            logger.info(f"Matching variant found: {quality} ({resolution})")
        
        logger.info(f"Using quality: {quality}")
        
        if is_verbose or is_debug:
            logger.info(f"Variant URL: {best_variant}")
        

        # ------------------------
        # Fetch variant playlists
        # ------------------------

        variant_fetcher = PlaylistFetcher(
            url=best_variant,
            auth_token=args.auth_token,
            verbose=is_verbose,
            debug=is_debug
        )

        try:
            variant_content = variant_fetcher.fetch()
            if is_verbose or is_debug:
                logger.info("Fetched variant playlist")

        except Exception as e:
            logger.error(f"Failed to fetch playlist: {e}")
            if is_debug:
                logger.debug("Full exception:", exc_info=True)
            return

        # ------------------------
        # Parse media playlist
        # ------------------------

        variant_parser = PlaylistParser(variant_content, best_variant)

        if variant_parser.is_master_playlist():
            logger.warning("Variant is still a master playlist (unexpected)")
        else:
            segments = variant_parser.parse_media()
            
            if is_verbose or is_debug:
                logger.info("Detected media playlist (segments)")
            logger.info("Ready to record")
            
            if is_verbose:
                logger.info("Detected media playlist (segments)")
                logger.info(f"Found {len(segments)} segments")

            if is_debug:
                for s in segments[:10]:  # optionally limit
                    logger.debug(f"Segment: {s}")

    else:
        logger.info("Detected media playlist (segments)")
        segments = parser.parse_media()

        for s in segments[:10]:
            logger.info(f"Segment: {s}")    

if __name__ == "__main__":
    main()
