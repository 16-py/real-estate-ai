import streamlit as st
from google import genai
from PIL import Image, ImageDraw
import io

# 1. INITIALIZE GEMINI CLIENT SECURELY
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

# 2. INTERFACE VISUAL DESIGN (Clean Layout - No Markdown Hacks)
st.set_page_config(page_title="Apex Real Estate Suite", layout="wide")

st.title("🏡 APEX // AI Real Estate & Poster Suite")
st.write("Generate elite property descriptions and custom marketing posters simultaneously.")

# Setup an elegant two-column dashboard split
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📋 Input Details")
    agency_name = st.text_input("AGENCY NAME:", placeholder="e.g., APEX GLOBAL REALTY")
    property_title = st.text_input("PROPERTY SHORT TITLE:", placeholder="e.g., LUXURY PENTHOUSE")
    
    property_details = st.text_area(
        "PROPERTY SPECIFICATIONS:", 
        placeholder="e.g., 3-bedroom penthouse in London, private balcony, marble countertops..."
    )
    
    uploaded_file = st.file_uploader("UPLOAD PROPERTY IMAGE:", type=["jpg", "jpeg", "png"])

# 3. POSTER CREATION ENGINE (Using Pillow)
def create_poster(image_file, agency, title):
    img = Image.open(image_file).convert("RGBA")
    poster_w, poster_h = 1080, 1350
    
    # Auto-crop logic
    img_ratio = img.width / img.height
    poster_ratio = poster_w / poster_h
    if img_ratio > poster_ratio:
        new_width = int(poster_h * img_ratio)
        img = img.resize((new_width, poster_h), Image.Resampling.LANCEZOS)
        left = (img.width - poster_w) / 2
        img = img.crop((left, 0, left + poster_w, poster_h))
    else:
        new_height = int(poster_w / img_ratio)
        img = img.resize((poster_w, new_height), Image.Resampling.LANCEZOS)
        top = (img.height - poster_h) / 2
        img = img.crop((0, top, poster_w, top + poster_h))

    overlay = Image.new("RGBA", (poster_w, poster_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Bottom layout bars (Dark blue and gold strip)
    draw.rectangle([(0, poster_h - 380), (poster_w, poster_h)], fill=(11, 17, 30, 230))
    draw.rectangle([(0, poster_h - 385), (poster_w, poster_h - 380)], fill=(212, 175, 55, 255))
    
    final_img = Image.alpha_composite(img, overlay).convert("RGB")
    draw_final = ImageDraw.Draw(final_img)
    
    # Typography rendering (System default)
    draw_final.text((540, poster_h - 260), title.upper(), fill=(255, 255, 255), anchor="mm")
    draw_final.text((540, poster_h - 150), "EXCLUSIVELY MARKETED BY:", fill=(212, 175, 55), anchor="mm")
    draw_final.text((540, poster_h - 90), agency.upper(), fill=(255, 255, 255), anchor="mm")
    
    return final_img

# 4. CAPTION & VISUAL GENERATION PROTOCOLS
with col2:
    st.subheader("✨ Generated Output")
    
    if st.button("Generate Marketing Assets", type="primary"):
        if not property_details or not agency_name or not property_title:
            st.error("Error: Please fill in all text input fields first.")
        else:
            with st.spinner("Writing elite listing copy..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=f"Write a luxury property listing caption for: {property_details}. Include agency details: {agency_name}"
                    )
                    st.write("**📝 Marketing Masterpiece:**")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"AI Generation Error: {str(e)}")
            
            if uploaded_file is not None:
                with st.spinner("Compiling luxury marketing poster..."):
                    try:
                        poster = create_poster(uploaded_file, agency_name, property_title)
                        st.image(poster, caption="Your Custom Marketing Poster", use_container_width=True)
                        
                        buf = io.BytesIO()
                        poster.save(buf, format="JPEG", quality=95)
                        byte_im = buf.getvalue()
                        
                        st.download_button(
                            label="📥 Download High-Res Poster",
                            data=byte_im,
                            file_name="property_marketing_poster.jpg",
                            mime="image/jpeg"
                        )
                    except Exception as e:
                        st.error(f"Poster compilation error: {str(e)}")
            else:
                st.info("💡 Tip: Upload an image in the left panel to output your visual poster alongside the copy.")
