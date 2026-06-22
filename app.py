import streamlit as st
from google import genai
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import io
import os

# --- 1. INITIALIZE GEMINI CLIENT ---
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

# --- 2. ELITE VISUAL CONFIGURATION ---
st.set_page_config(page_title="Apex Real Estate Suite", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0B111E; color: #F1F5F9; }
    h1 { color: #F1F5F9 !important; font-family: 'Montserrat', sans-serif; }
    h3 { color: #38BDF8 !important; }
    div[data-testid="stFileUploader"] { background-color: #1E293B; border: 2px dashed #475569; border-radius: 12px; }
    .stButton>button { background-color: #38BDF8 !important; color: #0B111E !important; font-weight: 700; border-radius: 8px; }
    </style>
""", unsafe_with_html=True)

st.title("🏡 APEX // AI Real Estate Suite")
st.write("Generate elite, high-converting marketing copy and professional-grade visual posters simultaneously.")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📋 Property Information")
    agency_name = st.text_input("AGENCY NAME:", placeholder="e.g., Ayan an Ali Agency")
    property_title = st.text_input("PROPERTY TITLE:", placeholder="e.g., THE PENTHOUSE AT SKYLINE")
    property_price = st.text_input("PRICE (Optional):", placeholder="e.g., $4,500,000")
    
    property_details = st.text_area(
        "RAW SPECIFICATIONS:", 
        placeholder="e.g., 3-bedroom, floor-to-ceiling windows, panoramic mountain views, private terrace..."
    )
    
    uploaded_file = st.file_uploader("UPLOAD HIGH-RES IMAGE:", type=["jpg", "jpeg", "png"])

# --- 3. THE ELITE POSTER ENGINE ---
def create_elite_poster(image_file, agency, title, price):
    # Set defined resolution (Vertical A4 ratio)
    target_w, target_h = 1414, 2000
    
    # 3a. Process Base Image (Full Bleed)
    base_img = Image.open(image_file).convert("RGB")
    
    # Precise center-cropping to maintain visual flow and cover the full frame
    img_ratio = base_img.width / base_img.height
    target_ratio = target_w / target_h
    
    if img_ratio > target_ratio:
        new_width = int(target_h * img_ratio)
        base_img = base_img.resize((new_width, target_h), Image.Resampling.LANCZOS)
        left = (base_img.width - target_w) / 2
        base_img = base_img.crop((left, 0, left + target_w, target_h))
    else:
        new_height = int(target_w / img_ratio)
        base_img = base_img.resize((target_w, new_height), Image.Resampling.LANCZOS)
        top = (base_img.height - target_h) / 2
        base_img = base_img.crop((0, top, target_w, top + target_h))

    # 3b. Create Dark "Glassmorphism" Text Backdrop and Graphics layer
    overlay_graphics = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay_graphics)
    
    # Defined professional colors
    gold_accent = (212, 175, 55, 255)
    text_light = (241, 245, 249, 255)
    text_white = (255, 255, 255, 255)
    text_dark = (11, 17, 30, 255)

    # Glassmorphism/Dark Blurred Panel at the bottom
    panel_height = 650
    draw.rectangle([(0, target_h - panel_height), (target_w, target_h)], fill=(11, 17, 30, 210))
    # Elegant single gold rule line
    draw.rectangle([(0, target_h - panel_height), (target_w, target_h - panel_height + 8)], fill=gold_accent)

    # 3c. Initialize Professional Fonts (Must exist in /assets)
    assets_path = "assets" # Point to the new assets folder
    font_bold = ImageFont.truetype(os.path.join(assets_path, "bold.ttf"), 110)
    font_price = ImageFont.truetype(os.path.join(assets_path, "bold.ttf"), 160)
    font_agency = ImageFont.truetype(os.path.join(assets_path, "light.ttf"), 60)
    font_marketing_tag = ImageFont.truetype(os.path.join(assets_path, "light.ttf"), 60)
    
    # 3d. Draw Typography onto Graphics Layer
    # Centered Title (All Caps)
    draw.text((target_w/2, target_h - 480), title.upper(), fill=text_white, anchor="mm", font=font_bold)
    
    # Centered Price (If provided)
    if price:
        draw.text((target_w/2, target_h - 320), price, fill=gold_accent, anchor="mm", font=font_price)
        draw.text((target_w/2, target_h - 180), "EXCLUSIVELY MARKETED BY:", fill=text_light, anchor="mm", font=font_marketing_tag)
        draw.text((target_w/2, target_h - 100), agency.upper(), fill=text_white, anchor="mm", font=font_agency)
    else:
        # Layout adjustment if no price (Title lowered)
        draw.text((target_w/2, target_h - 220), "EXCLUSIVELY MARKETED BY:", fill=text_light, anchor="mm", font=font_marketing_tag)
        draw_final.text((target_w/2, target_h - 140), agency.upper(), fill=text_white, anchor="mm", font=font_agency)

    # 3e. Composite and Apply Branding (Logo)
    final_poster = Image.alpha_composite(base_img.convert("RGBA"), overlay_graphics)
    
    # Integrated Agency Logo (Must exist in /assets/logo.png)
    logo_src = Image.open(os.path.join(assets_path, "logo.png")).convert("RGBA")
    logo_w, logo_h = logo_src.size
    
    # Scale logo and place it bottom-right
    new_logo_w = 400
    new_logo_h = int(logo_h * (new_logo_w / logo_w))
    logo_scaled = logo_src.resize((new_logo_w, new_logo_h), Image.Resampling.LANCZOS)
    
    final_poster.paste(logo_scaled, (target_w - new_logo_w - 80, target_h - new_logo_h - 60), logo_scaled)
    
    return final_poster.convert("RGB")

# --- 4. GENERATION PROTOCOLS ---
with col2:
    st.subheader("✨ Final Assets")
    
    if st.button("Generate Professional Package", type="primary"):
        if not property_details or not agency_name or not property_title:
            st.error("Error: Complete the left panel details first.")
        else:
            with st.spinner("AI Copywriter creating polished listing..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=(
                            f"Write a high-converting, luxury property listing for: {property_details}. "
                            f"Focus on the view and architecture. Agency: {agency_name}. Add 5 trending real estate hashtags."
                        )
                    )
                    st.write("**📝 High-Converting Copy:**")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"AI Generation Failed: {str(e)}")
            
            # Execute Elite Poster Graphics Generator
            if uploaded_file is not None:
                with st.spinner("Compiling professional-grade poster..."):
                    try:
                        poster = create_elite_poster(uploaded_file, agency_name, property_title, property_price)
                        st.image(poster, caption="Professional Visual Asset", use_container_width=True)
                        
                        # Convert to downloadable JPEG
                        buf = io.BytesIO()
                        poster.save(buf, format="JPEG", quality=98)
                        byte_im = buf.getvalue()
                        
                        st.download_button(
                            label="📥 Download High-Res Poster",
                            data=byte_im,
                            file_name="APEX_Property_Poster.jpg",
                            mime="image/jpeg"
                        )
                    except FileNotFoundError:
                        st.error("Visual Error: Make sure your logo.png, bold.ttf, and light.ttf are in the /assets/ folder on GitHub.")
                    except Exception as e:
                        st.error(f"Visual compilation error: {str(e)}")
            else:
                st.info("💡 Tip: Upload an image on the left panel to output your custom visual asset alongside the copy.")
