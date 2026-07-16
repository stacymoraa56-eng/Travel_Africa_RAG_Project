"""
Travel Africa RAG Assistant
--------------------------------------------------

Module:
    base_api.py

Purpose:
--------
Provides a reusable base class for interacting with REST APIs used
throughout the Travel Africa RAG project.

All API clients inherit this class to reuse common functionality such
as sending requests, waiting between requests, handling errors, and
logging.
"""

# ==========================================================
# Imports
# ==========================================================

import json
import random
import time
from typing import Dict, Optional

import requests

from data_collection.utils.logger import logger


# ==========================================================
# Base API Client
# ==========================================================

class BaseAPIClient:
    """
    Parent class for all API clients.
    """

    def __init__(self):
        """
        Initialize API settings.
        """

        self.timeout = 30
        self.request_delay = 5

        self.headers = {
            "User-Agent": "TravelAfricaRAG/1.0 (Educational Project)",
            "Accept": "application/json"
        }

    # ======================================================
    # Wait Between Requests
    # ======================================================

    def wait(self):
        """
        Pause between requests to respect API rate limits.
        """

        delay = self.request_delay + random.uniform(0.5, 1.5)

        logger.info(f"Waiting {delay:.2f} seconds...")

        time.sleep(delay)

    # ======================================================
    # HTTP GET Request
    # ======================================================

    def get(
        self,
        url: str,
        params: Optional[Dict] = None,
        retries: int = 3
    ):
        """
        Send an HTTP GET request.

        Parameters
        ----------
        url : str
            API endpoint.

        params : dict
            Query parameters.

        retries : int
            Number of retry attempts.

        Returns
        -------
        dict | None
        """

        for attempt in range(retries):

            try:

                logger.info(
                    f"Request {attempt + 1}: {url}"
                )

                response = requests.get(
                    url=url,
                    headers=self.headers,
                    params=params,
                    timeout=self.timeout
                )

                response.raise_for_status()

                self.wait()

                return response.json()

            except requests.RequestException as e:

                logger.warning(
                    f"Attempt {attempt + 1} failed."
                )

                logger.warning(e)

                time.sleep(2)

        logger.error("Maximum retries exceeded.")

        return None

    # ======================================================
    # Pretty Print JSON
    # ======================================================

    @staticmethod
    def pretty_json(data):
        """
        Print formatted JSON.
        """

        print(
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False
            )
        )