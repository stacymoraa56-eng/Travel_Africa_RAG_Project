import json
import os
import chromadb
from chromadb.utils import embedding_functions


def ingest_to_chroma():
    """Reads enriched_hotels.json and populates ChromaDB with vector embeddings and metadata."""
    input_path = "data/enriched_hotels.json"

    if not os.path.exists(input_path):
        print(f"Error: Enriched dataset not found at {input_path}. Run enrich_dataset.py first.")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        hotels = json.load(f)

    if not hotels:
        print("No hotel records found to ingest.")
        return

    # Initialize persistent client
    client = chromadb.PersistentClient(path="chroma_db")

    # SentenceTransformer embedding function
    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    # Standardized collection name
    collection = client.get_or_create_collection(
        name="east_africa_hotels",
        embedding_function=embedding_func
    )

    documents = []
    metadatas = []
    ids = []

    for idx, hotel in enumerate(hotels):
        amenities = hotel.get("amenities", [])
        amenities_str = ", ".join(amenities) if isinstance(amenities, list) else str(amenities)

        attractions = hotel.get("nearby_attractions", [])
        attractions_str = ", ".join(attractions) if isinstance(attractions, list) else str(attractions)

        # Context document for vector similarity search
        doc_text = (
            f"Hotel Name: {hotel['hotel_name']}. "
            f"Location: {hotel['location']}, {hotel['country']}. "
            f"Region: {hotel.get('county_or_region', '')}. "
            f"Description: {hotel['description']} "
            f"Price Range: {hotel['price_range']}. "
            f"Amenities: {amenities_str}. "
            f"Nearby Attractions: {attractions_str}."
        )

        # ChromaDB metadatas only accept primitive types (str, int, float, bool)
        metadata = {
            "hotel_name": str(hotel.get("hotel_name", "")),
            "location": str(hotel.get("location", "")),
            "country": str(hotel.get("country", "")),
            "latitude": float(hotel.get("latitude", -1.286389)),
            "longitude": float(hotel.get("longitude", 36.817223)),
            "description": str(hotel.get("description", "")),
            "price_range": str(hotel.get("price_range", "Mid-Range")),
            "rating": float(hotel.get("rating", 4.5)),
            "amenities": amenities_str,
            "website_url": str(hotel.get("website_url", "https://example.com")),
        }

        doc_id = f"hotel_{idx}_{hotel['location'].lower().replace(' ', '_')}"

        documents.append(doc_text)
        metadatas.append(metadata)
        ids.append(doc_id)

    # Upsert into ChromaDB
    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"Successfully ingested {len(documents)} hotel records into ChromaDB collection 'east_africa_hotels'.")


if __name__ == "__main__":
    ingest_to_chroma()