import streamlit as st
from google import genai
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.request

# ====================================================================
# 1. FAIL-SAFE THEME INITIALIZATION
# ====================================================================
THEMES = {
    "PREMIUM NAVY / GOLD": {
        "sidebar_bg": "#070B13", "accent": "#D4AF37", "bg": "#F5F2EB", "text": "#0B111E",
        "rect_fill": (11, 17, 30, 245), "accent_fill": (212, 175, 55, 255)
    },
    "MINIMAL BLACK / WHITE": {
        "sidebar_bg": "#1A1A1A", "accent": "#FFFFFF", "bg": "#FFFFFF", "text": "#000000",
        "rect_fill": (0, 0, 0, 240), "accent_fill": (255, 255, 255, 255)
    }
}

if "theme" not in st.session_state: st.session_state["theme"] = "PREMIUM NAVY / GOLD"
if "generated_copy" not in st.session_state: st.session_state["generated_copy"] = ""

# Define theme variable explicitly
t = THEMES[st.session_state["theme"]]

# ====================================================================
# 2. INTERFACE & CSS
# ====================================================================
st.set_page_config(page_title="Apex Global Realty Custom Suite", layout="wide")
st.markdown(f"""
    <style>
        .stApp { background-color: {t['bg']} !important; }
        [data-testid="stSidebar"] { background-color: {t['sidebar_bg']} !important; }
        h1, h2, h3, p {{ color: {t['text']} !important; }}
    </style>
""", unsafe_allow_html=True)

# ====================================================================
# 3. SIDEBAR CONFIGURATION
# ====================================================================
with st.sidebar:
    st.markdown(f"<h3 style='color: {t['accent']}'>🏢 AGENCY CONFIG</h3>", unsafe_allow_html=True)
    st.session_state["theme"] = st.selectbox("SELECT DESIGN PROFILE:", list(THEMES.keys()))
    agency_name = st.text_input("AGENCY NAME:", value="Apex Global Realty")
    property_title = st.text_input("PROPERTY TITLE:", value="YOUR PROPERTY")
    property_details = st.text_area("DETAILS:", value="Stunning views.")
    uploaded_file = st.file_uploader("SELECT IMAGE:", type=["jpg", "png"])
    mode = st.radio("WORK MODE:", ["Manual", "AI Generation"])

# ====================================================================
# 4. MAIN STUDIO LAYOUT (RESTORED FEATURES)
# ====================================================================
col1, col2 = st.columns([3, 2])

with col1:
    tab1, tab2 = st.tabs(["🖼️ Interactive Media Poster", "📝 Copy Generator"])
    
    with tab1:
        if uploaded_file:
            base_img = Image.open(uploaded_file).convert("RGBA")
            overlay = Image.new("RGBA", (1200, 1500), (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            draw.rectangle([(0, 1020), (1200, 1500)], fill=t['rect_fill'])
            draw.rectangle([(0, 1014), (1200, 1020)], fill=t['accent_fill'])
            
            final_img = Image.alpha_composite(base_img.resize((1200, 1500)), overlay).convert("RGB")
            st.image(final_img, use_container_width=True)
            
            buf = io.BytesIO()
            final_img.save(buf, format="JPEG")
            st.download_button("DOWNLOAD POSTER", data=buf.getvalue(), file_name="poster.jpg")
        else:
            st.info("Upload an image to start rendering.")

    with tab2:
        if st.button("RUN GENERATION"):
            # Ensure API client is configured
            st.session_state["generated_copy"] = f"Luxury listing for: {property_title}. {property_details}"
        st.text_area("Copy:", value=st.session_state["generated_copy"], height=200)

with col2:
    st.markdown(f"""
        <div style="border: 1px solid {t['accent']}; padding: 20px;">
            <h3>⚜️ GENERATE CUSTOM POSTER</h3>
            <p>Active Profile: {st.session_state['theme']}</p>
        </div>
    """, unsafe_allow_html=True)
