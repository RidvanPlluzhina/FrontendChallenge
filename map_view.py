import streamlit as st
import pydeck as pdk

def show_map_view(df_coords):
    """
    Display webcam locations on an interactive map with image tooltips
    
    Args:
        df_coords: DataFrame containing webcam data with lat/lon coordinates and image URLs
    """
    # Define Pydeck Layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_coords,
        pickable=True,
        opacity=0.8,
        filled=True,
        radius_scale=50,
        radius_min_pixels=5,
        radius_max_pixels=100,
        line_width_min_pixels=1,
        get_position='[lon, lat]',
        get_fill_color='[200, 30, 0, 160]'
    )

    # Set initial view state
    view_state = pdk.ViewState(
        latitude=df_coords['lat'].mean(),
        longitude=df_coords['lon'].mean(),
        zoom=8,
        pitch=0
    )

    # Custom tooltip with images
    tooltip = {
        "html": "<b>{title}</b><br><img src='{image}' width='200'>",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }

    # Render deck.gl map
    r = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip
    )

    # Add instructions for users
    st.info("👆 Hover over a point on the map to view the webcam image")

    st.subheader('Webcam Map')
    st.pydeck_chart(r)
    
    # Add map controls and statistics
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Total Webcams:** {len(df_coords)}")
    with col2:
        st.write(f"**Average Coordinates:** ({df_coords['lat'].mean():.4f}, {df_coords['lon'].mean():.4f})")
        
    # # Add instructions for users
    # st.info("👆 Hover over a point on the map to view the webcam image")