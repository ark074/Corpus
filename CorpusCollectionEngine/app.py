
import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Corpus Collection Engine", layout="centered")
st.title("🧠 Corpus Collection Engine")

LANGUAGES = {
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Bengali": "bn",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Gujarati": "gu",
    "Odia": "or",
    "Marathi": "mr",
    "English": "en"
}

data_file = "data/data.csv"
os.makedirs("data/uploads", exist_ok=True)

if not os.path.exists(data_file):
    df = pd.DataFrame(columns=["Timestamp", "Language", "Text", "Audio", "Video", "Image", "Caption"])
    df.to_csv(data_file, index=False)

st.header("📥 Contribute Data")

with st.form("upload_form", clear_on_submit=True):
    lang = st.selectbox("Select Language", list(LANGUAGES.keys()))
    text = st.text_area("Enter sentence / phrase")
    audio_file = st.file_uploader("Upload audio", type=["mp3", "wav", "m4a"])
    video_file = st.file_uploader("Upload video", type=["mp4", "mkv", "avi"])
    image_file = st.file_uploader("Upload image (optional)", type=["jpg", "jpeg", "png"])
    caption = st.text_input("Caption for image (optional)")
    submitted = st.form_submit_button("Submit")

    if submitted:
        ts = datetime.now().isoformat()
        audio_path = video_path = image_path = ""

        def save_file(uploaded_file, subfolder):
            if uploaded_file:
                save_path = os.path.join("data/uploads", subfolder + "_" + uploaded_file.name)
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                return save_path
            return ""

        audio_path = save_file(audio_file, "audio")
        video_path = save_file(video_file, "video")
        image_path = save_file(image_file, "image")

        new_data = pd.DataFrame([{
            "Timestamp": ts,
            "Language": LANGUAGES[lang],
            "Text": text,
            "Audio": audio_path,
            "Video": video_path,
            "Image": image_path,
            "Caption": caption
        }])

        new_data.to_csv(data_file, mode="a", header=False, index=False)
        st.success("✅ Data submitted successfully!")

st.markdown("---")
st.subheader("📊 Download Collected Data")
with open(data_file, "rb") as f:
    st.download_button("Download CSV", f, file_name="corpus_data.csv", mime="text/csv")
