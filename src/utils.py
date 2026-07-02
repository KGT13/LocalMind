import streamlit as st
import os

def add_logo():
    """Renders the localmind logo at the top of the sidebar."""
    # Points to your logo inside the assets folder
    logo_path = os.path.join("assets", "localmind_logo.png") 
    
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, use_column_width=True)
        st.sidebar.markdown("---") # Visual separator
