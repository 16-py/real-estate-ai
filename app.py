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
# 2. BRANDING CONTROL PANEL (SIDEBAR)
# ====================================================================
with st.sidebar:
    st.markdown("<h2 style='color: #D4AF37; font-family: Georgia; font-size: 22px; margin-bottom: 0px;'>🏢 AGENCY CONFIG</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 12px; margin-top: 0px;'>Set up corporate branding metadata</p>", unsafe_allow_html=True)
    agency_name = st.text_input("AGENCY NAME:", value="Apex Global Realty")
    
    st.markdown("<br
