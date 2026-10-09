import chromadb
from chromadb.utils import embedding_functions
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="East Africa Travel Advisor API")

# Enable CORS for local Streamlit UI and Render deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChromaDB Persistent Client
CHROMA_PATH = "chroma_db"
client = chromadb.PersistentClient(path=CHROMA_PATH)

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.get_or_create_collection(
    name="east_africa_hotels",
    embedding_function=embedding_func
)


class SearchRequest(BaseModel):
    query: Optional[str] = "luxury beach resort safari lodge stay"
    country: Optional[str] = ""
    city: Optional[str] = ""


@app.get("/")
def read_root():
    return {"status": "online", "message": "East Africa Travel API is running!"}


@app.post("/search")
def search_hotels(req: SearchRequest):
    """Executes vector similarity search with optional country and city metadata filters."""
    query_text = req.query.strip() if req.query and req.query.strip() else "luxury beach resort safari lodge stay"

    # Build Chroma metadata filter
    where_filter = {}
    if req.country and req.country.strip():
        where_filter["country"] = req.country.strip()
    if req.city and req.city.strip():
        where_filter["location"] = req.city.strip()

    kwargs = {"query_texts": [query_text], "n_results": 10}

    if where_filter:
        if len(where_filter) == 1:
            kwargs["where"] = where_filter
        else:
            kwargs["where"] = {"$and": [{k: v} for k, v in where_filter.items()]}

    try:
        results = collection.query(**kwargs)

        hotels = []
        if results and results.get("metadatas") and len(results["metadatas"]) > 0:
            for meta in results["metadatas"][0]:
                raw_amenities = meta.get("amenities", "")
                if isinstance(raw_amenities, str):
                    amenities_list = [a.strip() for a in raw_amenities.split(",") if a.strip()]
                else:
                    amenities_list = raw_amenities

                hotels.append({
                    "hotel_name": meta.get("hotel_name", "Luxury Stay"),
                    "location": meta.get("location", "East Africa"),
                    "country": meta.get("country", ""),
                    "latitude": float(meta.get("latitude", -1.286389)),
                    "longitude": float(meta.get("longitude", 36.817223)),
                    "description": meta.get("description", "A comfortable vacation stay."),
                    "price_range": meta.get("price_range", "Mid-Range ($100-$250)"),
                    "rating": float(meta.get("rating", 4.5)),
                    "amenities": amenities_list,
                    "website_url": meta.get("website_url", "https://example.com"),
                })

        return {"results": hotels}

    except Exception as e:
        print(f"ChromaDB Query Error: {e}")
        return {"results": []}