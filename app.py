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
# 3. INTERACTIVE MAIN STUDIO SPLIT-LAYOUT (SYNTAX FIXED)
# ====================================================================
col1, col2 = st.columns([3, 2])

with col1:
    # Native Clean Containers Avoid String Literal Mismatches Completely
    st.caption("✨ Production Asset Studio Frame")
    st.markdown("### Review and compile your high-resolution layout frameworks live.")
    
    tab1, tab2 = st.tabs(["🖼️ Interactive Media Poster", "📝 Formatted Copy Preview"])
    
    with tab1:
        if uploaded_file is not None:
            try:
                # Load picture and set up standard master aspect scale dimensions
                base_img = Image.open(uploaded_file).convert("RGBA")
                poster_w, poster_h = 1200, 1500
                
                # Dynamic Center-Crop Matrix Logic
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

                # Render Translucent Vector Card Overlay
                overlay = Image.new("RGBA", (poster_w, poster_h), (0, 0, 0, 0))
                draw = ImageDraw.Draw(overlay)
                
                # Solid Navy Frame Accent Block (Bottom 480px)
                draw.rectangle([(0, poster_h - 480), (poster_w, poster_h)], fill=(11, 17, 30, 245))
                # Solid Metallic Gold Horizon Line Separator Strip
                draw.rectangle([(0, poster_h - 486), (poster_w, poster_h - 480)], fill=(212, 175, 55, 255))
                
                final_img = Image.alpha_composite(base_img, overlay).convert("RGB")
                draw_final = ImageDraw.Draw(final_img)
                
                # Fetch High-Res Montserrat Typography Stream directly from Google Fonts
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
                draw_final.text((600, poster_h - 370), property_title.upper(), fill=(255, 255, 255), anchor="mm", font=title_font)
                if property_price:
                    draw_final.text((600, poster_h - 280), property_price.upper(), fill=(212, 175, 55), anchor="mm", font=price_font)
                
                # Slicing listing detail snippet for safe typographic string fitment
                snippet = property_details[:130] + "..." if len(property_details) > 130 else property_details
                draw_final.text((600, poster_h - 185), snippet, fill=(148, 163, 184), anchor="mm", font=label_font)
                draw_final.text((600, poster_h - 110), agency_name.upper(), fill=(255, 255, 255), anchor="mm", font=agency_font)
                
                # Streamlit UI Canvas Core Rendering Image Display Output
                st.image(final_img, caption="Live Layout Core Preview Matrix", use_container_width=True)
                
                # Memory Stream Image Compiler For Raw Export downloads
                buf = io.BytesIO()
                final_img.save(buf, format="JPEG", quality=98)
                
                st.download_button(
                    label="⚜️ DOWNLOAD MASTER HIGH-RES JPG ASSET",
                    data=buf.getvalue(),
                    file_name="apex_luxury_poster.jpg",
                    mime="image/jpeg",
                    use_container_width=True
                )
            except Exception as render_err:
                st.error(f"Render System Notice: {str(render_err)}")
        else:
            st.info("💡 Asset Manager Standby. Drop a high-resolution photo in the sidebar to see it render.")

    with tab2:
        st.markdown("#### 📄 Description Workspace Copy Block")
        if st.button("RUN TEXT ENGINE GENERATION", type="primary"):
            if mode == "Live AI Generation" and client:
                with st.spinner("Compiling copy framework..."):
                    try:
                        prompt_text = f"Write an ultra-luxury real estate listing description for: {property_details}. Agency: {agency_name}."
                        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt_text)
                        st.session_state["generated_copy"] = response.text
                    except Exception as e:
                        st.error(f"AI text model failed: {str(e)}")
            else:
                st.session_state["generated_copy"] = property_details
                
        st.text_area("Active Workspace Output Area:", value=st.session_state["generated_copy"], height=280)

with col2:
    # Right Column Sidebar Card Info
    with st.container(border=True):
        st.markdown("### ⚜️ GENERATE CUSTOM POSTER")
        st.write("The integrated layout processor captures raw uploaded image files and conforms them into premium 4:5 vertical marketing arrays for distribution across listing networks.")
        st.markdown("---")
        st.markdown("**ACTIVE DESIGN PROFILE:**")
        st.info("PREMIUM NAVY / GOLD CORPORATE")
