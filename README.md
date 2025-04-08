# 📸 Webcam Viewer 

A lightweight and interactive Streamlit app to explore real-time webcams from South Tyrol, using open tourism data provided by the Open Data Hub. Visualize webcams on a map, browse them in a table, and preview live images—all in one interface.

## 🔧 Features

- 📋 Browse webcam data in a clean, responsive table  
- 🌐 View webcam locations on an interactive map  
- 📸 Preview live images for each webcam  
- 🔍 Filter and select webcams via dropdown menu  
- 🧭 Real-time coordinates and language metadata

## 🧰 Tools

This project was built using the following tools and libraries:

- **[Streamlit](https://streamlit.io/)** – Used to build the interactive web app. It's one of the best frameworks for fast prototyping and creating data-driven interfaces with minimal effort.
- **[Pandas](https://pandas.pydata.org/)** – For data manipulation and table generation  
- **[Requests](https://docs.python-requests.org/)** – To fetch webcam data from the Open Data Hub API  
- **[Pydeck](https://deckgl.readthedocs.io/en/latest/)** – For rendering the interactive map with webcam markers  
- **[Open Data Hub API – Tourism](https://opendatahub.bz.it/)** – The source of real-time webcam data from South Tyrol 

## 🚀 Getting Started

### 1. Clone the Repository

git clone https://github.com/RidvanPlluzhina/WebcamVisualizer.git
cd WebcamVisualizer

### 2. Install Dependencies

pip install -r requirements.txt

### 3. Run the App

streamlit run main.py

## 📦 Requirements
- streamlit
- pandas
- requests
- (Already included in requirements.txt)

## 👥 Contributors
- Sam,
- Michele,
- Enri,
- Ridvan
