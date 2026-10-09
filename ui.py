import os
import re
import folium
from folium.plugins import MarkerCluster
import requests
import streamlit as st
from streamlit_folium import st_folium

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Karibu! East Africa Vacation & Beach Advisor",
    page_icon="🏖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")


# --- HELPER FUNCTIONS ---
def clean_price_string(price_str: str) -> str:
    """Cleans duplicate price strings like 'Luxury (150-\n150-350)'."""
    if not price_str:
        return "Mid-Range ($100 - $250)"
    cleaned = re.sub(r"\s+", " ", str(price_str)).strip()
    match = re.search(r"(\$?\d+[\s-]*\$?\d+)", cleaned)
    if match:
        range_val = match.group(1).replace(" ", "")
        if not range_val.startswith("$"):
            range_val = f"${range_val}"
        if "luxury" in cleaned.lower():
            return f"Luxury ({range_val})"
        elif "budget" in cleaned.lower():
            return f"Budget ({range_val})"
        return f"Mid-Range ({range_val})"
    return cleaned


def fetch_hotels(query: str = "", country: str = "", city: str = ""):
    """Fetches hotel records from the backend FastAPI / ChromaDB API."""
    endpoint = f"{BACKEND_URL.rstrip('/')}/search"
    payload = {"query": query or "luxury resort beach lodge stay", "country": country, "city": city}
    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        if response.status_code == 200:
            return response.json().get("results", [])
        return []
    except Exception:
        return []


def render_east_africa_map(hotels: list):
    """Renders an interactive Folium map displaying stay locations."""
    if not hotels:
        return

    m = folium.Map(
        location=[-2.5, 36.5],
        zoom_start=6,
        tiles="CartoDB voyager",
    )
    marker_cluster = MarkerCluster().add_to(m)

    for hotel in hotels:
        lat = hotel.get("latitude")
        lng = hotel.get("longitude")
        name = hotel.get("hotel_name", "Stay")
        city = hotel.get("location", "")
        country = hotel.get("country", "")
        rating = hotel.get("rating", 4.5)
        price = clean_price_string(hotel.get("price_range", ""))

        if lat and lng:
            popup_html = f"""
            <div style="font-family: sans-serif; width: 210px;">
                <h4 style="margin: 0 0 4px 0; color: #b45309;">{name}</h4>
                <p style="margin: 0; font-size: 13px; color: #475569;">📍 {city}, {country}</p>
                <p style="margin: 6px 0 0 0; font-size: 12px; color: #0d9488;"><b>⭐ {rating}</b> | {price}</p>
            </div>
            """
            folium.Marker(
                location=[lat, lng],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=f"{name} ({city})",
                icon=folium.Icon(color="orange", icon="sun", prefix="fa"),
            ).add_to(marker_cluster)

    st_folium(m, width="100%", height=460, returned_objects=[])


# --- WARM BEACH VACATION CSS STYLING ---
st.markdown(
    """
    <style>
    /* Warm Sunset Gradient Background */
    .stApp {
        background: linear-gradient(180deg, #fffbeb 0%, #fef3c7 35%, #ffedd5 70%, #fef3c7 100%);
        color: #1e293b;
        font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: rgba(255, 251, 235, 0.9) !important;
        border-right: 1px solid #fde68a;
    }

    /* Warm Welcome Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 50%, #ea580c 100%);
        border-radius: 24px;
        padding: 2.5rem 2rem;
        text-align: center;
        color: #ffffff;
        box-shadow: 0 10px 25px -5px rgba(217, 119, 6, 0.3);
        margin-bottom: 2rem;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        font-weight: 500;
        opacity: 0.95;
    }

    /* Hotel Card Styling */
    .vacation-card {
        background: #ffffff;
        border: 1px solid #fde68a;
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(217, 119, 6, 0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .vacation-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(217, 119, 6, 0.15);
    }

    .card-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #92400e;
        margin-bottom: 0.2rem;
    }

    .card-location {
        color: #0d9488;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.75rem;
    }

    .badge-pill {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.4rem;
        margin-bottom: 0.5rem;
    }

    .badge-rating { background: #fef3c7; color: #d97706; border: 1px solid #fde68a; }
    .badge-price { background: #ccfbf1; color: #0f766e; border: 1px solid #99f6e4; }
    .badge-amenity { background: #f3f4f6; color: #4b5563; }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #d97706 0%, #ea580c 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.65rem 1.25rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(217, 119, 6, 0.25) !important;
    }

    .stButton>button:hover {
        transform: scale(1.02) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --- HERO WELCOME BANNER ---
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-title">☀️ Jambo! Where do you want to take your next vacation?</div>
        <div class="hero-subtitle">Discover sun-kissed beaches, coastal resorts, and breathtaking safari lodges across Kenya, Tanzania & Uganda.</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# --- SIDEBAR FILTERS ---
st.sidebar.title("🌴 Vacation Filters")
st.sidebar.markdown("---")

country_filter = st.sidebar.selectbox(
    "Select Country",
    options=["All Countries", "Kenya", "Tanzania", "Uganda"],
    index=0,
)

city_options = {
    "All Countries": ["All Cities"],
    "Kenya": ["All Cities", "Diani", "Mombasa", "Watamu", "Malindi", "Lamu", "Maasai Mara", "Naivasha", "Nairobi", "Kisumu"],
    "Tanzania": ["All Cities", "Zanzibar", "Arusha", "Dar es Salaam"],
    "Uganda": ["All Cities", "Kampala"],
}

available_cities = city_options.get(country_filter, ["All Cities"])
city_filter = st.sidebar.selectbox("Select Destination City", options=available_cities, index=0)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Beach Vacation Tip:** Try searching for *'oceanfront resort in Diani with pool'* or *'sunset view stay in Zanzibar'*.")


# --- MAIN SEARCH BAR ---
search_col, btn_col = st.columns([4, 1])

with search_col:
    search_query = st.text_input(
        "Search Preferences",
        placeholder="e.g., Beachfront resort in Zanzibar with pool and spa",
        label_visibility="collapsed",
    )

with btn_col:
    search_clicked = st.button("Find Stays", use_container_width=True)


# --- SESSION STATE & TRIGGER RESOLUTION ---
if "selected_city_trigger" not in st.session_state:
    st.session_state["selected_city_trigger"] = ""

# Determine active filters
active_country = "" if country_filter == "All Countries" else country_filter
active_city = st.session_state["selected_city_trigger"] or ("" if city_filter == "All Cities" else city_filter)

# Fetch data for current view
with st.spinner("Finding your ideal East African vacation stay..."):
    results = fetch_hotels(
        query=search_query if search_query else "luxury beach resort safari lodge stay",
        country=active_country,
        city=active_city,
    )


# --- DISPLAY SECTION ---
if active_city or active_country or search_query or search_clicked:
    # Reset trigger after search renders
    st.session_state["selected_city_trigger"] = ""

    st.markdown("---")
    st.subheader(f"✨ Found {len(results)} Vacation Stays")

    if results:
        view_mode = st.radio(
            "Display View Mode",
            options=["🎴 Card View", "🗺️ Interactive Map"],
            horizontal=True,
            label_visibility="collapsed",
        )

        if view_mode == "🗺️ Interactive Map":
            render_east_africa_map(results)
        else:
            col1, col2 = st.columns(2)
            for idx, hotel in enumerate(results):
                target_col = col1 if idx % 2 == 0 else col2

                name = hotel.get("hotel_name", "Luxury Stay")
                city = hotel.get("location", "East Africa")
                country = hotel.get("country", "")
                desc = hotel.get("description", "A relaxed getaway stay.")
                rating = hotel.get("rating", 4.5)
                price = clean_price_string(hotel.get("price_range", ""))
                amenities = hotel.get("amenities", ["WiFi", "Pool"])
                website = hotel.get("website_url", "#")

                amenity_pills = "".join([f'<span class="badge-pill badge-amenity">{a}</span>' for a in amenities[:4]])

                with target_col:
                    st.markdown(
                        f"""
                        <div class="vacation-card">
                            <div class="card-title">{name}</div>
                            <div class="card-location">📍 {city}, {country}</div>
                            <div>
                                <span class="badge-pill badge-rating">⭐ {rating:.1f}</span>
                                <span class="badge-pill badge-price">🏷️ {price}</span>
                            </div>
                            <p style="color: #475569; font-size: 0.95rem; margin: 0.75rem 0;">{desc}</p>
                            <div>{amenity_pills}</div>
                            <div style="margin-top: 1rem;">
                                <a href="{website}" target="_blank" style="text-decoration: none; color: #ea580c; font-weight: 700; font-size: 0.9rem;">
                                    View Resort Details & Book →
                                </a>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
    else:
        st.warning("No stays found for this exact filter. Ensure `uvicorn app:app --port 8000` is running in another terminal window!")

else:
    # --- DEFAULT LANDING PAGE & COUNTRY EXPANDERS ---
    st.markdown("---")
    st.markdown("### 🏖️ Explore Regional Destination Hubs")
    st.write("Click on any country icon below to expand and view top vacation cities:")

    # 1. Kenya Expander
    with st.expander("🇰🇪 **Kenya - Coastal Beaches & Wildlife Havens**", expanded=True):
        st.write("Select a Kenyan city to view available stays:")
        k_cols = st.columns(4)
        kenyan_cities = ["Diani", "Mombasa", "Watamu", "Malindi", "Lamu", "Maasai Mara", "Naivasha", "Kisumu"]
        for i, c_name in enumerate(kenyan_cities):
            if k_cols[i % 4].button(f"📍 {c_name}", key=f"btn_kenya_{c_name}"):
                st.session_state["selected_city_trigger"] = c_name
                st.rerun()

    # 2. Tanzania Expander
    with st.expander("🇹🇿 **Tanzania - Zanzibar Spice Island & Safari Gateways**"):
        st.write("Select a Tanzanian city to view available stays:")
        t_cols = st.columns(3)
        tanzanian_cities = ["Zanzibar", "Arusha", "Dar es Salaam"]
        for i, c_name in enumerate(tanzanian_cities):
            if t_cols[i % 3].button(f"📍 {c_name}", key=f"btn_tz_{c_name}"):
                st.session_state["selected_city_trigger"] = c_name
                st.rerun()

    # 3. Uganda Expander
    with st.expander("🇺🇬 **Uganda - Pearl of Africa & Lake Victoria Resorts**"):
        st.write("Select a Ugandan destination city:")
        u_cols = st.columns(2)
        ugandan_cities = ["Kampala"]
        for i, c_name in enumerate(ugandan_cities):
            if u_cols[i % 2].button(f"📍 {c_name}", key=f"btn_ug_{c_name}"):
                st.session_state["selected_city_trigger"] = c_name
                st.rerun()

    # Show featured default stays below the expanders on landing
    if results:
        st.markdown("<br>#### Recommended Stays Across East Africa", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        for idx, hotel in enumerate(results[:6]):
            target_col = col1 if idx % 2 == 0 else col2
            name = hotel.get("hotel_name", "Luxury Stay")
            city = hotel.get("location", "East Africa")
            country = hotel.get("country", "")
            desc = hotel.get("description", "A relaxed getaway stay.")
            rating = hotel.get("rating", 4.5)
            price = clean_price_string(hotel.get("price_range", ""))
            website = hotel.get("website_url", "#")

            with target_col:
                st.markdown(
                    f"""
                    <div class="vacation-card">
                        <div class="card-title">{name}</div>
                        <div class="card-location">📍 {city}, {country}</div>
                        <div>
                            <span class="badge-pill badge-rating">⭐ {rating:.1f}</span>
                            <span class="badge-pill badge-price">🏷️ {price}</span>
                        </div>
                        <p style="color: #475569; font-size: 0.95rem; margin: 0.75rem 0;">{desc}</p>
                        <div style="margin-top: 0.75rem;">
                            <a href="{website}" target="_blank" style="text-decoration: none; color: #ea580c; font-weight: 700; font-size: 0.9rem;">
                                View Resort Details & Book →
                            </a>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )