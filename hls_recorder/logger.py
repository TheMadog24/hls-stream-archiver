import logging
import sys


def setup_logger(
    verbose: bool = False,
    debug: bool = False,
    log_file: str = None,
):
		
	
    """
    Configure application logging.

    :param verbose: Enable verbose (INFO) console output
    :param debug: Enable debug (DEBUG) console output
    :param log_file: Optional file to write logs to
    """

	# This sets up logging, and captures everything internally
	# Will setup filters later

    logger = logging.getLogger()	
    logger.setLevel(logging.DEBUG)  

    # Clear Hadlers to prevent duplicate logs, I think
	
    logger.handlers.clear()
	
	

    # ------------------------
    # Console
    # ------------------------
	
	# Setup multiple levels of logging/debugging
	# File should write everything to a specified output file
	
    console_handler = logging.StreamHandler(sys.stdout)

    if debug:
        console_level = logging.DEBUG
    elif verbose:
        console_level = logging.INFO
    else:
        console_level = logging.WARNING

    console_handler.setLevel(console_level)

    console_format = logging.Formatter(
        "[%(levelname)s] %(message)s"
    )
    console_handler.setFormatter(console_format)

    logger.addHandler(console_handler)
	


    # ------------------------
    # File Handler
    # ------------------------
	
	
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        file_format = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        file_handler.setFormatter(file_format)

        logger.addHandler(file_handler)

    return logger