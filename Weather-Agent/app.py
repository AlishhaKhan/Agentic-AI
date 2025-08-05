import streamlit as st
import requests
from langdetect import detect
from langcodes import Language
from geopy.geocoders import Nominatim
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import speech_recognition as sr
import av
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pycountry

# Page Setup
st.set_page_config(page_title="🌤️ Weather Agent", layout="centered")

# ------------------ Sidebar ------------------
with st.sidebar:
    st.markdown("## 🌐 Weather Agent")
    st.image("https://img.icons8.com/fluency/96/000000/partly-cloudy-day.png", width=100)
    st.markdown("---")
    st.markdown("**🔍 Features:**")
    st.markdown("- 🌍 Auto language detection\n- 🎙️ Voice input\n- 📍 Location-based forecast")
    st.markdown("---")
    st.markdown("📌 **Developed by:** Alisha Khan")
    st.markdown("🔖 **Version:** 1.0.0")
    st.markdown("[🌐 GitHub](https://github/AlishhaKhan.com/) | [📧 Contact](alishakhan8627@gmail.com)", unsafe_allow_html=True)

# ------------------ Title ------------------
st.title("🌦️ Multilingual Weather Agent")
st.markdown("Enter or speak a city name below 👇")

# ------------------ Audio Input ------------------
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio_data = frame.to_ndarray().tobytes()
        try:
            audio = sr.AudioData(audio_data, frame.sample_rate, 2)
            text = self.recognizer.recognize_google(audio)
            st.session_state["city"] = text
            st.success(f"🎙️ You said: {text}")
        except:
            pass
        return frame

webrtc_streamer(
    key="mic",
    mode=WebRtcMode.SENDONLY,
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True, "video": False}
)

# ------------------ City Input ------------------
st.markdown("### 🏙️ City Input")
city = st.text_input("Type city name:", value=st.session_state.get("city", ""))

# ------------------ Language Detection ------------------
if city:
    try:
        code = detect(city)
        lang_name = Language.get(code).display_name()
        lang_name_cap = lang_name.capitalize()

        # Try to find country code for flag emoji
        country = pycountry.languages.get(alpha_2=code)
        emoji_flag = f":flag-{code}:" if country else ""
        st.info(f"🌐 Detected Language: {emoji_flag} **{lang_name_cap}**")
    except:
        st.warning("⚠️ Could not detect language.")

# ------------------ Weather Data ------------------
if st.button("☁️ Get Weather") and city:
    with st.spinner("Fetching weather data..."):
        try:
            geolocator = Nominatim(user_agent="weather-agent")
            location = geolocator.geocode(city)
            if location:
                lat, lon = location.latitude, location.longitude
                api_url = (
                    f"https://api.open-meteo.com/v1/forecast?"
                    f"latitude={lat}&longitude={lon}"
                    f"&current_weather=true&hourly=temperature_2m"
                    f"&timezone=auto"
                )
                response = requests.get(api_url)
                data = response.json()

                current = data.get("current_weather", {})
                hourly_temps = data.get("hourly", {}).get("temperature_2m", [])
                time_stamps = data.get("hourly", {}).get("time", [])

                st.success("✅ Weather data fetched successfully!")

                # 🌡️ Current Weather
                st.metric(label="🌡️ Current Temperature (°C)", value=current.get("temperature"))

                # 📍 Map View
                st.markdown("### 🗺️ City Location")
                st.map(data=[{"lat": lat, "lon": lon}])

                # 📊 Hourly Forecast with Time
                st.markdown("### 📊 Hourly Temperature Forecast (Next 12 Hours)")
                times = [datetime.fromisoformat(t) for t in time_stamps[:12]]
                fig, ax = plt.subplots()
                ax.plot(times, hourly_temps[:12], marker='o')
                ax.set_xlabel("Time")
                ax.set_ylabel("Temperature (°C)")
                ax.set_title("Hourly Forecast")
                ax.grid(True)
                plt.xticks(rotation=30)
                st.pyplot(fig)
            else:
                st.error("❌ City not found. Please try again.")
        except Exception as e:
            st.error(f"⚠️ Error: {e}")
