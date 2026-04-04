import argparse
import logging
from hls_recorder.logger import setup_logger


def parse_args():
    parser = argparse.ArgumentParser(
        description="HLS Stream Recorder"
    )

    # ------------------------
    # Arguments
    # ------------------------
	
	
    parser.add_argument(
        "url",
        help="HLS playlist URL"
    )

    # ------------------------
    # Auth options
    # ------------------------
	
	# Auth options are mutually exclusive
	# Only 1 or the other, not both
	# manually entered OAuth or OAuth read from specified file
	
    auth_group = parser.add_mutually_exclusive_group()

    auth_group.add_argument(
        "--auth-token",
        help="Twitch OAuth token"
    )

    auth_group.add_argument(
        "--auth-file",
        help="Path to auth JSON file"
    )


    # ------------------------
    # Logging
    # ------------------------
		
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output"
    )

    parser.add_argument(
        "--log-file",
        help="Write logs to file"
    )

    return parser.parse_args()


def main():
    args = parse_args()


    # ------------------------
    # Setup logging
    # ------------------------
		
    setup_logger(
        verbose=args.verbose,
        debug=args.debug,
        log_file=args.log_file
    )

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


if __name__ == "__main__":
    main()