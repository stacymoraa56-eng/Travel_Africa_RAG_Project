"""
Travel Africa RAG Assistant
---------------------------

Module: base_scraper.py

Purpose:
--------
This module provides a reusable base class for all web scrapers in the
Travel Africa RAG project.

Rather than implementing request handling, logging, delays, and HTML parsing
inside every individual scraper, these common responsibilities are centralized
here. This ensures consistency across all scraping modules while reducing code
duplication.

Responsibilities:
-----------------
1. Configure HTTP request headers.
2. Download webpages safely.
3. Respect ethical scraping practices by introducing delays.
4. Handle network errors gracefully.
5. Parse HTML using BeautifulSoup.
6. Provide helper methods that can be inherited by specialized scrapers.

Why This Design?
----------------
As the project grows to support multiple travel websites, each scraper will
share a common workflow:

Website URL
      ↓
Download HTML
      ↓
Parse HTML
      ↓
Extract Hotel Information

Instead of rewriting this workflow for every website, we define it once in
this module and allow other scrapers to inherit its functionality.

Role in the Pipeline:
---------------------

            scraper.py
                 │
      ┌──────────┼──────────┐
      │          │          │
      ▼          ▼          ▼
 Kenya      Safari      Official
Tourism    Bookings      Hotels
      │          │          │
      └──────────┼──────────┘
                 ▼
          base_scraper.py
                 ▼
         Shared HTTP Utilities
"""

# ==========================================================
# Imports
# ==========================================================

import logging
import random
import time
from typing import Optional

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# ==========================================================
# Logging Configuration
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ==========================================================
# Base Scraper Class
# ==========================================================

class BaseScraper:
    """
    Base class that provides shared functionality for all
    website-specific scrapers.

    Child scraper classes inherit this class so they don't need
    to reimplement request handling, delays, logging, or HTML parsing.
    """

    def __init__(self):
        """
        Initialize the scraper with a random browser User-Agent
        and default request headers.
        """

        self.user_agent = UserAgent()

        self.headers = {
            "User-Agent": self.user_agent.random,
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive"
        }

        self.request_delay = 5

    # ======================================================
    # Delay Between Requests
    # ======================================================

    def wait(self):
        """
        Pause between requests to avoid overwhelming the server.

        A small random delay is added so that requests appear
        more natural and are less likely to be flagged as automated.
        """

        delay = self.request_delay + random.uniform(0.5, 1.5)

        logger.info(f"Waiting {delay:.2f} seconds...")

        time.sleep(delay)

    # ======================================================
    # Download Webpage
    # ======================================================

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Download a webpage and return a BeautifulSoup object.

        Args:
            url (str):
                URL of the webpage.

        Returns:
            BeautifulSoup | None
        """

        try:

            logger.info(f"Fetching: {url}")

            response = requests.get(
                url,
                headers=self.headers,
                timeout=30
            )

            response.raise_for_status()

            self.wait()

            return BeautifulSoup(
                response.text,
                "lxml"
            )

        except requests.RequestException as e:

            logger.error(f"Request failed: {url}")

            logger.error(e)

            return None

    # ======================================================
    # Safe Text Extraction
    # ======================================================

    @staticmethod
    def safe_text(element):
        """
        Safely extract text from an HTML element.

        Args:
            element:
                BeautifulSoup HTML element.

        Returns:
            str
        """

        if element:
            return element.get_text(strip=True)

        return ""

    # ======================================================
    # Safe Attribute Extraction
    # ======================================================

    @staticmethod
    def safe_attribute(element, attribute):
        """
        Safely extract an HTML attribute.

        Example:
            img['src']

        becomes

            safe_attribute(img, 'src')
        """

        if element:
            return element.get(attribute, "")

        return ""

    # ======================================================
    # Hotel Template
    # ======================================================

    @staticmethod
    def hotel_template():
        """
        Returns a standardized hotel dictionary.

        Every scraper populates this structure so that
        all hotel records follow the same schema.
        """

        return {
            "hotel_name": "",
            "location": "",
            "county_or_region": "",
            "country": "",
            "description": "",
            "price_range": "",
            "amenities": "",
            "room_types": "",
            "rating": "",
            "review_summary": "",
            "nearby_attractions": "",
            "hotel_category": "",
            "contact_information": "",
            "website_url": "",
            "image_url": "",
            "source_url": ""
        }