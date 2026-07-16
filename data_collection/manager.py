"""
Travel Africa RAG Assistant
--------------------------------------------------

Module:
    manager.py

Purpose
-------
Coordinates the complete data collection stage of the
Travel Africa RAG project.

The manager is responsible for running all hotel collectors,
enriching the collected data, merging the results into a
single dataset, and exporting the raw hotel records.

This module intentionally preserves duplicate records and
missing values. Data quality improvements are performed in
the cleaning stage.
"""

from pathlib import Path

import pandas as pd

from data_collection.api.overpass_api import OverpassAPI
from data_collection.api.nominatim_api import NominatimAPI
from data_collection.html.magical_kenya import MagicalKenyaScraper
from data_collection.utils.logger import logger


class CollectionManager:

    def __init__(self):

        self.overpass = OverpassAPI()

        self.nominatim = NominatimAPI()

        self.magical = MagicalKenyaScraper()

        self.output_folder = Path("data/raw")

        self.output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

    # ------------------------------------------------------

    def collect_overpass(self):

        logger.info("Starting Overpass collection...")

        hotels = self.overpass.collect_all()

        enriched = []

        for hotel in hotels:

            hotel = self.nominatim.enrich_hotel(hotel)

            enriched.append(hotel)

        logger.info(
            f"Collected {len(enriched)} Overpass hotels."
        )

        return enriched

    # ------------------------------------------------------

    def collect_magical(self):

        logger.info(
            "Starting Magical Kenya collection..."
        )

        hotels = self.magical.scrape()

        logger.info(
            f"Collected {len(hotels)} Magical Kenya hotels."
        )

        return hotels

    # ------------------------------------------------------

    def merge_hotels(self):

        hotels = []

        hotels.extend(
            self.collect_overpass()
        )

        hotels.extend(
            self.collect_magical()
        )

        logger.info(
            f"Total raw hotels: {len(hotels)}"
        )

        return hotels

    # ------------------------------------------------------

    def save_raw_dataset(self, hotels):

        output = self.output_folder / "hotels_raw.csv"

        df = pd.DataFrame(hotels)

        df.to_csv(
            output,
            index=False,
            encoding="utf-8-sig"
        )

        logger.info(
            f"Saved raw dataset to {output}"
        )

    # ------------------------------------------------------

    def run(self):

        hotels = self.merge_hotels()

        self.save_raw_dataset(hotels)

        logger.info(
            "Data collection completed successfully."
        )

        return hotels


if __name__ == "__main__":

    manager = CollectionManager()

    manager.run()