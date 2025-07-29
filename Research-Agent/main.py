import os
import io
import streamlit as st
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import markdown
from xhtml2pdf import pisa

# Load env vars from .env file
load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Setup Tavily Search Tool
search_tool = TavilySearchResults(api_key=TAVILY_API_KEY)

# Setup Gemini Chat Model
llm = ChatGoogleGenerativeAI(
    api_key=GEMINI_API_KEY,
    model="gemini-1.5-flash-latest",
    temperature=0.3
)

# Streamlit page config
st.set_page_config(
    page_title="Research Agent",
    page_icon="🔎",
    layout="wide"
)

# Theming
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body, .stMarkdown, .stText, .stTextInput, .stSelectbox, .stRadio, .stSlider {
            color: #333333;
            font-family: 'Segoe UI', sans-serif;
            font-size: 16px;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #1E3A8A;
            font-family: 'Segoe UI', sans-serif;
            font-weight: 600;
        }

        .stButton > button {
            background-color: #3B82F6;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5em 1em;
            font-size: 16px;
        }
        .stButton > button:hover {
            background-color: #1E3A8A;
            color: #ffffff;
        }

        .fade-in {
            animation: fadeIn 2s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to   { opacity: 1; }
        }

        .stMarkdown a {
            color: #3B82F6;
            text-decoration: none;
            font-weight: bold;
        }
        .stMarkdown a:hover {
            color: #1E3A8A;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🔎 Research Agent - Alisha's Project")

query = st.text_input("Enter your research topic:")

num_results = st.slider(
    "Select number of search results to fetch from Tavily:",
    min_value=1,
    max_value=10,
    value=3
)

summary_style = st.radio(
    "Choose your summary style:",
    ["Short bullets", "Detailed paragraphs", "Q&A style"]
)

if st.button("Run Research") and query:
    with st.spinner("🔎 Searching..."):

        # Step 1 → Search Tavily
        search_results = search_tool.run(query, num_results=num_results)

        # Combine results
        combined_text = "\n\n".join(
            [item['content'] for item in search_results]
        )

        # Step 2 → Create prompt
        if summary_style == "Short bullets":
            style_instruction = (
                "Summarize the following into clear bullet points. "
                "Start each point on a new line with '* '."
            )
        elif summary_style == "Detailed paragraphs":
            style_instruction = (
                "Write a detailed research summary in paragraphs, using Markdown formatting."
            )
        else:
            style_instruction = (
                "Present the following research as a Q&A summary in Markdown format."
            )

        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"You are an expert research assistant. {style_instruction}"
                ),
                ("human", "{input_text}"),
            ]
        )

        formatted_prompt = prompt_template.format(input_text=combined_text)

        # Step 3 → Call Gemini
        summary = llm.invoke(formatted_prompt)

        # Clean up bullet formatting if required
        final_output = summary.content.strip()

        if summary_style == "Short bullets":
            # Ensure consistent bullet formatting
            lines = [
                f"* {line.strip()}"
                for line in final_output.replace("\n", "").split("* ")
                if line.strip()
            ]
            final_output = "\n".join(lines)

        # Step 4 → Display
        st.markdown("## 📄 Research Summary")
        st.markdown(
            f"<div class='fade-in'>{markdown.markdown(final_output)}</div>",
            unsafe_allow_html=True
        )

        # Step 5 → Generate PDF
        html_content = markdown.markdown(final_output)

        pdf_bytes = io.BytesIO()
        pisa.CreatePDF(io.StringIO(html_content), dest=pdf_bytes)
        pdf_bytes.seek(0)

        # Download button
        st.download_button(
            label="⬇️ Download Summary as PDF",
            data=pdf_bytes,
            file_name="research_summary.pdf",
            mime="application/pdf"
        )
