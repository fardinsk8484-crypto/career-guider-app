import streamlit as st
import google.generativeai as genai
import os
from PyPDF2 import PdfReader
import docx

# ========== SETUP ==========
# Get your Gemini API key from https://aistudio.google.com/app/apikey
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

# ========== HELPERS ==========
def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def get_text_from_file(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    else:
        return ""

def analyze_resume(resume_text, job_text):
    prompt = f"""
    You are a career guidance assistant. Compare the following resume with the job description
    and provide insights:
    1. Key strengths of the resume
    2. Missing skills/keywords
    3. Suggestions to improve alignment
    4. Final match score (0–100)

    Resume:
    {resume_text}

    Job Description:
    {job_text}
    """
    response = model.generate_content(prompt)
    return response.text

# ========== UI ==========
st.set_page_config(page_title="Career Guider App", layout="centered")
st.title("💼 Career Guider App")
st.write("Upload your resume and job description to get AI-powered career guidance.")

# Resume input
resume_file = st.file_uploader("Upload your Resume (PDF/DOCX)", type=["pdf", "docx"])
resume_text = ""
if resume_file:
    resume_text = get_text_from_file(resume_file)

if not resume_text:
    resume_text = st.text_area("Or paste your resume text here:")

# Job description input
job_file = st.file_uploader("Upload Job Description (PDF/DOCX)", type=["pdf", "docx"])
job_text = ""
if job_file:
    job_text = get_text_from_file(job_file)

if not job_text:
    job_text = st.text_area("Or paste the job description here:")

# Analyze button
if st.button("🔍 Analyze Match"):
    if resume_text and job_text:
        with st.spinner("Analyzing..."):
            result = analyze_resume(resume_text, job_text)
        st.subheader("📊 Career Guidance Report")
        st.write(result)
    else:
        st.error("Please provide both resume and job description.")
