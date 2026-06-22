import streamlit as st
from google import genai
import base64

# 1. INITIALIZE GEMINI CLIENT
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

st.set_page_config(page_title="Apex Real Estate Suite", layout="wide")

# Inject premium Montserrat Google font directly into the web interface
st.markdown("""
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700;800&display=swap">
    <style>
    .stApp { background-color: #0F172A; color: #F8FAFC; font-family: 'Montserrat', sans-serif; }
    h1 { font-weight: 800; color: #38BDF8 !important; }
    h3 { font-weight: 700; color: #F1F5F9 !important; }
    div[data-testid="stFileUploader"] { background-color: #1E293B; border: 2px dashed #475569; border-radius: 12px; }
    .stButton>button { background: linear-gradient(135deg, #D4AF37 0%, #AA7C11 100%) !important; color: white !important; font-weight: 700; border: none !important; border-radius: 8px; padding: 12px 24px; }
    </style>
""", unsafe_with_html=True)

st.title("🏡 APEX // AI Elite Real Estate Suite")
st.write("Generate modern, magazine-grade marketing visuals and copy in real-time.")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📋 Property Assets & Details")
    agency_name = st.text_input("AGENCY NAME:", placeholder="e.g., AYAN AN ALI AGENCY")
    property_title = st.text_input("PROPERTY TITLE:", placeholder="e.g., THE LUXURY PENTHOUSE")
    property_price = st.text_input("LISTING PRICE:", placeholder="e.g., $4,250,000")
    
    property_details = st.text_area(
        "RAW SPECIFICATIONS:", 
        placeholder="e.g., 3 bedrooms, floor-to-ceiling panoramic glass windows, private infinity terrace, premium marble finishings..."
    )
    
    uploaded_file = st.file_uploader("UPLOAD HIGH-RES PHOTO:", type=["jpg", "jpeg", "png"])

with col2:
    st.subheader("✨ Premium Finished Output")
    
    if st.button("Generate Elite Marketing Package", type="primary"):
        if not property_details or not agency_name or not property_title:
            st.error("Error: Please provide all text configuration fields in the left column.")
        else:
            # Step A: Generate Elite Ad Copy
            with st.spinner("AI Copywriter crafting luxury pitch..."):
                try:
                    prompt_text = f"Write an ultra-luxury real estate listing caption for: {property_details}. Highlight the prestige. Agency: {agency_name}. End with 5 trending high-converting real estate hashtags."
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt_text
                    )
                    st.write("### 📝 Luxury Listing Copy")
                    st.write(response.text)
                    st.markdown("---")
                except Exception as e:
                    st.error(f"AI Generation Error: {str(e)}")
            
            # Step B: Render Professional Poster Layout via Clean HTML/CSS Canvas
            if uploaded_file is not None:
                with st.spinner("Compiling luxury digital poster..."):
                    try:
                        # Convert image data safely to Base64 to inject directly into the HTML graphic layout
                        bytes_data = uploaded_file.getvalue()
                        encoded_img = base64.b64encode(bytes_data).decode("utf-8")
                        img_type = uploaded_file.type
                        img_data_url = f"data:{img_type};base64,{encoded_img}"
                        
                        # High-End Design Frame (Clean typography, edge-to-edge bleed, frosted dark contrast cards)
                        poster_html = f"""
                        <div style="
                            width: 100%;
                            max-width: 550px;
                            height: 680px;
                            border-radius: 20px;
                            background-image: url('{img_data_url}');
                            background-size: cover;
                            background-position: center;
                            position: relative;
                            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
                            font-family: 'Montserrat', sans-serif;
                            overflow: hidden;
                            margin: 20px auto;
                            border: 1px solid rgba(255, 255, 255, 0.1);
                        ">
                            <div style="position: absolute; top:0; left:0; width:100%; height:150px; background: linear-gradient(to bottom, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0) 100%); z-index: 1;"></div>
                            
                            <div style="
                                position: absolute;
                                bottom: 0;
                                left: 0;
                                width: 100%;
                                background: linear-gradient(to top, rgba(15, 23, 42, 0.98) 0%, rgba(15, 23, 42, 0.85) 75%, rgba(15, 23, 42, 0) 100%);
                                padding: 60px 30px 40px 30px;
                                box-sizing: border-box;
                                z-index: 2;
                                display: flex;
                                flex-direction: column;
                                justify-content: flex-end;
                            ">
                                <div style="width: 60px; height: 4px; background: linear-gradient(90deg, #D4AF37, #F3E5AB); margin-bottom: 20px; border-radius: 2px;"></div>
                                
                                <h2 style="color: #FFFFFF; font-size: 28px; font-weight: 800; text-transform: uppercase; margin: 0 0 8px 0; letter-spacing: 1.5px; line-height: 1.2; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">{property_title}</h2>
                                
                                <div style="color: #D4AF37; font-size: 24px; font-weight: 700; margin-bottom: 30px; letter-spacing: 1px;">{property_price}</div>
                                
                                <div style="width: 100%; height: 1px; background: rgba(255,255,255,0.1); margin-bottom: 20px;"></div>
                                
                                <div style="font-size: 11px; color: #94A3B8; font-weight: 400; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 4px;">Exclusively Marketed By</div>
                                <div style="font-size: 18px; color: #FFFFFF; font-weight: 700; text-transform: uppercase; letter-spacing: 2px;">{agency_name}</div>
                            </div>
                        </div>
                        """
                        
                        st.write("### 🖼️ Professional Digital Asset")
                        st.markdown(poster_html, unsafe_with_html=True)
                        st.caption("✨ Tip: To save this high-resolution visual layout to your device instantly, right-click inside the image card frame and select 'Save Image As' or take a quick crisp screenshot for Instagram Stories.")
                    except Exception as e:
                        st.error(f"Visual asset generation failed: {str(e)}")
            else:
                st.info("💡 To view the premium visual asset layout, upload a high-resolution property photograph in the left input panel.")
