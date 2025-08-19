import streamlit as st
import PyPDF2
import docx
import openai
import os

# Set your OpenAI API key from environment variable (better than hardcoding)
openai.api_key = os.getenv("OPENAI_API_KEY")

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

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",   # Lightweight but good for reasoning
        messages=[{"role": "system", "content": "You are an expert career advisor."},
                  {"role": "user", "content": prompt}],
        max_tokens=600
    )
    return response["choices"][0]["message"]["content"]

# --- Chatbot function ---
def career_chatbot(question, resume_text):
    prompt = f"""
    Resume: {resume_text}

    Question: {question}

    Answer as a helpful career counselor with clear reasoning.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a career guidance assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=300
    )
    return response["choices"][0]["message"]["content"]

# --- File Upload ---
uploaded_file = st.file_uploader("📂 Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    else:
        resume_text = extract_text_from_docx(uploaded_file)

    st.success("✅ Resume uploaded successfully!")
    st.subheader("📊 Career Guidance Results")
    result = analyze_resume(resume_text)
    st.write(result)

    # Chatbot Section
    st.subheader("💬 Ask Career Questions")
    user_question = st.text_input("Enter your question:")
    if st.button("Ask"):
        if user_question.strip():
            answer = career_chatbot(user_question, resume_text)
            st.write("### 🤖 Career Bot says:")
            st.write(answer)
