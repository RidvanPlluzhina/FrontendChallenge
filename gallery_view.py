import streamlit as st

def show_gallery_view(df_coords):
    """
    Display webcam images in a grid layout
    
    Args:
        df_coords: DataFrame containing webcam data with image URLs
    """
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
    
    st.write(f"Showing {start_idx+1}-{end_idx} of {len(display_df)} webcams")