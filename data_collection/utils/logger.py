"""
Travel Africa RAG Assistant
--------------------------------------------------

Module:
    logger.py

Purpose:
--------
Centralizes logging configuration for the entire
Travel Africa data collection pipeline.

All scrapers and API clients import this logger so
that logs are written consistently to both the console
and a log file.
"""

import logging
import os

# --------------------------------------------------
# Create logs directory if it doesn't exist
# --------------------------------------------------

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "scraper.log")

# --------------------------------------------------
# Configure Logger
# --------------------------------------------------

logger = logging.getLogger("travel_africa")

logger.setLevel(logging.INFO)

# Prevent duplicate handlers
if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # Log to terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Log to file
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)