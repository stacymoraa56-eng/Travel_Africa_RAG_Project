"""
Travel Africa RAG Assistant
---------------------------

Module: scraper.py

Purpose:
--------
This module is responsible for collecting publicly available hotel information
from selected travel websites and official tourism sources. It serves as the
first stage of the Retrieval-Augmented Generation (RAG) pipeline by creating
the raw dataset that will later be cleaned, embedded, and indexed in the vector
database.

Responsibilities:
-----------------
1. Send HTTP requests to publicly available hotel listing pages.
2. Respect ethical scraping practices by:
   - Using a descriptive User-Agent.
   - Adding delays between requests.
   - Handling request failures gracefully.
3. Extract hotel information into a standardized format.
4. Store the collected records as a raw CSV dataset.

Output:
-------
The scraper generates:

    data/raw/hotels_raw.csv

The raw dataset intentionally preserves duplicate records, incomplete fields,
and minor inconsistencies. These will be addressed during the data cleaning
stage to demonstrate a realistic data engineering workflow.

"""

# Import necessary libraries 
# ==========================================================
# Imports
# ==========================================================
# Import the required libraries for:
# - making HTTP requests
# - parsing HTML
# - storing scraped data
# - logging progress
# - introducing polite delays between requests
# ==========================================================
import os
import time
import random
import logging
from urllib.parse import urljoin

import requests
import pandas as pd

from bs4 import BeautifulSoup
from fake_useragent import UserAgent



# Logging configuration
# ==========================================================
# Logging Configuration
# ==========================================================
# Logging allows us to monitor the scraper as it runs.
# Instead of using print statements, logging provides
# timestamps, message levels, and better debugging support.
# ==========================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Output folder 
RAW_DATA_FOLDER = "../data/raw"

os.makedirs(RAW_DATA_FOLDER, exist_ok=True)

# Request headers
# ==========================================================
# HTTP Request Headers
# ==========================================================
# Many websites reject requests that appear to come from bots.
# We rotate User-Agent strings to mimic normal browser traffic.
# ==========================================================
ua = UserAgent()

HEADERS = {
    "User-Agent": ua.random,
    "Accept-Language": "en-US,en;q=0.9"
}


#Five seconds delay between requests
# ==========================================================
# Rate Limiting
# ==========================================================
# To comply with responsible scraping practices and reduce the
# likelihood of overwhelming target servers, the scraper waits
# approximately five seconds between requests.
# ==========================================================

REQUEST_DELAY = 5


def polite_pause():
    """
    Sleep between requests to avoid overwhelming servers.
    """
    delay = REQUEST_DELAY + random.uniform(0, 1.5)
    logger.info(f"Sleeping for {delay:.2f} seconds...")
    time.sleep(delay)


# Request function with error handling
# ==========================================================
# Page Retrieval
# ==========================================================
# This helper function downloads a webpage while:
# - applying request headers
# - handling network errors
# - respecting rate limits
# - returning the HTML for parsing
# ==========================================================
def fetch_page(url):
    """
    Fetch a webpage safely.
    """

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=30
        )

        response.raise_for_status()

        polite_pause()

        return response.text

    except Exception as e:

        logger.error(f"Failed: {url}")

        logger.error(e)

        return None
    

# Hotel model - Every scraped hotel will use the same structure 
# ==========================================================
# Hotel Record Schema
# ==========================================================
# Every hotel is represented using the same dictionary
# structure. Maintaining a consistent schema simplifies
# data cleaning, storage, and embedding generation later
# in the RAG pipeline.
# ==========================================================
def create_hotel_record():

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

# Save hotels as csv files 
# ==========================================================
# Save Dataset
# ==========================================================
# After scraping completes, all hotel records are exported
# to a CSV file that serves as the raw dataset for the
# subsequent cleaning stage.
# ==========================================================
def save_hotels(hotels):

    df = pd.DataFrame(hotels)

    output = os.path.join(
        RAW_DATA_FOLDER,
        "hotels_raw.csv"
    )

    df.to_csv(output, index=False)

    logger.info(f"Saved {len(df)} hotels.")

