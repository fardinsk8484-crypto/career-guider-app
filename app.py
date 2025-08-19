import streamlit as st
import PyPDF2
import docx
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI Career Guider", page_icon="🎯", layout="wide")

st.title("🎯 AI Career Guider")
st.write("Upload your resume and get personalized career guidance with detailed explanations.")

# --- Function to extract text from PDF ---
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

# --- Function to extract text from DOCX ---
def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# --- Analyze Resume using GPT ---
def analyze_resume(resume_text):
    prompt = f"""
    You are a professional career counselor.
    The following is a resume text:

    {resume_text}

    Based on this, suggest the top 5 most suitable career options.
    Rank them in order (best first).
    For each career option, provide:
    - Job Title
    - Why this is a good fit
    - Skills from resume that support this
    - Possible growth opportunities
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",   # Lightweight but good for reasoning
        messages=[
            {"role": "system", "content": "You are an expert career advisor."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=600
    )
    return response.choices[0].message.content

# --- Chatbot function ---
def care

