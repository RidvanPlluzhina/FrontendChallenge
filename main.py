import streamlit as st
import requests
import pandas as pd
import pydeck as pdk

st.set_page_config(layout="wide")  # Use full width of the screen
st.title('Webcam Locations 🗺️📷')

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

        # === Responsive Styled Table ===
        st.subheader('Webcam Table')
        styled_df = df_coords[['title', 'language', 'lat', 'lon']].style.set_properties(**{
            'text-overflow': 'ellipsis',
            'overflow': 'hidden',
            'white-space': 'nowrap'
        })
        st.dataframe(styled_df, hide_index=True)

        # Webcam selection
        st.subheader("Select a webcam to view the image:")
        selected_title = st.selectbox("Choose a webcam", df_coords['title'])
        selected_row = df_coords[df_coords['title'] == selected_title].iloc[0]
        selected_img = selected_row['image']
        st.image(selected_img, caption=selected_title, use_container_width=True)

    else:
        st.warning('No webcams with coordinates and images found.')

except requests.exceptions.RequestException as e:
    st.error(f"Error fetching data: {e}")
