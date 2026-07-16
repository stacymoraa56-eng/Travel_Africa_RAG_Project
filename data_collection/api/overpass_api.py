"""
Travel Africa RAG Assistant
--------------------------------------------------

Module:
    overpass_api.py

Purpose
-------
Collect hotel records from OpenStreetMap using the
Overpass API.

This is the primary data source for hotel discovery.
Each hotel includes its geographic coordinates, which
are later enriched using the Nominatim API.
"""

from data_collection.api.base_api import BaseAPIClient
from data_collection.utils.logger import logger

import random


class OverpassAPI(BaseAPIClient):

    OVERPASS_URL = "https://overpass-api.de/api/interpreter"

    LOCATIONS = [
        "Nairobi",
        "Mombasa",
        "Diani",
        "Naivasha",
        "Nakuru",
        "Maasai Mara",
        "Amboseli",
        "Watamu",
        "Malindi",
        "Kisumu",
        "Nanyuki",
        "Lamu",
        "Zanzibar",
        "Arusha",
        "Kampala",
        "Dar es Salaam"
    ]

    # ======================================================
    # Maximum hotels to keep from each destination
    # ======================================================

    LOCATION_LIMITS = {

        "Nairobi": 7,
        "Mombasa": 8,
        "Diani": 6,
        "Naivasha": 6,
        "Nakuru": 5,
        "Maasai Mara": 6,
        "Amboseli": 5,
        "Watamu": 5,
        "Malindi": 5,
        "Kisumu": 5,
        "Nanyuki": 5,
        "Lamu": 5,
        "Zanzibar": 10,
        "Arusha": 10,
        "Kampala": 10,
        "Dar es Salaam": 10
    }

    def __init__(self):
        super().__init__()

    # ======================================================

    def build_query(self, location):

        return f"""
        [out:json][timeout:60];

        area["name"="{location}"]->.searchArea;

        (
            node["tourism"="hotel"](area.searchArea);
            way["tourism"="hotel"](area.searchArea);
            relation["tourism"="hotel"](area.searchArea);
        );

        out center tags;
        """

    # ======================================================

    def collect_location(self, location):

        logger.info(f"Collecting hotels for {location}")

        response = self.get(
            self.OVERPASS_URL,
            params={
                "data": self.build_query(location)
            }
        )

        if response is None:
            return []

        hotels = []

        for element in response.get("elements", []):

            tags = element.get("tags", {})

            hotel = {

                "hotel_name": tags.get(
                    "name",
                    "Unknown Hotel"
                ),

                "location": location,

                "county_or_region": "",

                "country": "",

                "description": tags.get(
                    "description",
                    ""
                ),

                "price_range": "",

                "amenities": "",

                "room_types": "",

                "rating": "",

                "review_summary": "",

                "nearby_attractions": "",

                "hotel_category": tags.get(
                    "tourism",
                    "Hotel"
                ),

                "contact_information": tags.get(
                    "phone",
                    ""
                ),

                "website_url": tags.get(
                    "website",
                    ""
                ),

                "image_url": "",

                "latitude": element.get(
                    "lat",
                    element.get("center", {}).get("lat")
                ),

                "longitude": element.get(
                    "lon",
                    element.get("center", {}).get("lon")
                ),

                "source_url": "https://www.openstreetmap.org"
            }

            hotels.append(hotel)

        total_found = len(hotels)

        # ==================================================
        # Randomly sample hotels
        # ==================================================

        random.Random(42).shuffle(hotels)

        limit = self.LOCATION_LIMITS.get(location, 10)

        hotels = hotels[:limit]

        logger.info(
            f"{location}: kept {len(hotels)} of {total_found} hotels."
        )

        return hotels

    # ======================================================

    def collect_all(self):

        all_hotels = []

        for location in self.LOCATIONS:

            hotels = self.collect_location(location)

            all_hotels.extend(hotels)

        logger.info(
            f"Collected {len(all_hotels)} hotels from Overpass."
        )

        return all_hotels