import os
import streamlit as st
from openai import OpenAI
import docx
from PyPDF2 import PdfReader

# Load API key securely
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Career Guider App", layout="wide")

st.title("💼 Career Guider App")
st.write("Upload your resume and job description to get AI-powered career guidance.")

# -------------------------------
# Helper functions
# -------------------------------
def read_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def read_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

# -------------------------------
# Resume Input
# -------------------------------
st.subheader("Resume Input")
resume_option = st.radio("Choose input method:", ["Upload File", "Paste Text"], key="resume_option")

resume_text = ""
if resume_option == "Upload File":
    uploaded_resume = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"], key="resume_uploader")
    if uploaded_resume:
        if uploaded_resume.type == "application/pdf":
            resume_text = read_pdf(uploaded_resume)
        elif uploaded_resume.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = read_docx(uploaded_resume)
else:
    resume_text = st.text_area("Paste your resume text here:", key="resume_input")

# -------------------------------
# Job Description Input
# -------------------------------
st.subheader("Job Description Input")
job_option = st.radio("Choose input method:", ["Upload File", "Paste Text"], key="job_option")

job_description = ""
if job_option == "Upload File":
    uploaded_job = st.file_uploader("Upload Job Description (PDF/DOCX)", type=["pdf", "docx"], key="job_uploader")
    if uploaded_job:
        if uploaded_job.type == "application/pdf":
            job_description = read_pdf(uploaded_job)
        elif uploaded_job.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            job_description = read_docx(uploaded_job)
else:
    job_description = st.text_area("Paste the job description here:", key="job_input")

# -------------------------------
# Analyze
# -------------------------------
if st.button("🔍 Analyze M
