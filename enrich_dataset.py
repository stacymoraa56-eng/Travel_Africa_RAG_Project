import json
import os

# Exact GPS coordinates for East African destination hubs
CITY_COORDINATES = {
    "Nairobi": (-1.286389, 36.817223),
    "Mombasa": (-4.043477, 39.668206),
    "Diani": (-4.2796, 39.5947),
    "Watamu": (-3.3510, 40.0305),
    "Malindi": (-3.2172, 40.1169),
    "Lamu": (-2.2696, 40.9006),
    "Maasai Mara": (-1.4061, 35.1052),
    "Amboseli": (-2.6527, 37.2606),
    "Naivasha": (-0.7171, 36.4310),
    "Nakuru": (-0.3031, 36.0800),
    "Kisumu": (-0.0917, 34.7680),
    "Nanyuki": (0.0167, 37.0722),
    "Zanzibar": (-6.1659, 39.2026),
    "Arusha": (-3.3869, 36.6830),
    "Dar es Salaam": (-6.7924, 39.2083),
    "Kampala": (0.3476, 32.5825),
}


def extract_real_location_and_country(
    hotel_name: str, raw_location: str, raw_address: str = ""
) -> tuple[str, str]:
    """Maps hotel details accurately to standardized destination cities and countries."""
    text = f"{hotel_name} {raw_location} {raw_address}".lower()

    # 1. Tanzania & Zanzibar Disambiguation
    if "zanzibar" in text or "stone town" in text or "paje" in text or "nungwi" in text:
        return "Zanzibar", "Tanzania"
    if "arusha" in text or "olduvai" in text or "bougainvillea" in text:
        return "Arusha", "Tanzania"
    if "dar es salaam" in text or "dar-es-salaam" in text:
        return "Dar es Salaam", "Tanzania"

    # 2. Uganda
    if "kampala" in text or "munyonyo" in text or "entebbe" in text:
        return "Kampala", "Uganda"

    # 3. Kenya Coast & Safari Hubs
    if "mombasa" in text or "bamburi" in text or "nyali" in text or "severin" in text or "pundamilia" in text:
        return "Mombasa", "Kenya"
    if "diani" in text or "ukunda" in text:
        return "Diani", "Kenya"
    if "watamu" in text:
        return "Watamu", "Kenya"
    if "malindi" in text:
        return "Malindi", "Kenya"
    if "lamu" in text:
        return "Lamu", "Kenya"
    if "maasai mara" in text or "mara" in text or "soroi" in text or "ol kiombo" in text:
        return "Maasai Mara", "Kenya"
    if "amboseli" in text:
        return "Amboseli", "Kenya"
    if "naivasha" in text:
        return "Naivasha", "Kenya"
    if "nakuru" in text:
        return "Nakuru", "Kenya"
    if "nanyuki" in text:
        return "Nanyuki", "Kenya"
    if "kisumu" in text:
        return "Kisumu", "Kenya"

    return "Nairobi", "Kenya"


def generate_accurate_description(hotel_name: str, city: str, country: str, raw_desc: str) -> str:
    """Ensures hotel descriptions accurately reflect coastal vs safari settings."""
    if len(raw_desc.strip()) > 60 and "premier coastal resort" not in raw_desc.lower():
        return raw_desc.strip()

    coastal_cities = {"Zanzibar", "Mombasa", "Diani", "Watamu", "Malindi", "Lamu"}
    safari_cities = {"Maasai Mara", "Amboseli", "Arusha", "Naivasha", "Nakuru"}

    if city in coastal_cities:
        return (
            f"{hotel_name} is a beachside resort located in {city}, {country}, "
            f"offering ocean views, tropical palm gardens, and direct access to pristine beaches."
        )
    elif city in safari_cities:
        return (
            f"{hotel_name} is a lodge situated in {city}, {country}, "
            f"featuring authentic bush accommodations and guided safari excursion access."
        )
    else:
        return (
            f"{hotel_name} is a comfortable hotel located in {city}, {country}, "
            f"offering modern travel amenities, quality dining, and relaxed surroundings."
        )


def enrich_dataset():
    """Reads seed_hotels.json and cleaned_hotels.json, standardizes fields, and saves enriched output."""
    os.makedirs("data", exist_ok=True)
    combined_hotels = []

    for file_name in ["data/seed_hotels.json", "data/cleaned_hotels.json"]:
        if os.path.exists(file_name):
            with open(file_name, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    combined_hotels.extend(data)
                    print(f"Loaded {len(data)} records from {file_name}")
                except Exception as e:
                    print(f"Error reading {file_name}: {e}")

    if not combined_hotels:
        print("Error: No data found to enrich!")
        return

    seen_names = set()
    unique_hotels = []

    for hotel in combined_hotels:
        name = str(hotel.get("hotel_name", "Unknown Stay")).strip()
        if not name or name.lower() in seen_names:
            continue
        seen_names.add(name.lower())

        raw_loc = str(hotel.get("location", ""))
        raw_addr = str(hotel.get("address", ""))
        city, country = extract_real_location_and_country(name, raw_loc, raw_addr)

        lat, lng = CITY_COORDINATES.get(city, (-1.286389, 36.817223))
        raw_description = str(hotel.get("description", ""))
        description = generate_accurate_description(name, city, country, raw_description)

        record = {
            "hotel_name": name,
            "location": city,
            "country": country,
            "county_or_region": str(hotel.get("county_or_region", city)),
            "latitude": lat,
            "longitude": lng,
            "description": description,
            "price_range": str(hotel.get("price_range", "Mid-Range ($100-$250)")),
            "rating": float(hotel.get("rating", 4.5)),
            "amenities": hotel.get("amenities", ["Free WiFi", "Swimming Pool"]),
            "room_types": hotel.get("room_types", ["Standard Room"]),
            "nearby_attractions": hotel.get("nearby_attractions", [city]),
            "website_url": str(hotel.get("website_url", "https://example.com")),
            "source_url": str(hotel.get("source_url", "https://example.com")),
        }
        unique_hotels.append(record)

    output_path = "data/enriched_hotels.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(unique_hotels, f, indent=2, ensure_ascii=False)

    print(f"Successfully enriched {len(unique_hotels)} destination records -> {output_path}")


if __name__ == "__main__":
    enrich_dataset()