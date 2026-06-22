import streamlit as st
from google import genai
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.request

# ====================================================================
# RESTORED PREMIUM INTERFACE
# ====================================================================
st.set_page_config(page_title="Apex Global Realty Custom Suite", layout="wide")

st.markdown(
    """
    <style>
        /* Main Layout Backgrounds */
        .stApp, [data-testid="stAppViewContainer"] { background-color: #F5F2EB !important; }
        [data-testid="stSidebar"], [data-testid="stSidebar"] > div { background-color: #070B13 !important; }
        
        /* Ensure all text is readable */
        .stApp p, .stApp span, .stApp label, .stApp div { color: #0B111E !important; }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label { color: #E2E8F0 !important; }
        
        /* Input Field Highlights */
        div[data-baseweb="input"]:focus-within, div[data-baseweb="textarea"]:focus-within {
            border: 2px solid #D4AF37 !important;
            box-shadow: 0 0 8px rgba(212, 175, 55, 0.6) !important;
        }
        
        .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: #0B111E !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize Gemini Client
api_key = st.secrets.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=api_key) if api_key else None
if "generated_copy" not in st.session_state: st.session_state["generated_copy"] = ""

# ====================================================================
# SIDEBAR
# ====================================================================
with st.sidebar:
    st.markdown("<h3 style='color: #D4AF37;'>🏢 AGENCY CONFIG</h3>", unsafe_allow_html=True)
    agency_name = st.text_input("AGENCY NAME:", value="Apex Global Realty")
    property_title = st.text_input("PROPERTY TITLE:", value="YOUR PROPERTY")
    property_details = st.text_area("DETAILS:", value="Stunning views.")
    uploaded_file = st.file_uploader("SELECT IMAGES:", type=["jpg", "png"])
    mode = st.radio("COPY ENGINE:", ["Manual", "Live AI Generation"])

# ====================================================================
# MAIN STUDIO
# ====================================================================
col1, col2 = st.columns([3, 2])

with col1:
    tab1, tab2 = st.tabs(["🖼️ Interactive Media Poster", "📝 Formatted Copy Preview"])
    
    with tab1:
        if uploaded_file is not None:
            base_img = Image.open(uploaded_file).convert("RGBA")
            overlay = Image.new("RGBA", (1200, 1500), (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            draw.rectangle([(0, 1020), (1200, 1500)], fill=(11, 17, 30, 245)) 
            draw.rectangle([(0, 1014), (1200, 1020)], fill=(212, 175, 55, 255))
            
            final_img = Image.alpha_composite(base_img.resize((1200, 1500)), overlay).convert("RGB")
            st.image(final_img, use_container_width=True)
            
            buf = io.BytesIO()
            final_img.save(buf, format="JPEG")
            st.download_button("⚜️ DOWNLOAD MASTER JPG", data=buf.getvalue(), file_name="apex_poster.jpg")
        else:
            st.info("💡 Asset Manager Standby. Upload an image to render.")

    with tab2:
        if st.button("RUN TEXT ENGINE GENERATION"):
            st.session_state["generated_copy"] = f"Luxury property description for: {property_title}."
        st.text_area("Workspace Output:", value=st.session_state["generated_copy"], height=280)

with col2:
    st.markdown(
        """
        <div style="border: 1px solid #D4AF37; padding: 20px; background-color: #F5F2EB;">
            <h3 style="color: #0B111E !important;">⚜️ GENERATE CUSTOM POSTER</h3>
            <p style="color: #0B111E !important;">The integrated layout processor captures raw uploaded image files.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
