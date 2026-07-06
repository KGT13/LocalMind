import streamlit as st
import os
import base64

@st.cache_data
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def add_logo():
    """Renders the localmind logo at the top of the sidebar."""
    is_dark = st.session_state.get("dark_mode", False)
    logo_filename = "localmind_logo_dark.png" if is_dark else "localmind_logo.png"
    logo_path = os.path.join("assets", logo_filename) 
    
    if not os.path.exists(logo_path):
        # Fallback if the dark logo wasn't generated correctly or is missing
        logo_path = os.path.join("assets", "localmind_logo.png")
        
    if os.path.exists(logo_path):
        base64_img = get_base64_image(logo_path)
        # Create columns to center the logo and make it a proportional size
        col1, col2, col3 = st.columns([1.5, 7, 1.5])
        with col2:
            # Using raw HTML <img> prevents Streamlit from attaching the fullscreen button
            st.markdown(
                f'<img src="data:image/png;base64,{base64_img}" style="width:100%; border-radius: 8px;">',
                unsafe_allow_html=True
            )
        st.markdown("---") # Visual separator


# ── Theme helpers ────────────────────────────────────────────────────────


def load_theme():
    """Load the base stylesheet and, if dark mode is active, the dark overrides.

    Call this at the top of every page, right after ``st.set_page_config``.
    """
    import streamlit.components.v1 as components
    
    is_dark = str(st.session_state.get("dark_mode", False)).lower()
    
    # We use JS to inject the CSS into the parent document's head.
    # This ensures the CSS persists across page navigations, eliminating the white flash (FOUC).
    js = f"""
    <script>
        var parentDoc = window.parent.document;
        
        // Ensure base style is present
        if (!parentDoc.getElementById('localmind-base-style')) {{
            var link = parentDoc.createElement('link');
            link.id = 'localmind-base-style';
            link.rel = 'stylesheet';
            link.href = 'app/static/style.css';
            parentDoc.head.appendChild(link);
        }}
        
        // Handle dark mode style
        var darkStyle = parentDoc.getElementById('localmind-dark-style');
        var isDarkMode = {is_dark};
        
        if (isDarkMode && !darkStyle) {{
            var link = parentDoc.createElement('link');
            link.id = 'localmind-dark-style';
            link.rel = 'stylesheet';
            link.href = 'app/static/dark.css';
            parentDoc.head.appendChild(link);
        }} else if (!isDarkMode && darkStyle) {{
            darkStyle.remove();
        }}
    </script>
    """
    components.html(js, height=0, width=0)


def render_theme_toggle():
    """Render a dark-mode toggle at the top right of the page.

    Call this right after load_theme() on every page.
    """
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False

    col1, col2 = st.columns([10, 2])
    with col2:
        icon = ":material/dark_mode:" if not st.session_state.dark_mode else ":material/light_mode:"
        label = f"{icon} Dark Mode"
        toggled = st.toggle(label, value=st.session_state.dark_mode)

        if toggled != st.session_state.dark_mode:
            st.session_state.dark_mode = toggled
            st.rerun()
