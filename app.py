import streamlit as st
from google import genai
from PIL import Image, ImageDraw
import io

# 1. INITIALIZE GEMINI CLIENT SECURELY
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

# 2. INTERFACE VISUAL DESIGN (Clean & Wide Layout)
st.set_page_config(page_title="Apex Real Estate Suite", layout="wide")

st.title("🏡 APEX // AI Real Estate Suite")
st.write("Generate high-converting property copy and premium marketing posters simultaneously.")

# Setup a clean two-column dashboard split
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📋 Input Details")
    agency_name = st.text_input("AGENCY NAME:", placeholder="e.g., AYAN AN ALI AGENCY")
    property_title = st.text_input("PROPERTY TITLE:", placeholder="e.g., LUXURY PENTHOUSE")
    
    property_details = st.text_area(
        "PROPERTY SPECIFICATIONS:", 
        placeholder="e.g., 3-bedroom penthouse in London, private balcony, marble countertops..."
    )
    
    uploaded_file = st.file_uploader("UPLOAD PROPERTY IMAGE:", type=["jpg", "jpeg", "png"])

# 3. HIGH-END POSTER CREATION ENGINE
def create_poster(image_file, agency, title):
    # Open base image
    base_img = Image.open(image_file).convert("RGBA")
    
    # Instagram Portrait Dimensions (1080x1350) for crisp high-res layout
    poster_w, poster_h = 1080, 1350
    
    # Professional Aspect Ratio Center-Cropping
    img_ratio = base_img.width / base_img.height
    poster_ratio = poster_w / poster_h
    if img_ratio > poster_ratio:
        new_width = int(poster_h * img_ratio)
        base_img = base_img.resize((new_width, poster_h), Image.Resampling.LANCZOS)
        left = (base_img.width - poster_w) / 2
        base_img = base_img.crop((left, 0, left + poster_w, poster_h))
    else:
        new_height = int(poster_w / img_ratio)
        base_img = base_img.resize((poster_w, new_height), Image.Resampling.LANCZOS)
        top = (base_img.height - poster_h) / 2
        base_img = base_img.crop((0, top, poster_w, top + poster_h))

    # Create graphic graphics layer for transparent blending
    overlay = Image.new("RGBA", (poster_w, poster_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Premium Design Layout: Dark matte footer card across the bottom
    draw.rectangle([(0, poster_h - 420), (poster_w, poster_h)], fill=(15, 23, 42, 235))
    
    # Pure Gold Divider Line accent
    draw.rectangle([(0, poster_h - 425), (poster_w, poster_h - 420)], fill=(212, 175, 55, 255))
    
    # Merge base image with the graphic layout cards
    final_img = Image.alpha_composite(base_img, overlay).convert("RGB")
    draw_final = ImageDraw.Draw(final_img)
    
    # Modern Text Layout Blocks using system default typography safely
    # Centered Title (Bold, All-Caps)
    draw_final.text((540, poster_h - 300), title.upper(), fill=(255, 255, 255), anchor="mm")
    
    # Sub-Branding Line
    draw_final.text((540, poster_h - 180), "EXCLUSIVELY MARKETED BY:", fill=(212, 175, 55), anchor="mm")
    
    # Agency Name Presentation
    draw_final.text((540, poster_h - 110), agency.upper(), fill=(255, 255, 255), anchor="mm")
    
    return final_img

# 4. CAPTION & VISUAL GENERATION PROTOCOLS
with col2:
    st.subheader("✨ Generated Output")
    
    if st.button("Generate Professional Package", type="primary"):
        if not property_details or not agency_name or not property_title:
            st.error("Error: Please fill in all text input fields first.")
        else:
            with st.spinner("Writing premium listing copy..."):
                try:
                    prompt_text = (
                        f"Write a luxury property listing caption for: {property_details}. "
                        f"Include agency details: {agency_name}. "
                        f"At the very end of the text, include 5-8 trending real estate hashtags."
                    )
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt_text
                    )
                    st.write("**
