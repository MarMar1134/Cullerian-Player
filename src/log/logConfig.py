"""Logging system to track application events and errors."""

import logging
import sys

def setup_logger():
    """Configure the application-wide logger."""

    from pathlib import Path

    logPath = Path(__file__).resolve().parent.parent.parent / "logs"

    if not logPath.exists():
        logPath.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("cullerian_player")
    logger.setLevel(logging.INFO)

    logFilePath = logPath / 'cullerian_player.log'

    # Create handlers
    consoleHandler = logging.StreamHandler(sys.stdout)
    fileHandler = logging.FileHandler(logFilePath)

    # Create formatters and add it to handlers
    logFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    consoleHandler.setFormatter(logFormat)
    fileHandler.setFormatter(logFormat)

    # Add handlers to the logger
    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)

    return logger

logger = setup_logger()