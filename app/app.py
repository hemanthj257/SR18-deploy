import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from test import quick_detect
from PIL import Image
import numpy as np

# Set page config with custom width
st.set_page_config(page_title="Change Detection App", layout="wide")

# Add custom CSS to control image size
st.markdown("""
    <style>
        .stImage > img {
            max-width: 400px;
        }
    </style>
""", unsafe_allow_html=True)

def main():
    try:
        st.title("Change Detection System")

        tab1, tab2 = st.tabs(["Detect Changes", "History"])

        with tab1:
            st.write("Upload two images to detect changes between them")

            # Create three columns for better spacing
            col1, col2, col3 = st.columns(3)

            with col1:
                st.subheader("First Image (Current)")
                img1_file = st.file_uploader("Upload first image", type=['png', 'jpg', 'jpeg'], key="img1")
                if img1_file:
                    st.image(img1_file)

            with col2:
                st.subheader("Second Image (Previous)")
                img2_file = st.file_uploader("Upload second image", type=['png', 'jpg', 'jpeg'], key="img2")
                if img2_file:
                    st.image(img2_file)

            with col3:
                st.subheader("Result")
                if img1_file and img2_file:
                    if st.button("Detect Changes"):
                        with st.spinner("Processing..."):
                            # Save uploaded files
                            img1_path = os.path.join("app", "temp", "img1.jpg")
                            img2_path = os.path.join("app", "temp", "img2.jpg")
                            
                            Image.open(img1_file).save(img1_path)
                            Image.open(img2_file).save(img2_path)
                            
                            # Perform detection
                            result_path = quick_detect(img1_path, img2_path)
                            
                            if result_path and os.path.exists(result_path):
                                st.image(result_path)
                                # Save session without user ID
                                save_detection_session(None, img1_path, img2_path, result_path)
                            else:
                                st.error("Error processing images")

        with tab2:
            st.subheader("Previous Detections")
            # Get all sessions without user filtering
            sessions = get_user_sessions(None)
            if sessions:
                for session in sessions:
                    cols = st.columns(3)
                    with cols[0]:
                        st.image(session['img1_path'], caption="First Image")
                    with cols[1]:
                        st.image(session['img2_path'], caption="Second Image")
                    with cols[2]:
                        st.image(session['result_path'], caption="Result")
                    st.markdown("---")
            else:
                st.info("No previous detections found")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
