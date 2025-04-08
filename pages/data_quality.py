import streamlit as st
import requests
import pandas as pd


@st.cache_data(ttl=3600)
def fetch_webcam_data():
    url = "https://tourism.api.opendatahub.com/v1/WebcamInfo?pagesize=2000&removenullvalues=false&getasidarray=false"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Process the webcam data to generate the sanity check table
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

        # Count webcams with and without an image gallery
        if image_gallery:
            webcams_with_gallery += 1
        else:
            webcams_without_gallery += 1

        # Check if the webcam URL is valid
        if webcam_url:
            valid_urls += 1
        else:
            invalid_urls += 1

    # Prepare the sanity check data
    sanity_check_data = {
        "Total Webcams": total_webcams,
        "Webcams with Image Gallery": webcams_with_gallery,
        "Webcams without Image Gallery": webcams_without_gallery,
        "Valid Webcam URLs": valid_urls,
        "Urls not present": invalid_urls,
    }

    return sanity_check_data

# Streamlit page setup
def main():
    st.title("Webcam Data Sanity Check")

    # Fetch data from the API
    data = fetch_webcam_data()

    # Process the data to generate sanity check table
    sanity_check_data = process_webcam_data(data)

    # Display the sanity check data in a table with conditional formatting
    st.subheader("Sanity Check Summary")
    df = pd.DataFrame(list(sanity_check_data.items()), columns=["Metric", "Count"])

    # Function to apply colors
    def colorize(val):
        if val == "Webcams with Image Gallery" or val == "Valid Webcam URLs":
            return 'color: green'
        elif val == "Webcams without Image Gallery" or val == "Urls not present":
            return 'color: red'
        return ''

    # Apply conditional formatting
    styled_df = df.style.applymap(colorize, subset=["Metric"])

    st.table(styled_df)

if __name__ == "__main__":
    main()
