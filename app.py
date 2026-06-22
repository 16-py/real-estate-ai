import streamlit as st
from google import genai
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.request

# ====================================================================
# 1. LUXURY DASHBOARD THEMING & CONFIGURATION
# ====================================================================
st.set_page_config(
    page_title="Apex Global Realty Custom Suite",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Deep Luxury Navy & Gold UI Custom Style Injection
st.markdown(
    """
    <style>
        /* Base application background styling */
        .stApp {
            background-color: #FDFBF7;
        }
        
        /* Main UI tab adjustments */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
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
        
        /* Primary premium action buttons button styling */
        div.stButton > button:first-child {
            background-color: #D4AF37;
            color: #0B111E;
            font-weight: bold;
            border: none;
            width: 100%;
            border-radius: 4px;
            font-family: 'Georgia', serif;
            letter-spacing: 1px;
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
    <div style="text-align: center; padding: 15px; margin-bottom: 25px; border-bottom: 1px solid #E2E8F0;">
        <h1 style="color: #0B111E; font-family: 'Georgia', serif; font-size: 44px; letter-spacing: 3px; margin-bottom: 0px;">
            ⚜️ APEX GLOBAL REALTY
        </h1>
        <p style="color: #D4AF37; font-family: 'Arial', sans-serif; font-size: 13px; letter-spacing: 5px; text-transform: uppercase; margin-top: 5px;">
            CUSTOM PROPERTY POSTER CREATOR
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ====================================================================
# 2. BRANDING CONTROL PANEL (SIDEBAR) - FIXED SYNTAX IMMUNE FORMAT
# ====================================================================
with st.sidebar:
    st.markdown("### 🏢 AGENCY CONFIG")
    agency_name = st.text_input("AGENCY NAME:", value="Apex Global Realty")
    
    st.markdown("---")
    st.markdown("### 📑 PROPERTY ASSETS")
    property_title = st.text_input("PROPERTY TITLE:", value="YOUR PROPERTY, BEAUTIFULLY PRESENTED")
    property_price = st.text_input("LISTING PRICE / SUBTITLE:", value="EXCLUSIVELY MARKETED BY:")
    
    property_details = st.text_area(
        "PROPERTY DETAILS:",
        value="Panoramic ocean views from this modern Architectural Masterpiece, with gorgeous green sanctuaries, modern interiors, and beautifully presented layout structures."
    )
    
    st.markdown("---")
    st.markdown("### 📸 ASSET MANAGER")
    uploaded_file = st.file_uploader("SELECT IMAGES:", type=["jpg", "jpeg", "png"])
    
    st.markdown("---")
    mode = st.radio("COPY ENGINE WORKSPACE MODE:", ["Offline Workspace", "Live AI Generation"])

# ====================================================================
# 3. INTERACTIVE MAIN STUDIO SPLIT-LAYOUT
# ====================================================================
col1, col2 = st.columns([3, 2])

with col1:
    # Stylized Canvas Context Tag
    st.markdown(
        """
        <div style="border-left: 4px solid #D4AF37; padding-left: 15px; margin-
