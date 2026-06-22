import streamlit as st
from google import genai
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.request

# 1. INITIALIZE CLIENT
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

# 2. CONFIGURE NATIVE INTERFACE
st.set_page_config(page_title="Apex Real Estate Suite", layout="wide")
st.title("🏡 APEX // AI Real Estate Suite")
st.write("Generate high-converting property copy and premium marketing posters simultaneously.")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📋 Input Details")
    agency_name = st.text_input("AGENCY NAME:", placeholder="e.g., AYAN AN ALI AGENCY")
    property_title = st.text_input("PROPERTY TITLE:", placeholder="e.g., LUXURY PENTHOUSE")
    property_price = st.text_input("PRICE / SUBTITLE:", placeholder="e.g., $4,250,000")
    property_details = st.text_area("PROPERTY SPECIFICATIONS:", placeholder="e.g., 3-bedroom luxury flat...")
    uploaded_file = st.file_uploader("UPLOAD PROPERTY IMAGE:", type=["jpg", "jpeg", "png"])

# 3. MODERN EMBEDDED LAYOUT CARD ENGINE
def create_poster(image_file, agency, title, price):
    base_img = Image.open(image_file).convert("RGBA")
    poster_w, poster_h = 1200, 1500
    
    # Cross-version stable canvas resizing 
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
    
    # Modern Editorial Design: Clean Dark Contrast Lower Panel Block
    draw.rectangle([(0, poster_h - 480), (poster_w, poster_h)], fill=(11, 17, 30, 245))
    # Signature Deep Gold Accent Border Rule Line
    draw.rectangle([(0, poster_h - 486), (poster_w, poster_h - 480)], fill=(212, 175, 55, 255))
    
    final_img = Image.alpha_composite(base_img, overlay).convert("RGB")
    draw_final = ImageDraw.Draw(final_img)
    
    # Pull premium structural geometry font dynamically from Google Fonts open source repository
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
    
    # Geometric centered alignment layout
    draw_final.text((600, poster_h - 370), title.upper(), fill=(255, 255, 255), anchor="mm", font=title_font)
    if price:
        draw_final.text((600, poster_h - 280), price.upper(), fill=(212, 175, 55), anchor="mm", font=price_font)
    draw_final.text((600, poster_h - 175), "EXCLUSIVELY MARKETED BY:", fill=(148, 163, 184), anchor="mm", font=label_font)
    draw_final.text((600, poster_h - 110), agency.upper(), fill=(255, 255, 255), anchor="mm", font=agency_font)
    
    return final_img

# 4. EXECUTION HANDLERS (Flattened to eradicate indentation syntax errors)
with col2:
    st.subheader("✨ Generated Output")
    
    # Verify inputs safely before allowing compilation triggers
    fields_filled = property_details and agency_name and property_title
    button_pressed = st.button("Generate Professional Package", type="primary")

if button_pressed and not fields_filled:
    st.error("Error: Please provide values for Agency Name, Property Title, and Specifications first.")

if button_pressed and fields_filled:
    with st.spinner("Writing luxury listing copy..."):
        try:
            prompt_text = f"Write an ultra-luxury real estate listing description for: {property_details}. Focus on architectural elegance. Agency: {agency_name}. Conclude directly with 6 high-traffic real estate hashtags."
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt_text)
            st.write("📝 **Marketing Masterpiece:**")
            st.write(response.text)
        except Exception as e:
            st.error(f"AI text model failed: {str(e)}")
            
    if uploaded_file is not None:
        with st.spinner("Compiling high-res visual assets..."):
            try:
                poster = create_poster(uploaded_file, agency_name, property_title, property_price)
                st.image(poster, caption="Your New Marketing Poster", use_container_width=True)
                
                buf = io.BytesIO()
                poster.save(buf, format="JPEG", quality=95)
                
                st.download_button(
                    label="📥 Download High-Res Poster",
                    data=buf.getvalue(),
                    file_name="property_marketing_poster.jpg",
                    mime="image/jpeg"
                )
            except Exception as e:
                st.error(f"Visual composite error: {str(e)}")
    else:
        st.info("💡 Real estate poster rendering skipped. Drag and drop a property photo into the upload field to compile.")
