import os

# Clear proxy settings before importing clients that may inspect them.
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
os.environ["no_proxy"] = "*"

import streamlit as st
import requests


def clear_proxy_settings() -> None:
    """Avoid local proxy settings that can block outbound API calls."""
    for key in list(os.environ.keys()):
        if "proxy" in key.lower() and key.lower() != "no_proxy":
            os.environ.pop(key, None)
    os.environ["no_proxy"] = "*"


def get_api_key() -> str | None:
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except FileNotFoundError:
        pass
    return os.environ.get("GEMINI_API_KEY")


clear_proxy_settings()

st.set_page_config(page_title="Apex Real Estate Automation", layout="centered")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0B111E;
        color: #F1F5F9;
    }
    h1 {
        color: #38BDF8 !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
    }
    .stTextArea textarea {
        background-color: #1E293B !important;
        color: #FFFFFF !important;
        border: 1px solid #475569 !important;
        border-radius: 8px;
    }
    .stButton button {
        border-radius: 8px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("APEX // AI Real Estate Suite")
st.write(
    "Convert raw property criteria into polished, high-converting international marketing copy."
)

property_details = st.text_area(
    "PROPERTY SPECIFICATIONS:",
    placeholder=(
        "e.g., 3-bedroom penthouse in London, private balcony, marble countertops, "
        "5 mins from transit..."
    ),
)

if st.button("Generate Premium Marketing Copy", type="primary"):
    api_key = get_api_key()

    if not property_details.strip():
        st.error("Please provide property data before generating copy.")
    elif not api_key:
        st.error(
            "Missing Gemini API key. Add GEMINI_API_KEY to your environment or "
            "Streamlit secrets."
        )
    else:
        with st.spinner("Analyzing property details and generating copy..."):
            try:
                url = (
                    "https://generativelanguage.googleapis.com/v1beta/models/"
                    f"gemini-2.5-flash:generateContent?key={api_key}"
                )
                payload = {
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": (
                                        "Write a luxury property listing caption for: "
                                        f"{property_details.strip()}"
                                    )
                                }
                            ]
                        }
                    ],
                    "systemInstruction": {
                        "parts": [
                            {
                                "text": (
                                    "You are an elite real estate copywriter for premium agencies "
                                    "in the US and UK. Take raw property specs and structure them "
                                    "into a high-end social media listing. Include an attention-"
                                    "grabbing hook sentence, a clean bulleted list of features, "
                                    "a call to action to book viewings, and professional hashtags. "
                                    "Do not use filler talk."
                                )
                            }
                        ]
                    },
                }

                session = requests.Session()
                session.trust_env = False
                response = session.post(
                    url,
                    json=payload,
                    proxies={"http": None, "https": None},
                    timeout=60,
                )

                if response.status_code == 200:
                    response_data = response.json()
                    output_text = response_data["candidates"][0]["content"]["parts"][0][
                        "text"
                    ]
                    st.subheader("Generated Marketing Copy")
                    st.write(output_text)
                else:
                    st.error(
                        f"Google API returned an error ({response.status_code}): "
                        f"{response.text}"
                    )
            except Exception as exc:
                st.error(f"Network processing failed: {exc}")
                st.info(
                    "Tip: If you are using a VPN, try toggling it and running the "
                    "request again."
                )
