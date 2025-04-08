import streamlit as st
import pandas as pd
import requests
from map_view import show_map_view
from table_view import show_table_view
from gallery_view import show_gallery_view

st.set_page_config(layout="wide")  # Use full width of the screen

# Custom CSS for horizontal navigation
st.markdown("""
<style>
    .horizontal-nav {
        display: flex;
        justify-content: space-around;
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .nav-item {
        text-align: center;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    .nav-item-active {
        background-color: #4e8cff;
        color: white;
    }
    .nav-item:hover:not(.nav-item-active) {
        background-color: #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

st.title('Webcam Locations 🗺️📷')

# Define navigation options
nav_options = ["Map View", "Table View", "Image Gallery"]

# Create horizontal navigation bar
cols = st.columns(len(nav_options))
for i, option in enumerate(nav_options):
    with cols[i]:
        if 'nav_selection' not in st.session_state:
            st.session_state.nav_selection = "Map View"  # Default view
        
        if st.session_state.nav_selection == option:
            st.markdown(f"""
            <div class="horizontal-nav">
                <div class="nav-item nav-item-active">{option}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Create a clickable navigation item
            if st.button(option, key=f"nav_{option}"):
                st.session_state.nav_selection = option
                st.rerun()

@st.cache_data(ttl=3600)
def fetch_webcam_data():
    url = "https://tourism.api.opendatahub.com/v1/WebcamInfo?pagesize=2000&removenullvalues=false&getasidarray=false"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

try:
    data = fetch_webcam_data()
    webcams = data.get('Items', [])

    coords = []

    for webcam in webcams:
        gps_info = webcam.get('GpsInfo')
        image_gallery = webcam.get('ImageGallery')
        detail = webcam.get('Detail', {})
        lang_info = next(iter(detail.values()), {})
        language = lang_info.get('Language', 'unknown')

        if gps_info and image_gallery:
            position = gps_info[0]
            lat = position.get('Latitude')
            lon = position.get('Longitude')
            img_url = image_gallery[0].get('ImageUrl') if image_gallery else None
            title = webcam.get('Shortname', 'Unnamed Webcam')

            if lat and lon and img_url:
                coords.append({
                    'title': title,
                    'language': language,
                    'lat': lat,
                    'lon': lon,
                    'image': img_url
                })

    if coords:
        df_coords = pd.DataFrame(coords)

        # Display content based on navigation selection
        if st.session_state.nav_selection == "Map View":
            show_map_view(df_coords)
        elif st.session_state.nav_selection == "Table View":
            show_table_view(df_coords)
        elif st.session_state.nav_selection == "Image Gallery":
            show_gallery_view(df_coords)

    else:
        st.warning('No webcams with coordinates and images found.')

except requests.exceptions.RequestException as e:
    st.error(f"Error fetching data: {e}")