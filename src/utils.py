import streamlit as st
import os
import base64

@st.cache_data
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def add_logo():
    """Renders the localmind logo at the top of the sidebar."""
    # Points to your logo inside the assets folder
    logo_path = os.path.join("assets", "localmind_logo.png") 
    
    if os.path.exists(logo_path):
        base64_img = get_base64_image(logo_path)
        st.sidebar.markdown(
            f'<div style="text-align: center; margin: -50px -20px -40px -20px;"><img src="data:image/png;base64,{base64_img}" style="width:70%;"></div>',
            unsafe_allow_html=True
        )
        st.sidebar.markdown("---") # Visual separator
