import streamlit as st
import requests
import pandas as pd

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

    st.subheader('Webcam Gallery')
    # Filter functionality
    languages = ['All'] + sorted(df_coords['language'].unique().tolist())
    selected_language = st.selectbox("Filter by language", languages)

    if selected_language != 'All':
        display_df = df_coords[df_coords['language'] == selected_language]
    else:
        display_df = df_coords

    # Pagination for gallery
    items_per_page = 12  # 4 rows of 3 images
    total_pages = (len(display_df) - 1) // items_per_page + 1

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if 'gallery_page' not in st.session_state:
            st.session_state.gallery_page = 1
        
        page = st.slider("Gallery Page", 1, max(1, total_pages), st.session_state.gallery_page, key="gallery_slider")
        st.session_state.gallery_page = page

    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, len(display_df))

    # Display as grid with 3 columns
    display_subset = display_df.iloc[start_idx:end_idx]
    cols = st.columns(3)

    for i, (_, row) in enumerate(display_subset.iterrows()):
        with cols[i % 3]:
            st.image(row['image'], caption=row['title'], use_container_width=True)
            with st.expander("Location Details"):
                st.write(f"**Language:** {row['language']}")
                st.write(f"**Coordinates:** {row['lat']:.4f}, {row['lon']:.4f}")
                
                # Add a "View on Map" link that switches to map view and centers on this webcam
                if st.button(f"View on Map", key=f"map_btn_{i}"):
                    # Store coordinates to center map on this webcam when switching to map view
                    st.session_state.center_lat = row['lat']
                    st.session_state.center_lon = row['lon']
                    st.session_state.nav_selection = "Map View"
                    st.rerun()

    st.write(f"Showing {start_idx+1}-{end_idx} of {len(display_df)} webcams")

except requests.exceptions.RequestException as e:
    st.error(f"Error fetching data: {e}")