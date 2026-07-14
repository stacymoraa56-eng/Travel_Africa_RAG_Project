# 🌍 Travel Africa RAG Assistant

## Project Overview

Travel Africa RAG Assistant is a Retrieval-Augmented Generation (RAG) application that helps users discover hotels, compare destinations, and plan trips across Kenya and East Africa.

Unlike a traditional chatbot, the assistant answers questions using a curated dataset of real hotels collected from publicly available sources. Retrieved hotel information is supplied to a Large Language Model (LLM), enabling grounded responses with source attribution.

---

# Project Objectives

The project aims to:

* Collect authentic hotel information from publicly available sources.
* Clean and standardize the collected data.
* Build a Retrieval-Augmented Generation (RAG) pipeline.
* Store hotel embeddings in a vector database.
* Provide hotel recommendations and trip planning through a FastAPI backend.
* Connect the backend to the provided Travel Africa frontend template.

---

# Current Project Structure

```text
Travel_Africa_RAG/

│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── data_collection/
│   ├── api/
│   │   ├── base_api.py
│   │   ├── overpass_api.py
│   │   └── nominatim_api.py
│   │
│   ├── html/
│   │   ├── base_scraper.py
│   │   ├── magical_kenya.py
│   │   └── ktb.py
│   │
│   ├── manager.py
│   │
│   └── utils/
│       ├── logger.py
│       ├── helpers.py
│       ├── validators.py
│       └── __init__.py
│
├── tests/
│
├── app/
│
├── templates/
│
├── static/
│
├── requirements.txt
│
└── README.md
```

---

# Technologies Used

## Backend

* Python 3.12
* FastAPI
* Uvicorn

## Data Collection

* Requests
* BeautifulSoup4
* lxml
* OpenStreetMap Overpass API
* OpenStreetMap Nominatim API

## Data Processing

* Pandas

## Planned RAG Components

* LangChain
* ChromaDB
* OpenAI Embeddings
* OpenAI Chat Model

---

# Data Sources

The project uses publicly available data only.

## Active Sources

### OpenStreetMap Overpass API

Purpose:

* Collect hotel names
* Geographic coordinates
* Websites
* Contact information
* Hotel category

Website

https://overpass-api.de/

---

### OpenStreetMap Nominatim API

Purpose:

* Reverse geocode hotel coordinates
* County / Region
* Country
* Formatted Address

Website

https://nominatim.openstreetmap.org/

---

### Magical Kenya

Purpose:

* Hotel descriptions
* Destination information
* Tourism-approved accommodation
* Images
* Nearby attractions

Website

https://magicalkenya.com/

---

## Evaluated Sources

### Kenya Tourism Board

A scraper was developed for the Kenya Tourism Board website. However, due to the current website structure, no consistent hotel listing data could be extracted automatically. The scraper remains available for future updates but is not part of the primary data collection pipeline.

---

### Tourism Regulatory Authority (TRA)

The Tourism Regulatory Authority website was evaluated as a potential source of hotel information.

Although publicly accessible, it primarily provides regulatory information rather than structured hotel listings suitable for Retrieval-Augmented Generation.

For this reason, it is documented but excluded from the production data pipeline.

---

# Data Collection Pipeline

```text
Overpass API
      │
      ▼
Hotel Records
      │
      ▼
Magical Kenya
      │
      ▼
Merge Records
      │
      ▼
Nominatim Enrichment
      │
      ▼
Raw Dataset
```

---

# Ethical Scraping

All scraping follows responsible data collection practices.

Measures implemented include:

* Random browser User-Agent rotation.
* Approximately five-second delay between requests.
* Request logging.
* Graceful error handling.
* Publicly available information only.
* Source URLs retained for traceability.

---

# Expected Dataset

## Raw Dataset

Target:

Approximately **130 hotel records**

Characteristics:

* Duplicate hotels
* Missing descriptions
* Missing prices
* Inconsistent county names
* Different website formats

---

## Clean Dataset

Target:

Approximately **110 hotel records**

Cleaning operations will include:

* Removing duplicate hotels.
* Standardizing county names.
* Standardizing location names.
* Removing invalid records.
* Filling missing values where possible.
* Preparing hotel descriptions for embedding.

---

# Current Progress

## Completed

* Project structure
* Python virtual environment
* Dependency management
* Logging utility
* Base HTML scraper
* Base API client
* Overpass API integration
* Nominatim reverse geocoding
* Magical Kenya scraper
* Kenya Tourism Board scraper
* Data collection architecture

---

## In Progress

* Manager pipeline
* Raw dataset generation

---

## Upcoming

* Data cleaning
* Text chunk generation
* Embedding generation
* ChromaDB vector database
* FastAPI endpoints
* Frontend integration
* Travel itinerary generation
* Source attribution
* Final documentation

---

# Hotel Distribution

The Overpass API currently limits the number of hotels collected from each destination to create a balanced dataset across East Africa.

| Destination   | Target Hotels |
| ------------- | ------------: |
| Nairobi       |             7 |
| Mombasa       |             8 |
| Diani         |             6 |
| Naivasha      |             6 |
| Nakuru        |             5 |
| Maasai Mara   |             6 |
| Amboseli      |             5 |
| Watamu        |             5 |
| Malindi       |             5 |
| Kisumu        |             5 |
| Nanyuki       |             5 |
| Lamu          |             5 |
| Zanzibar      |            10 |
| Arusha        |            10 |
| Kampala       |            10 |
| Dar es Salaam |            10 |

Total target from Overpass:

**108 hotels**

Additional records will be merged from Magical Kenya before the data cleaning stage.

---

# Author

Developed as part of a Retrieval-Augmented Generation (RAG) project using FastAPI, OpenStreetMap APIs, and publicly available tourism data to build a hotel discovery and travel planning assistant for Kenya and East Africa.
