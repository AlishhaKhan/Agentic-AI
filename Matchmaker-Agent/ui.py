import streamlit as st
from agent import get_match_recommendation  # ✅ Updated function name
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="💘 AI Matchmaker",
    page_icon="💘",
    layout="centered"
)

# ---------- Custom CSS ----------
st.markdown(
    """
    <style>
        .stApp {
            background-image: url('https://images.unsplash.com/photo-1518544803493-c164d89b3f87');
            background-size: cover;
            background-attachment: fixed;
            padding: 2rem;
        }
        .main-card {
            background-color: rgba(255, 255, 255, 0.92);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.2);
        }
        .match-title {
            text-align: center;
            font-weight: bold;
            font-size: 32px;
            color: #e91e63;
        }
        .footer {
            text-align: center;
            font-size: 14px;
            margin-top: 2rem;
            color: gray;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- App UI ----------
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="match-title">💘 AI Matchmaker Agent</div>', unsafe_allow_html=True)
    st.write("Find your perfect partner powered by AI! 💑")

    with st.form("match_form"):
        name = st.text_input("Your Name")
        age = st.slider("Your Age", 18, 60, 25)
        gender = st.radio("Your Gender", ["Female", "Male", "Other"])
        interests = st.text_area("Your Hobbies / Interests")
        looking_for = st.text_input("What kind of partner are you looking for?")
        submit = st.form_submit_button("Find My Match 💌")

    # ---------- Logic ----------
    if submit:
        if not name or not interests or not looking_for:
            st.warning("Please fill out all fields before submitting.")
        else:
            with st.spinner("Thinking... 💭"):
                prompt = (
                    f"My name is {name}, I'm a {age}-year-old {gender}. "
                    f"My interests include {interests}. "
                    f"I'm looking for a partner who is {looking_for}."
                )
                try:
                    # ✅ Updated function call
                    reply = get_match_recommendation(prompt)
                    st.success("💘 Here's your potential match:")
                    st.write(reply)
                except Exception as e:
                    st.error("⚠️ An error occurred. Please try again later.")
                    st.exception(e)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown('<div class="footer">Made with ❤️ by Alisha | Powered by Agentic AI</div>', unsafe_allow_html=True)
