import streamlit as st
import os
from dotenv import load_dotenv
from memory import create_table, save_translation, get_all_translations, clear_translations
import requests
from langdetect import detect
from langcodes import Language
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import speech_recognition as sr
import av
import numpy as np
from enum import Enum  # ✅ workaround for StreamingMode

# ✅ Manually define the StreamingMode enum
class StreamingMode(Enum):
    SENDRECV = "SENDRECV"
    SENDONLY = "SENDONLY"
    RECVONLY = "RECVONLY"

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure Streamlit
st.set_page_config(page_title="🌍 Multilingual Translator", layout="centered")

# Sidebar
with st.sidebar:
    st.title("🧭 Translator Dashboard")
    st.markdown("**👩‍💻 Built by Alisha Khan**")
    st.markdown("✅ Auto-language detection")
    st.markdown("🎙️ Speech-to-text supported")
    if st.button("🗑️ Clear All Memory"):
        clear_translations()
        st.success("All stored translations deleted.")

# Title
st.title("🌍 Multilingual Translator")
st.caption("🎯 Translate anything into any language with memory & voice")

# Create table in DB
create_table()

# 🎤 Speech-to-text using WebRTC
st.subheader("🎤 Speak Instead (Optional)")

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray()
        audio = np.mean(audio, axis=1).astype(np.int16).tobytes()
        try:
            audio_data = sr.AudioData(audio, frame.sample_rate, 2)
            text = self.recognizer.recognize_google(audio_data)
            st.session_state["user_input"] = text
            st.success(f"🎙️ You said: {text}")
        except sr.UnknownValueError:
            pass
        return frame

# ✅ Fixed: using enum value
webrtc_streamer(
    key="speech",
    mode=StreamingMode.SENDONLY,
    audio_processor_factory=AudioProcessor
)

# Text input field
user_input = st.text_area("✍️ Enter text (or use mic above)", st.session_state.get("user_input", ""))

# Auto-detect source language
if user_input:
    try:
        detected_code = detect(user_input)
        detected_lang = Language.get(detected_code).display_name()
        st.info(f"🌐 Detected Language: **{detected_lang}** ({detected_code})")
    except:
        st.warning("⚠️ Could not auto-detect the language.")

# Target language input
target_language = st.text_input("🌐 Translate to (e.g. Urdu, French, Arabic)", "")

# Translate button
if st.button("🔁 Translate"):
    if user_input and target_language:
        instruction = f"You are a multilingual translator. Detect the source language and translate the following into {target_language}. Respond only with the translated result."

        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_api_key}"
            headers = {"Content-Type": "application/json"}
            data = {
                "contents": [ { "parts": [ { "text": instruction + "\n" + user_input } ] } ]
            }

            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            translated_text = response.json()['candidates'][0]['content']['parts'][0]['text']

            st.success(f"🔤 Translated to {target_language}:")
            st.write(translated_text)

            save_translation(user_input, translated_text, target_language)

        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("Please fill both the input text and target language.")

# Display Memory
translations = get_all_translations()
if translations:
    with st.expander("🧠 View Your Stored Translations"):
        for t in reversed(translations):
            st.markdown(f"- **{t[1]}** → *({t[3]})* ➜ {t[2]}")
