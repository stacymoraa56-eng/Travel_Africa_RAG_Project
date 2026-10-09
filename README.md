# 🏖️ East Africa Travel & Hotel RAG Advisor

# Karibu! East Africa Vacation & Beach Advisor 

![Karibu! East Africa Vacation & Beach Advisor - Landing Page](Travel_Africa_Landing_Page.png)

An AI-powered travel advisor helping users explore accommodation options across East Africa.


##  Project Overview

Finding suitable accommodation across East Africa often requires searching multiple websites and comparing fragmented information. This project addresses that challenge by collecting accommodation data from selected travel and tourism websites, transforming it into a structured dataset, and making it searchable through semantic retrieval.

The application allows users to explore accommodation using descriptive queries, apply geographic filters, and view matching properties through interactive cards and a map.

### Key Features

* Natural-language accommodation search using semantic similarity.
* Country and destination filtering.
* Geographic enrichment and interactive map visualization.
* Structured accommodation data processed through a multi-stage pipeline.
* FastAPI backend connected to a Streamlit dashboard.
* Deployment on Render.

##  From Web Scraping to Deployment

The project was developed through a series of connected data engineering and AI development stages.

### 1. Data Collection and Scraping

Accommodation information was collected from selected East African travel and tourism websites using Python-based web scraping tools, including BeautifulSoup.

The initial collection produced **109 accommodation records**. These records provided the raw input for the downstream data processing pipeline.

### 2. Data Cleaning and Standardization

The raw records were cleaned to improve consistency and prepare them for indexing. The process addressed data quality issues such as inconsistent fields, missing information, and formatting differences.

Following cleaning, the dataset contained **99 accommodation records**, providing a more consistent foundation for enrichment and retrieval.

### 3. Geographic Enrichment and Validation

The cleaned records were enriched with standardized location information, geographic coordinates where available, and contextual descriptions.

Additional validation helped improve location consistency and reduce geographic ambiguity across destinations, including locations with similar names.

The resulting enriched dataset was prepared for semantic indexing.

### 4. Embeddings and Vector Database

The enriched accommodation descriptions were converted into numerical vector embeddings using SentenceTransformers and the `all-MiniLM-L6-v2` model.

The embeddings and associated accommodation information were indexed in ChromaDB, enabling semantic similarity searches against the collected data.

### 5. Retrieval API and Interactive Dashboard

A FastAPI backend handles search requests, queries the vector database, and applies supported country and location filters.

A Streamlit frontend provides the user-facing experience, including accommodation cards, destination filters, and interactive maps built with Folium.

### 6. Deployment

The application is configured for deployment on Render, connecting the frontend and backend to make the accommodation discovery experience accessible through the web.

The deployed services require the correct API configuration and access to a valid ChromaDB index.

##  Architecture

```text
Travel & Tourism Websites
           |
           v
    Web Scraping
           |
           v
   109 Raw Records
           |
           v
 Data Cleaning & Standardization
           |
           v
    99 Cleaned Records
           |
           v
 Geographic Enrichment & Validation
           |
           v
    Enriched Dataset
           |
           v
 SentenceTransformers Embeddings
           |
           v
        ChromaDB
           |
           v
       FastAPI API
           |
           v
     Streamlit Dashboard
      + Interactive Map
           |
           v
      Render Deployment
```

**RAG implementation note:** The current architecture provides the data preparation and semantic retrieval components used in RAG applications. A complete generative RAG workflow additionally passes retrieved context to a language model to generate grounded natural-language responses.

##  Technology Stack

| Technology               | Purpose                               |
| ------------------------ | ------------------------------------- |
| Python, BeautifulSoup    | Web scraping and data collection      |
| Pandas, Regex            | Data cleaning and standardization     |
| SentenceTransformers     | Text embeddings                       |
| ChromaDB                 | Vector storage and semantic retrieval |
| FastAPI, Uvicorn         | Backend API                           |
| Pydantic                 | Request and data validation           |
| Streamlit                | Interactive user interface            |
| Folium, Streamlit-Folium | Geographic visualization              |
| Render                   | Application deployment                |

##  Project Structure

```text
Travel_Africa_RAG/
├── app.py                    # FastAPI backend and retrieval
├── ui.py                     # Streamlit dashboard
├── enrich_dataset.py         # Geographic and contextual enrichment
├── ingest_chroma.py          # Embedding generation and indexing
├── requirements.txt          # Python dependencies
├── data/
│   ├── cleaned_hotels.json   # 99 cleaned records
│   └── enriched_hotels.json  # Enriched accommodation dataset
└── data_collection/
    ├── scraper.py            # Scraper orchestration
    ├── cleaner.py            # Data cleaning
    └── html/                 # Site-specific scraping modules
```

##  Running Locally

**Prerequisites:** Python and Git.

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd Travel_Africa_RAG
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Build the vector index

Ensure the enriched dataset is available, then run:

```bash
python ingest_chroma.py
```

### 4. Start the backend

```bash
uvicorn app:app --reload --port 8000
```

API documentation: `http://localhost:8000/docs`

### 5. Start the frontend

In a separate terminal:

```bash
streamlit run ui.py
```

Ensure the frontend is configured to communicate with the running FastAPI backend.


## Live Demo

[Explore the live application](https://travel-africa-project-rag.onrender.com/)

An AI-powered travel discovery application that helps users find accommodation across **Kenya, Tanzania, and Uganda** using natural-language search.

The project combines web scraping, data cleaning, geographic enrichment, semantic search, and an interactive dashboard to make accommodation discovery across 16 key destination hubs more accessible.

**Tech Stack:** Python · BeautifulSoup · Pandas · SentenceTransformers · ChromaDB · FastAPI · Streamlit · Folium · Render


##  Future Improvements

* Integrate a generative language model for complete RAG-based responses.
* Automate data collection, validation, and index updates.
* Improve retrieval ranking and accommodation comparisons.
* Expand accommodation coverage across additional East African destinations.
* Introduce stronger retrieval evaluation and data-quality monitoring.

##  Project Focus

This project demonstrates the integration of **web scraping, data engineering, semantic search, vector databases, API development, interactive visualization, and cloud deployment** into a practical AI-powered travel discovery application.
