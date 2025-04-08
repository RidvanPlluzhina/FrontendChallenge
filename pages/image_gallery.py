# import streamlit as st
# import requests
# import pandas as pd
# import math

# st.set_page_config(layout="wide")

# @st.cache_data(ttl=3600)
# def fetch_webcam_data():
#     url = "https://tourism.api.opendatahub.com/v1/WebcamInfo?pagesize=2000&removenullvalues=false&getasidarray=false"
#     response = requests.get(url)
#     response.raise_for_status()
#     return response.json()

# try:
#     st.title("Image Gallery")
    
#     data = fetch_webcam_data()
#     webcams = data.get('Items', [])

#     coords = []

#     for webcam in webcams:
#         gps_info = webcam.get('GpsInfo')
#         image_gallery = webcam.get('ImageGallery')
#         detail = webcam.get('Detail', {})
#         lang_info = next(iter(detail.values()), {})
#         language = lang_info.get('Language', 'unknown')

#         if gps_info and image_gallery:
#             position = gps_info[0]
#             lat = position.get('Latitude')
#             lon = position.get('Longitude')
#             img_url = image_gallery[0].get('ImageUrl') if image_gallery else None
#             title = webcam.get('Shortname', 'Unnamed Webcam')

#             if lat and lon and img_url:
#                 coords.append({
#                     'title': title,
#                     'language': language,
#                     'lat': lat,
#                     'lon': lon,
#                     'image': img_url
#                 })

#     if coords:
#         df_coords = pd.DataFrame(coords)

#         # Filter functionality
#         languages = ['All'] + sorted(df_coords['language'].unique().tolist())
#         selected_language = st.selectbox("Filter by language", languages)

#         if selected_language != 'All':
#             display_df = df_coords[df_coords['language'] == selected_language]
#         else:
#             display_df = df_coords

#         # Pagination for gallery
#         items_per_page = 9  # 3 rows of 3 images for better visibility
#         total_pages = math.ceil(len(display_df) / items_per_page)

#         # Initialize session state for pagination
#         if 'gallery_page' not in st.session_state:
#             st.session_state.gallery_page = 1
            
#         start_idx = (st.session_state.gallery_page - 1) * items_per_page
#         end_idx = min(start_idx + items_per_page, len(display_df))
        
#         # Display as grid with 3 columns and fixed height for each cell
#         display_subset = display_df.iloc[start_idx:end_idx]
        
#         # Custom CSS to ensure equal card sizes
#         st.markdown("""
#         <style>
#         .webcam-card {
#             height: 400px;
#             border: 1px solid #2b2d3e;
#             border-radius: 10px;
#             padding: 10px;
#             margin-bottom: 20px;
#             background-color: #1e1e2f;
#         }
#         .image-container {
#             height: 250px;
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             overflow: hidden;
#         }
#         .image-container img {
#             width: 100%;
#             height: 100%;
#             object-fit: cover;
#         }
#         </style>
#         """, unsafe_allow_html=True)
        
#         # Create rows and columns for the grid
#         rows = math.ceil(len(display_subset) / 3)
        
#         for row in range(rows):
#             cols = st.columns(3)
            
#             for col in range(3):
#                 idx = row * 3 + col
#                 if idx < len(display_subset):
#                     webcam = display_subset.iloc[idx]
                    
#                     with cols[col]:
#                         # Create card with HTML for consistent sizing
#                         html = f"""
#                         <div class="webcam-card">
#                             <div class="image-container">
#                                 <img src="{webcam['image']}" alt="{webcam['title']}">
#                             </div>
#                             <h4>{webcam['title']}</h4>
#                             <p>Language: {webcam['language']}</p>
#                             <p>Coordinates: {webcam['lat']:.4f}, {webcam['lon']:.4f}</p>
#                         </div>
#                         """
#                         st.markdown(html, unsafe_allow_html=True)
                        
#                         # Add expandable details using Streamlit components
#                         with st.expander("Location Details"):
#                             st.write(f"**Language:** {webcam['language']}")
#                             st.write(f"**Latitude:** {webcam['lat']:.4f}")
#                             st.write(f"**Longitude:** {webcam['lon']:.4f}")
                            
#                             # Add a "View on Map" button
#                             if st.button(f"View on Map", key=f"map_btn_{idx}"):
#                                 st.session_state.center_lat = webcam['lat']
#                                 st.session_state.center_lon = webcam['lon']
#                                 st.session_state.nav_selection = "Map View"
#                                 st.rerun()
        
#         # Amazon-style pagination at the bottom
#         st.write("---")
#         st.write(f"Showing {start_idx+1}-{end_idx} of {len(display_df)} webcams")
        
#         # Pagination controls
#         pagination_cols = st.columns([1, 1, 3, 1, 1])
        
#         # Previous page button
#         if pagination_cols[0].button("← Previous", 
#                                      disabled=(st.session_state.gallery_page <= 1)):
#             st.session_state.gallery_page -= 1
#             st.rerun()
        
#         # Page number display
#         pagination_cols[2].write(f"Page {st.session_state.gallery_page} of {total_pages}")
        
#         # Next page button
#         if pagination_cols[4].button("Next →", 
#                                      disabled=(st.session_state.gallery_page >= total_pages)):
#             st.session_state.gallery_page += 1
#             st.rerun()

#     else:
#         st.warning('No webcams with coordinates and images found.')

# except requests.exceptions.RequestException as e:
#     st.error(f"Error fetching data: {e}")



import streamlit as st
import requests
import pandas as pd
import math

# This MUST be the first Streamlit command
# st.set_page_config(layout="wide", page_title="Image Gallery")

@st.cache_data(ttl=3600)
def fetch_webcam_data():
    url = "https://tourism.api.opendatahub.com/v1/WebcamInfo?pagesize=2000&removenullvalues=false&getasidarray=false"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

try:
    st.title("Image Gallery")
    
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

        # Filter functionality
        languages = ['All'] + sorted(df_coords['language'].unique().tolist())
        selected_language = st.selectbox("Filter by language", languages)

        if selected_language != 'All':
            display_df = df_coords[df_coords['language'] == selected_language]
        else:
            display_df = df_coords

        # Pagination for gallery
        items_per_page = 9  # 3 rows of 3 images for better visibility
        total_pages = math.ceil(len(display_df) / items_per_page)

        # Initialize session state for pagination
        if 'gallery_page' not in st.session_state:
            st.session_state.gallery_page = 1
            
        start_idx = (st.session_state.gallery_page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, len(display_df))
        
        # Display as grid with 3 columns and fixed height for each cell
        display_subset = display_df.iloc[start_idx:end_idx]
        
        # Custom CSS to ensure equal card sizes
        st.markdown("""
        <style>
        .webcam-card {
            height: 400px;
            border: 1px solid #2b2d3e;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 20px;
            background-color: #1e1e2f;
        }
        .image-container {
            height: 250px;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }
        .image-container img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create rows and columns for the grid
        rows = math.ceil(len(display_subset) / 3)
        
        for row in range(rows):
            cols = st.columns(3)
            
            for col in range(3):
                idx = row * 3 + col
                if idx < len(display_subset):
                    webcam = display_subset.iloc[idx]
                    
                    with cols[col]:
                        # Create card with HTML for consistent sizing
                        html = f"""
                        <div class="webcam-card">
                            <div class="image-container">
                                <img src="{webcam['image']}" alt="{webcam['title']}">
                            </div>
                            <h4>{webcam['title']}</h4>
                            <p>Language: {webcam['language']}</p>
                            <p>Coordinates: {webcam['lat']:.4f}, {webcam['lon']:.4f}</p>
                        </div>
                        """
                        st.markdown(html, unsafe_allow_html=True)
                        
                        # Add expandable details using Streamlit components
                        with st.expander("Location Details"):
                            st.write(f"**Language:** {webcam['language']}")
                            st.write(f"**Latitude:** {webcam['lat']:.4f}")
                            st.write(f"**Longitude:** {webcam['lon']:.4f}")
                            
                            # Add a "View on Map" button
                            if st.button(f"View on Map", key=f"map_btn_{idx}"):
                                st.session_state.center_lat = webcam['lat']
                                st.session_state.center_lon = webcam['lon']
                                st.session_state.nav_selection = "Map View"
                                st.rerun()
        
        # Amazon-style pagination at the bottom
        st.write("---")
        st.write(f"Showing {start_idx+1}-{end_idx} of {len(display_df)} webcams")
        
        # Pagination controls
        pagination_cols = st.columns([1, 1, 3, 1, 1])
        
        # Previous page button
        if pagination_cols[0].button("← Previous", 
                                     disabled=(st.session_state.gallery_page <= 1)):
            st.session_state.gallery_page -= 1
            st.rerun()
        
        # Page number display
        pagination_cols[2].write(f"Page {st.session_state.gallery_page} of {total_pages}")
        
        # Next page button
        if pagination_cols[4].button("Next →", 
                                     disabled=(st.session_state.gallery_page >= total_pages)):
            st.session_state.gallery_page += 1
            st.rerun()

    else:
        st.warning('No webcams with coordinates and images found.')

except requests.exceptions.RequestException as e:
    st.error(f"Error fetching data: {e}")