"""
Travel Africa RAG Assistant
--------------------------------------------------

Module:
    magical_kenya.py

Purpose:
--------
This module scrapes accommodation listings from the
Magical Kenya Tourism Information Centre (TIC).

Unlike the Overpass API, which primarily provides
basic location information, this scraper extracts
rich hotel information including descriptions,
websites, contact details, images, and accommodation
metadata.

The scraper works in two stages:

1. Discover accommodation listing URLs.
2. Visit every listing page and extract hotel details.

Responsibilities
----------------
- Discover accommodation listings
- Visit every hotel page
- Extract hotel information
- Standardize hotel records
- Respect ethical scraping practices
- Preserve the original source URL

Output
------
Returns a list of standardized hotel dictionaries
which are later merged with data collected from the
Overpass API before being cleaned and embedded for
the RAG pipeline.

Role in the Pipeline
--------------------

          Magical Kenya Website
                    │
                    ▼
          magical_kenya.py
                    │
                    ▼
      Standardized Hotel Records
                    │
                    ▼
              merger.py
"""

from urllib.parse import urljoin
import re

from bs4 import BeautifulSoup

from data_collection.html.base_scraper import BaseScraper
from data_collection.utils.logger import logger


class MagicalKenyaScraper(BaseScraper):

    BASE_URL = "https://tic.magicalkenya.com"

    LISTING_URL = (
        "https://tic.magicalkenya.com/listing-type/accommodation/"
    )

    MAX_PAGES = 40

    # ---------------------------------------------------------
    # Discover Hotel Links
    # ---------------------------------------------------------

    def get_listing_links(self):
        """
        Collect all accommodation listing URLs from
        every available page.
        """

        links = set()

        for page in range(1, self.MAX_PAGES + 1):

            page_url = (
                self.LISTING_URL
                if page == 1
                else f"{self.LISTING_URL}page/{page}/"
            )

            logger.info(f"Scanning page {page}")

            soup = self.fetch_page(page_url)

            if soup is None:
                continue

            page_links = 0

            for anchor in soup.find_all("a", href=True):

                href = anchor["href"]

                if "/listing/" in href:

                    links.add(urljoin(self.BASE_URL, href))
                    page_links += 1

            logger.info(
                f"Found {page_links} listings on page {page}"
            )

            # Stop automatically if no more listings exist

            if page_links == 0:
                break

        logger.info(
            f"Discovered {len(links)} unique hotels."
        )

        return sorted(links)

    # ---------------------------------------------------------
    # Parse Individual Hotel Page
    # ---------------------------------------------------------

    def parse_listing(self, url):

        soup = self.fetch_page(url)

        if soup is None:
            return None

        def text(selector):

            element = soup.select_one(selector)

            if element:
                return element.get_text(" ", strip=True)

            return ""

        hotel = {

            "hotel_name": text("h1"),

            "location": "",

            "county_or_region": "",

            "country": "Kenya",

            "description": text(
                ".elementor-widget-theme-post-content"
            ),

            "price_range": "",

            "amenities": "",

            "room_types": "",

            "rating": "",

            "review_summary": "",

            "nearby_attractions": "",

            "hotel_category": "Accommodation",

            "contact_information": "",

            "website_url": "",

            "image_url": "",

            "source_url": url
        }

        # -------------------------------------------------
        # Website
        # -------------------------------------------------

        for link in soup.find_all("a", href=True):

            href = link["href"]

            if (
                href.startswith("http")
                and "magicalkenya" not in href
            ):

                hotel["website_url"] = href
                break

        # -------------------------------------------------
        # Phone Number
        # -------------------------------------------------

        page_text = soup.get_text(" ", strip=True)

        phone = re.search(
            r"(\+254[\d\s-]+|0\d{9})",
            page_text
        )

        if phone:

            hotel["contact_information"] = phone.group(1)

        # -------------------------------------------------
        # Featured Image
        # -------------------------------------------------

        image = soup.find("img")

        if image:

            hotel["image_url"] = image.get("src", "")

        # -------------------------------------------------
        # Attempt Location Extraction
        # -------------------------------------------------

        breadcrumbs = soup.select("nav a")

        for crumb in breadcrumbs:

            value = crumb.get_text(strip=True)

            if value not in ["Home", "Accommodation"]:

                hotel["location"] = value

        return hotel

    # ---------------------------------------------------------
    # Main Scraper
    # ---------------------------------------------------------

    def scrape(self):

        logger.info(
            "Starting Magical Kenya accommodation scraper..."
        )

        hotels = []

        links = self.get_listing_links()

        total = len(links)

        for index, url in enumerate(links, start=1):

            logger.info(
                f"[{index}/{total}] Scraping hotel..."
            )

            hotel = self.parse_listing(url)

            if hotel:

                hotels.append(hotel)

            self.wait()

        logger.info(
            f"Finished. Collected {len(hotels)} hotels."
        )

        return hotels