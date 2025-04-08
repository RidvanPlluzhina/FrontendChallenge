import streamlit as st

st.set_page_config(page_title="Webcam Inspector", layout="wide", page_icon=":material/camera_video:")

home_page = st.Page(
    "pages/home.py",
    title="Home",
    icon=":material/home:",
)

map_page = st.Page(
    "pages/map.py",
    title="Map",
    icon=":material/map:",
)

data_quality_page = st.Page(
    "pages/data_quality.py",
    title="Data Quality",
    icon=":material/analytics:",
)

image_gallery_page = st.Page(
    "pages/image_gallery.py",
    title="Image Gallery",
    icon=":material/image:",
)

pg = st.navigation(
    {
        "General" : [home_page,
                     map_page,
                     data_quality_page,
                     image_gallery_page],
    }
)

pg.run()
