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

    consoleHandler = logging.StreamHandler(sys.stdout)
    fileHandler = logging.FileHandler(logFilePath)

    logFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    consoleHandler.setFormatter(logFormat)
    fileHandler.setFormatter(logFormat)

    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)

    return logger

logger = setup_logger()