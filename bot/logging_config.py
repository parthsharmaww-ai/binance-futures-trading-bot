"""
logging_config.py — Centralized logging setup.
Logs everything to file AND prints to console.
"""
import logging
import os


def setup_logging(log_file: str = "trading_bot.log") -> logging.Logger:
    """
    Configure logging for the entire bot.
    - INFO and above → console
    - DEBUG and above → log file
    Returns the root logger.
    """

    # Create logs folder if needed
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    # Root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler 1 — File (DEBUG level — captures everything)
    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Handler 2 — Console (INFO level — only important stuff)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Avoid duplicate handlers if called multiple times
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    else:
        logger.handlers.clear()
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
