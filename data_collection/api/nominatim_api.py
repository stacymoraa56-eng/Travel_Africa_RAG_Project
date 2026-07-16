"""
Travel Africa RAG Assistant
--------------------------------------------------

Module:
    nominatim_api.py

Purpose:
--------
Uses the OpenStreetMap Nominatim API to enrich hotel
records with administrative information such as county,
region, country, and a formatted address.

This module is used after collecting hotels from the
Overpass API.
"""

from unittest import result

from data_collection.api.base_api import BaseAPIClient
from data_collection.utils.logger import logger


class NominatimAPI(BaseAPIClient):
    """
    Reverse geocoding client using the OpenStreetMap
    Nominatim API.
    """

    BASE_URL = "https://nominatim.openstreetmap.org/reverse"

    def reverse_geocode(self, latitude: float, longitude: float):
        """
        Reverse geocode a pair of coordinates.

        Parameters
        ----------
        latitude : float

        longitude : float

        Returns
        -------
        dict
        """

        params = {
            "lat": latitude,
            "lon": longitude,
            "format": "jsonv2",
            "addressdetails": 1
        }

        data = self.get(
            self.BASE_URL,
            params=params
        )

        if data is None:
            return None

        address = data.get("address", {})

        return {
            "county_or_region":(
                address.get("county")
                or address.get("city")
                or address.get("state")
                or address.get("region")
                or address.get("municipality")
                or address.get("district")
                or ""
            ),
            "country": address.get(
                "country",
                ""
            ),
            "formatted_address": data.get(
                "display_name",
                ""
            )
        }

    def enrich_hotel(self, hotel: dict):
        """
        Enrich one hotel record.

        Parameters
        ----------
        hotel : dict

        Returns
        -------
        dict
        """

        latitude = hotel.get("latitude")
        longitude = hotel.get("longitude")

        if latitude is None or longitude is None:
            return hotel

        logger.info(
            f"Reverse geocoding {hotel.get('hotel_name')}"
        )

        result = self.reverse_geocode(
            latitude,
            longitude
        )

        if result is None:
            return hotel

        hotel["county_or_region"] = (
            result["county_or_region"]
            or hotel.get("location", "")
            )
        hotel["country"] = result["country"]
        hotel["formatted_address"] = result["formatted_address"]

        return hotel