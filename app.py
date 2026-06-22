import streamlit as st
from google import genai
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.request

# 1. CLIENT SETTINGS
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

# 2. UI SETUP
st.set_page_config(page_title="Apex Real Estate Suite", layout="wide")
st.title("🏡 APEX // AI Real Estate Suite")
st.write("Generate high-converting property copy and premium marketing posters simultaneously.")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📋 Input Details")
    agency_name = st.text_input("AGENCY NAME:", placeholder="e.g., AYAN AN ALI AGENCY")
    property_title = st.text_input("PROPERTY TITLE:", placeholder="e.g., LUXURY PENTHOUSE")
    property_price = st.text_input("PRICE / SUBTITLE:", placeholder="e.g., $4,250,000")
    property_details = st.text_area("PROPERTY SPECIFICATIONS:", placeholder="e.g., 3 bedrooms, balcony...")
    uploaded_file = st.file_uploader("UPLOAD PROPERTY IMAGE:", type=["jpg", "jpeg", "png"])

# 3. POSTER GENERATION ENGINE
def create_poster(image_file, agency, title, price):
    base_img = Image.open(image_file).convert("RGBA")
    poster_w, poster_h = 1200, 1500
    
    # Crop and Resize Layout using safe default scaling integers to prevent crashes
    img_ratio = base_img.width / base_img.height
    poster_ratio = poster_w / poster_h
    if img_ratio > poster_ratio:
        new_width = int(poster_h * img_ratio)
        base_img = base_img.resize((new_width, poster_h), 3) # Safe integer for high-quality scaling
        left = (base_img.width - poster_w) / 2
        base_img = base_img.crop((left, 0, left + poster_w, poster_h))
    else:
        new_height = int(poster_w / img_ratio)
        base_img = base_img.resize((poster_w, new_height), 3) # Safe integer for high-quality scaling
        top = (base_img.height - poster_h) / 2
        base_img = base_img.crop((0, top, poster_w, top + poster_h))

    overlay = Image.new("RGBA", (poster_w, poster_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Translucent Dark Bottom Card Banner
    draw.rectangle([(0, poster_h - 480), (poster_w, poster_h)], fill=(11, 17, 30, 240))
    # Elegant Gold Line Accent Separator
    draw.rectangle([(0, poster_h - 486), (poster_w, poster_h - 480)], fill=(212, 175, 55, 255))
    
    final_img = Image.alpha_composite(base_img, overlay).convert("RGB")
    draw_final = ImageDraw.Draw(final_img)
    
    # Download clean modern geometry fonts dynamically
    try:
        font_url = "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-Bold.ttf"
        font_response = urllib.request.urlopen(font_url)
        font_data = io.BytesIO(font_response.read())
        title_font = ImageFont.truetype(font_data, 72)
        price_font = ImageFont.truetype(font_data, 54)
        label_font = ImageFont.truetype(font_data, 30)
        agency_font = ImageFont.truetype(font_data, 44)
    except Exception:
        title_font = ImageFont.load_default()
        price_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        agency_font = ImageFont.load_default()
    
    # Draw Premium Typography
    draw_final.text((600, poster_h - 360), title.upper(), fill=(255, 255, 255), anchor="mm", font=title_font)
    if price:
        draw_final.text((600, poster_h - 270), price.upper(), fill=(212, 175, 55), anchor="mm", font=price_font)
    draw_final.text((600, poster_h - 170), "EXCLUSIVELY MARKETED BY:", fill=(200, 200, 200), anchor="mm", font=label_font)
    draw_final.text((600, poster_h - 100), agency.upper(), fill=(255, 255, 255), anchor="mm", font=agency_font)
    
    return final_img

# 4. RUN PROCESSING PROTOCOLS
with col2:
    st.subheader("✨ Generated Output")
    
    if st.button("Generate Professional Package", type="primary"):
        if not property_details or not agency_name or not property_title:
            st.error("Error: Please fill out all text input blocks in the left column first.")
        else:
            with st.spinner("Writing luxury listing copy..."):
                try:
                    prompt_text = "Write a luxury real estate listing description for: " + str(property_details) + ". Include the branding details for agency: " + str(agency_name) + ". Append 6 high-traffic real estate hashtags directly at the bottom."
                    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt_text)
                    st.write("📝 **Marketing Masterpiece:**")
                    st.write(response.text)
                except Exception as e:
                    st.error("AI Generation Error: " + str(e))
            
            if uploaded_file is not None:
