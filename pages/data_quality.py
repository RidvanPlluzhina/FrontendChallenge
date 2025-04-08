import streamlit as st
import requests
import pandas as pd


@st.cache_data(ttl=3600)
def fetch_webcam_data():
    url = "https://tourism.api.opendatahub.com/v1/WebcamInfo?pagesize=2000&removenullvalues=false&getasidarray=false"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def process_webcam_data(data):
    webcams = data['Items']
    
    total_webcams = len(webcams)
    webcams_with_gallery = 0
    webcams_without_gallery = 0
    valid_urls = 0
    invalid_urls = 0

    for webcam in webcams:
        image_gallery = webcam.get("ImageGallery", [])
        webcam_url = webcam.get("Webcamurl", "")

        if image_gallery:
            webcams_with_gallery += 1
        else:
            webcams_without_gallery += 1

        if webcam_url:
            valid_urls += 1
        else:
            invalid_urls += 1

    return {
        "Total Webcams": total_webcams,
        "With Gallery": webcams_with_gallery,
        "Without Gallery": webcams_without_gallery,
        "Valid URLs": valid_urls,
        "Invalid URLs": invalid_urls,
    }


def main():
    st.title("📊 Webcam Data Sanity Check")

    data = fetch_webcam_data()
    summary = process_webcam_data(data)

    df = pd.DataFrame.from_dict(summary, orient='index', columns=["Count"])

    st.subheader("Summary Chart")
    st.bar_chart(df)

    # Optional: also show the data as a table
    with st.expander("Show Data Table"):
        st.dataframe(df)

if __name__ == "__main__":
    main()
