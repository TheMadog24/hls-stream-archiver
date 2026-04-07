import logging
import sys

def setup_logger(verbose=False, debug=False, log_file=None):
    logger = logging.getLogger()

    # Clear existing handlers (important when re-running in same process)
    if logger.handlers:
        logger.handlers.clear()

    # Set level
    if debug:
        logger.setLevel(logging.DEBUG)
    elif verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.INFO)  # <-- IMPORTANT

    formatter = logging.Formatter("[%(levelname)s] %(message)s")

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)  # allow all, root logger filters it

    logger.addHandler(handler)

    # Optional file logging
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

# hls_recorder/logger.py

def log_verbose(logger, msg, verbose: bool):
    if verbose:
        logger.info(msg)


def log_debug(logger, msg, debug: bool):
    if debug:
        logger.debug(msg)