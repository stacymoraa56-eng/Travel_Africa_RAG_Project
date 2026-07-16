"""
hotel_cleaner.py

Travel Africa RAG
-----------------
Cleans raw hotel data collected from:
- OpenStreetMap (Overpass API)
- Magical Kenya
- Future hotel data sources

Output:
    data/cleaned/hotels_clean.csv
"""

import os
import re
import pandas as pd

# ==========================================================
# CONFIGURATION
# ==========================================================

INPUT_FILE = "data/raw/hotels_raw.csv"
OUTPUT_FILE = "data/cleaned/hotels_clean.csv"

SUPPORTED_LOCATIONS = {
    # Kenya
    "Nairobi",
    "Mombasa",
    "Diani",
    "Watamu",
    "Malindi",
    "Naivasha",
    "Nakuru",
    "Maasai Mara",
    "Amboseli",
    "Kisumu",
    "Nanyuki",
    "Lamu",

    # Uganda
    "Kampala",

    # Tanzania
    "Arusha",
    "Dar es Salaam",
    "Zanzibar",
    "Stone Town",

    # Placeholder from Magical Kenya
    "Add Listing"
}

NON_HOTEL_KEYWORDS = [
    "restaurant",
    "cafe",
    "bar",
    "club",
    "mall",
    "market",
    "shop",
    "boom mart",
    "hospital",
    "school",
    "office"
]

PLACEHOLDER_IMAGE = "KTB-Lock-Up"
PLACEHOLDER_WEBSITE = "ktb.go.ke"


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def clean_text(value):
    """Remove unnecessary whitespace."""

    if pd.isna(value):
        return ""

    value = str(value)
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def normalize_phone(phone):
    """Standardize phone numbers."""

    if pd.isna(phone):
        return ""

    phone = str(phone)

    phone = (
        phone.replace(" ", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
    )

    return phone


# ==========================================================
# CLEANING FUNCTIONS
# ==========================================================

def remove_exact_duplicates(df):
    """Remove rows that are identical across every column."""

    before = len(df)

    df = df.drop_duplicates()

    removed = before - len(df)

    return df, removed


def remove_duplicate_hotels(df):
    """
    Remove duplicate hotels using
    hotel name + location.
    """

    before = len(df)

    df["hotel_name_lower"] = (
        df["hotel_name"]
        .fillna("")
        .str.lower()
        .str.strip()
    )

    df["location_lower"] = (
        df["location"]
        .fillna("")
        .str.lower()
        .str.strip()
    )

    df = df.drop_duplicates(
        subset=["hotel_name_lower", "location_lower"]
    )

    df = df.drop(
        columns=["hotel_name_lower", "location_lower"]
    )

    removed = before - len(df)

    return df, removed


def remove_unknown_hotels(df):
    """Remove placeholder hotel entries."""

    before = len(df)

    df = df[
        ~df["hotel_name"]
        .fillna("")
        .str.lower()
        .str.contains("unknown hotel")
    ]

    removed = before - len(df)

    return df, removed


def remove_non_hotels(df):
    """Remove restaurants, cafes and other businesses."""

    before = len(df)

    pattern = "|".join(NON_HOTEL_KEYWORDS)

    df = df[
        ~df["hotel_name"]
        .fillna("")
        .str.lower()
        .str.contains(pattern)
    ]

    removed = before - len(df)

    return df, removed


def remove_out_of_scope_locations(df):
    """Keep only supported project destinations."""

    before = len(df)

    df = df[
        df["location"]
        .fillna("")
        .isin(SUPPORTED_LOCATIONS)
    ]

    removed = before - len(df)

    return df, removed


def remove_placeholder_images(df):
    """Clear placeholder image references."""

    removed = 0

    if "image_url" not in df.columns:
        return df, removed

    for index, value in df["image_url"].fillna("").items():

        if PLACEHOLDER_IMAGE.lower() in value.lower():

            df.at[index, "image_url"] = ""
            removed += 1

    return df, removed


def remove_placeholder_websites(df):
    """Clear placeholder website links."""

    removed = 0

    if "website_url" not in df.columns:
        return df, removed

    for index, value in df["website_url"].fillna("").items():

        if PLACEHOLDER_WEBSITE in value.lower():

            df.at[index, "website_url"] = ""
            removed += 1

    return df, removed


def normalize_categories(df):
    """Standardize accommodation categories."""

    if "hotel_category" not in df.columns:
        return df

    replacements = {
        "hotel": "Hotel",
        "accommodation": "Hotel",
        "resort": "Resort",
        "camp": "Camp",
        "lodge": "Lodge",
        "villa": "Villa",
        "guest house": "Guest House",
        "hostel": "Hostel",
        "apartment": "Apartment",
        "cottage": "Cottage",
        "": ""
    }

    df["hotel_category"] = (
        df["hotel_category"]
        .fillna("")
        .str.lower()
        .replace(replacements)
    )

    return df


def normalize_text_columns(df):
    """Clean whitespace from all text columns."""

    for column in df.columns:
        df[column] = df[column].apply(clean_text)

    return df


def normalize_phone_numbers(df):
    """Normalize contact numbers."""

    if "contact_information" in df.columns:

        df["contact_information"] = (
            df["contact_information"]
            .apply(normalize_phone)
        )

    return df


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("Loading raw hotel data...")

    df = pd.read_csv(INPUT_FILE)

    raw_records = len(df)

    # Standardization
    df = normalize_text_columns(df)
    df = normalize_phone_numbers(df)

    # Cleaning
    df, exact_removed = remove_exact_duplicates(df)
    df, duplicate_removed = remove_duplicate_hotels(df)
    df, unknown_removed = remove_unknown_hotels(df)
    df, nonhotel_removed = remove_non_hotels(df)
    df, scope_removed = remove_out_of_scope_locations(df)

    # Cleanup
    df, image_removed = remove_placeholder_images(df)
    df, website_removed = remove_placeholder_websites(df)

    df = normalize_categories(df)

    final_records = len(df)
    total_removed = raw_records - final_records

    # Save cleaned dataset
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    # Summary
    print("\n" + "=" * 60)
    print("HOTEL CLEANING COMPLETE")
    print("=" * 60)

    print(f"Raw records                  : {raw_records}")
    print(f"Final records                : {final_records}")
    print(f"Total rows removed           : {total_removed}")

    print("\nRemoval Summary")
    print("-" * 60)
    print(f"Exact duplicates             : {exact_removed}")
    print(f"Duplicate hotel names        : {duplicate_removed}")
    print(f"Unknown hotels               : {unknown_removed}")
    print(f"Non-hotels                   : {nonhotel_removed}")
    print(f"Out-of-scope locations       : {scope_removed}")

    print("\nFields Cleaned")
    print("-" * 60)
    print(f"Placeholder images cleared   : {image_removed}")
    print(f"Placeholder websites cleared : {website_removed}")

    print("\nSaved cleaned dataset to:")
    print(f"{OUTPUT_FILE}")


if __name__ == "__main__":
    main()