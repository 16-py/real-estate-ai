import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.request

# 1. PAGE SETUP (Clean, Wide Luxury Dashboard Layout)
st.set_page_config(
    page_title="Apex Real Estate Suite", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. SIDEBAR BRANDING & CONFIGURATION CONTROLS
with st.sidebar:
    st.markdown("### 🏢 BRANDING CONFIG")
    agency_name = st.text_input("AGENCY NAME:", value="AYAN AN ALI AGENCY")
    
    st.markdown("---")
    st.markdown("### 📑 PROPERTY DETAILS")
    property_title = st.text_input("PROPERTY TITLE:", value="THE LUXURY PENTHOUSE")
    property_price = st.text_input("LISTING PRICE / SUBTITLE:", value="$4,250,000")
    property_details = st.text_area(
        "RAW PROPERTY SPECIFICATIONS:", 
        value="3 bedrooms, floor-to-ceiling panoramic glass windows, private infinity terrace, premium marble finishings."
    )
    
    st.markdown("---")
    st.markdown("### 📸 ASSET UPLOAD")
    uploaded_file = st.file_uploader("UPLOAD HIGH-RES PHOTO:", type=["jpg", "jpeg", "png"])

# 3. MAIN INTERFACE WORKSPACE DISPLAY
st.title("🏡 APEX // AI Elite Real Estate Suite")
st.write("Compile magazine-grade property descriptions and matching premium marketing posters simultaneously.")

# Setup clean visual container cards for your content outputs
with st.container(border=True):
    st.subheader("✨ Luxury Workspace Output Preview")
    
    # Create navigation tabs to neatly separate your text copy and visual media assets
    tab1, tab2 = st.tabs(["📝 Elite Listing Copy", "🖼️ Premium Poster Visual"])
    
    with tab1:
        st.markdown("### 📄 Formatted Copy Preview")
        
        # Hardcoded premium preview text so you can test interface aesthetics during the API refresh window
        st.info("ℹ️ Gemini API Free-Tier Quota Refreshes Daily. Displaying offline design preview below:")
        
        preview_copy = f"""
        **Introducing an Architectural Masterpiece presented by {agency_name.upper()}**
        
        Step into luxury with **{property_title.upper()}**, a world-class residence offered exclusively at **{property_price}**. This exceptional property features top-tier designs tailored for the discerning individual.
        
        **Premium Specifications:**
        {property_details}
        
        #LuxuryRealEstate #PenthouseLiving #PropertyMarketing #EliteListings #{agency_name.replace(' ', '')}
        """
        st.markdown(preview_copy)

    with tab2:
        st.markdown("### 🖨️ High-Res Asset Composite")
        
        # IMAGE COMPOSITING ENGINE
        if uploaded_file is not None:
            try:
                base_img = Image.open(uploaded_file).convert("RGBA")
                poster_w, poster_h = 1200, 1500
                
                # Dynamic Center-Cropping Calculations
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
                
                # Dark Translucent Backdrop & Deep Gold Rule Accent
                draw.rectangle([(0, poster_h - 480), (poster_w, poster_h)], fill=(11, 17, 30, 245))
                draw.rectangle([(0, poster_h - 486), (poster_w, poster_h - 480)], fill=(212, 175, 55, 255))
                
                final_img = Image.alpha_composite(base_img, overlay).convert("RGB")
                draw_final = ImageDraw.Draw(final_img)
                
                # Pull high-end typography directly from Google Fonts
                try:
                    font_url = "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-Bold.ttf"
                    font_response = urllib.request.urlopen(font_url)
                    font_data = io.BytesIO(font_response.read())
                    title_font = ImageFont.truetype(font_data, 76)
                    price_font = ImageFont.truetype(font_data, 56)
                    label_font = ImageFont.truetype(font_data, 28)
                    agency_font = ImageFont.truetype(font_data, 46)
                except Exception:
                    title_font = ImageFont.load_default()
                    price_font = ImageFont.load_default()
                    label_font = ImageFont.load_default()
                    agency_font = ImageFont.load_default()
                
                # Render perfectly aligned typographic layout lines
                draw_final.text((600, poster_h - 370), property_title.upper(), fill=(255, 255, 255), anchor="mm", font=title_font)
                if property_price:
                    draw_final.text((600, poster_h - 280), property_price.upper(), fill=(212, 175, 55), anchor="mm", font=price_font)
                draw_final.text((600, poster_h - 175), "EXCLUSIVELY MARKETED BY:", fill=(148, 163, 184), anchor="mm", font=label_font)
                draw_final.text((600, poster_h - 110), agency_name.upper(), fill=(255, 255, 255), anchor="mm", font=agency_font)
                
                # Display the high-res poster inside the clean tab layout panel
                st.image(final_img, caption="
