import streamlit as st
from google import genai
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.request

# 1. LUXURY DASHBOARD CONFIGURATION (Fixes HTML injection crashes)
st.set_page_config(
    page_title="Apex Real Estate Suite",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Gemini Client Securely
api_key = st.secrets.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=api_key) if api_key else None

# Initialize persistent memory block for text output
if "generated_copy" not in st.session_state:
    st.session_state["generated_copy"] = "Click 'Generate / Refresh Text Package' below to populate your workspace copy."

# 2. SIDEBAR CONTROL PANEL
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
    st.markdown("### 📸 ASSET MANAGER")
    uploaded_file = st.file_uploader("UPLOAD HIGH-RES PHOTO:", type=["jpg", "jpeg", "png"])

    st.markdown("---")
    st.markdown("### ⚙️ GENERATION MODE")
    mode = st.radio("COPY ENGINE MODE:", ["Offline (Manual Input)", "Live AI Generation"])
    
    manual_caption = ""
    if mode == "Offline (Manual Input)":
        manual_caption = st.text_area(
            "WRITE YOUR OWN CAPTION:", 
            value="Type or paste your luxury listing copy here to preview it in the tab panel..."
        )

# 3. MAIN WORKSPACE DISPLAY
st.title("🏡 APEX // Elite Real Estate Suite")
st.write("Format magazine-grade property copy and compile structural marketing assets simultaneously.")

# Workspace output frame
with st.container(border=True):
    st.markdown("### ✨ Studio Workspace Output")
    
    tab1, tab2 = st.tabs(["📝 Formatted Copy Preview", "🖼️ Interactive Media Poster"])
    
    with tab1:
        st.markdown("#### 📄 Listing Copy Output")
        
        # Primary Action Trigger for Text Generation
        if st.button("Generate / Refresh Text Package", type="primary"):
            if mode == "Live AI Generation":
                if not client:
                    st.error("API Error: GEMINI_API_KEY secret is missing inside Streamlit Secrets.")
                elif not property_details or not agency_name:
                    st.error("Error: Please provide values for Agency Name and Specifications first.")
                else:
                    with st.spinner("Requesting description from Gemini..."):
                        try:
                            prompt_text = f"Write an ultra-luxury real estate listing description for: {property_details}. Focus on architectural elegance. Agency: {agency_name}. Conclude directly with 6 high-traffic real estate hashtags."
                            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt_text)
                            st.session_state["generated_copy"] = response.text
                        except Exception as e:
                            st.error(f"AI text model failed (Quota Exceeded): {str(e)}")
                            st.info("💡 Tip: Switch the Generation Mode in the sidebar to 'Offline' to manage your copy manually today.")
            else:
                st.session_state["generated_copy"] = manual_caption

        # Display editable text area block
        st.text_area(label="Active Workspace Copy Block:", value=st.session_state["generated_copy"], height=300)

    with tab2:
        st.markdown("#### 🖨️ Production Asset Composite")
        
        if uploaded_file is not None:
            try:
                # 4. ROBUST PIL CANVAS RENDERING LOGIC
                base_img = Image.open(uploaded_file).convert("RGBA")
                poster_w, poster_h = 1200, 1500
                
                # Aspect-ratio preservation cropping math
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
                
                # Dark Translucent Panel Card Placement (Bottom 480px)
                draw.rectangle([(0, poster_h - 480), (poster_w, poster_h)], fill=(11, 17, 30, 245))
                # Accent Luxury Gold Separator Strip
                draw.rectangle([(0, poster_h - 486), (poster_w, poster_h - 480)], fill=(212, 175, 55, 255))
                
                final_img = Image.alpha_composite(base_img, overlay).convert("RGB")
                draw_final = ImageDraw.Draw(final_img)
                
                # Typography Stream From Google Fonts (Montserrat Bold)
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
                
                # Type Alignment Matrix (Centered Layout)
                draw_final.text((600, poster_h - 370), property_title.upper(), fill=(255, 255, 255), anchor="mm", font=title_font)
                if property_price:
                    draw_final.text((600, poster_h - 280), property_price.upper(), fill=(212, 175, 55), anchor="mm", font=price_font)
                draw_final.text((600, poster_h - 175), "EXCLUSIVELY MARKETED BY:", fill=(148, 163, 184), anchor="mm", font=label_font)
                draw_final.text((600, poster_h - 110), agency_name.upper(), fill=(255, 255, 255), anchor="mm", font=agency_font)
                
                # Render Graphic inside the UI layout window
                st.image(final_img, caption="Live Layout Core Preview", use_container_width=True)
                
                # Export image stream compiler
                buf = io.BytesIO()
                final_img.save(buf, format="JPEG", quality=98)
                
                st.download_button(
                    label="📥 Download Master High-Res JPG Asset",
                    data=buf.getvalue(),
                    file_name="luxury_marketing_poster.jpg",
                    mime="image/jpeg",
                    use_container_width=True
                )
            except Exception as render_err:
                st.error(f"Render System Notice: {str(render_err)}")
        else:
            st.info("💡 Drop a raw listing image file directly into the sidebar Asset Manager panel to generate your typographic frame layouts live.")
