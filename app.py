import streamlit as st
from google import genai
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.request

# ====================================================================
# 1. PREMIUM INTERFACE THEME CONFIGURATION (WITH INPUT HIGHLIGHTS)
# ====================================================================
st.set_page_config(
    page_title="Apex Global Realty Custom Suite",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Deep Target Mockup UI Style Injections with Input Field Highlighting
st.markdown(
    """
    <style>
        /* Force the main application area to a premium ivory off-white */
        .stApp, [data-testid="stAppViewContainer"] {
            background-color: #F5F2EB !important;
        }
        
        /* Force the sidebar to match the exact rich dark navy tone */
        [data-testid="stSidebar"], [data-testid="stSidebar"] > div {
            background-color: #070B13 !important;
        }
        
        /* Sidebar text color adjustments for elite visibility */
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
            color: #E2E8F0 !important;
        }

        /* --- INPUT BOX HIGHLIGHTING RULES --- */
        /* Style inputs in the main area for high visibility */
        div[data-testid="stAppViewContainer"] div[data-baseweb="input"], 
        div[data-testid="stAppViewContainer"] div[data-baseweb="textarea"] {
            border: 1px solid #B8962E !important;
            background-color: #FFFFFF !important;
            border-radius: 4px !important;
        }
        
        /* Style inputs inside the dark sidebar to stand out clearly */
        div[data-testid="stSidebar"] div[data-baseweb="input"], 
        div[data-testid="stSidebar"] div[data-baseweb="textarea"] {
            border: 1px solid #4A5568 !important;
            background-color: #1A202C !important;
            border-radius: 4px !important;
        }

        /* Golden glow highlight matrix when ANY input box is clicked/focused */
        div[data-baseweb="input"]:focus-within, div[data-baseweb="textarea"]:focus-within {
            border: 2px solid #D4AF37 !important;
            box-shadow: 0 0 8px rgba(212, 175, 55, 0.6) !important;
        }
        /* ------------------------------------ */
        
        /* Main UI tab configuration switches */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: transparent;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #0B111E;
            color: #CDD5E0;
            border-radius: 4px 4px 0px 0px;
            padding: 10px 20px;
            font-family: 'Georgia', serif;
        }
        .stTabs [aria-selected="true"] {
            background-color: #D4AF37 !important;
            color: #0B111E !important;
            font-weight: bold;
        }
        
        /* Luxury Call-To-Action Primary Buttons */
        div.stButton > button:first-child {
            background-color: #D4AF37;
            color: #0B111E;
            font-weight: bold;
            border: none;
            width: 100%;
            border-radius: 4px;
            font-family: 'Georgia', serif;
            letter-spacing: 1px;
            padding: 12px;
        }
        div.stButton > button:first-child:hover {
            background-color: #B8962E;
            color: #FFFFFF;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize Gemini Client Securely
api_key = st.secrets.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=api_key) if api_key else None

if "generated_copy" not in st.session_state:
    st.session_state["generated_copy"] = ""

# Corporate Luxury Header Element Block
st.markdown(
    """
    <div style="text-align: center; padding: 15px; margin-bottom: 25px; border-bottom: 1px solid #D4AF37;">
        <h1 style="color: #0B111E; font-family: 'Georgia', serif; font-size: 44px; letter-spacing: 3px; margin-bottom: 0px;">
            ⚜️ APEX GLOBAL REALTY
        </h1>
        <p style="color: #B8962E; font-family: 'Arial', sans-serif; font-size: 13px; letter-spacing: 5px; text-transform: uppercase; margin-top: 5px;">
            CUSTOM PROPERTY POSTER CREATOR
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ====================================================================
# 2. BRANDING CONTROL PANEL (SIDEBAR)
# ====================================================================
with st.sidebar:
    st.markdown("<h3 style='color: #D4AF37; font-family: Georgia;'>🏢 AGENCY CONFIG</h3>", unsafe_allow_html=True)
    agency_name = st.text_input("AGENCY NAME:", value="Apex Global Realty")
    
    st.markdown("---")
    st.markdown("<h3 style='color: #D4AF37; font-family: Georgia;'>📑 PROPERTY ASSETS</h3>", unsafe_allow_html=True)
    property_title = st.text_input("PROPERTY TITLE:", value="YOUR PROPERTY, BEAUTIFULLY PRESENTED")
    property_price = st.text_input("LISTING PRICE / SUBTITLE:", value="EXCLUSIVELY MARKETED BY:")
    
    property_details = st.text_area(
        "PROPERTY DETAILS:",
        value="Panoramic ocean views from this modern Architectural Masterpiece, with gorgeous green sanctuaries, modern interiors, and beautifully presented layout structures."
    )
    
    st.markdown("---")
    st.markdown("<h3 style='color: #D4AF37; font-family: Georgia;'>📸 ASSET MANAGER</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("SELECT IMAGES:", type=["jpg", "jpeg", "png"])
    
    st.markdown("---")
    mode = st.radio("COPY ENGINE WORKSPACE MODE:", ["Offline Workspace", "Live AI Generation"])

# ====================================================================
# 3. INTERACTIVE MAIN STUDIO SPLIT-LAYOUT
# ====================================================================
col1, col2 = st.columns([3, 2])

with col1:
    st.caption("✨ Production Asset Studio Frame")
    st.markdown("<h3 style='color: #0B111E; font-family: Georgia;'>Review and compile your high-resolution layout frameworks live.</h3>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🖼️ Interactive Media Poster", "📝 Formatted Copy Preview"])
    
    with tab1:
        if uploaded_file is not None:
            try:
                base_img = Image.open(uploaded_file).convert("RGBA")
                poster_w, poster_h = 1200, 1500
                
                # Aspect-ratio preservation cropping logic
                img_ratio = base_img.width / base_img.height
                poster_ratio = poster_w / poster_h
                if img_ratio > poster_ratio:
                    new_width = int(poster_h * img_ratio)
                    base_img = base_img.resize((new_width, poster_h), 3)
                    left = (base_img.width - poster_w) / 2
                    base_img = base_img.crop((left, 0, left + poster_w, poster_h))
                else:
                    new_height = int(poster_w / img_ratio)
                    base_img = base_img.resize((poster_w, new_height), 3)
                    top = (base_img.height - poster_h) / 2
                    base_img = base_img.crop((0, top, poster_w, top + poster_h))

                overlay = Image.new("RGBA", (poster_w, poster_h), (0, 0, 0, 0))
                draw = ImageDraw.Draw(overlay)
                
                # Dark Translucent Panel Card Placement (Bottom 480px)
                draw.rectangle([(0, poster_h - 480), (poster_w, poster_h)], fill=(11, 17, 30, 245))
                # Accent Luxury Gold Separator Strip
                draw.rectangle([(0, poster_h - 486), (poster_w, poster_h - 480)], fill=(212, 175, 55, 255))
                
                final_img = Image.alpha_composite(base_img, overlay).convert("RGB")
                draw_final = ImageDraw.Draw(final_img)
                
                try:
                    font_url = "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-Bold.ttf"
                    font_response = urllib.request.urlopen(font_url)
                    font_data = io.BytesIO(font_response.read())
                    title_font = ImageFont.truetype(font_data, 72)
                    price_font = ImageFont.truetype(font_data, 52)
                    label_font = ImageFont.truetype(font_data, 26)
                    agency_font = ImageFont.truetype(font_data, 44)
                except Exception:
                    title_font = ImageFont.load_default()
                    price_font = ImageFont.load_default()
                    label_font = ImageFont.load_default()
                    agency_font = ImageFont.load_default()
                
                # Render Center-Aligned Type Strings
                draw_final.text((600,
