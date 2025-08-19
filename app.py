import streamlit as st
import openai
import os

# Load API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize OpenAI client
client = openai.OpenAI(api_key=openai.api_key)


# --- Function to analyze resume ---
def analyze_resume(resume_text):
    prompt = f"""
    You are a career guidance expert.
    Analyze the following resume and provide:
    1. Key strengths
    2. Possible weaknesses
    3. Best-fit career paths
    4. Skills to improve
    Resume: {resume_text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",   # lightweight, fast model
        messages=[
            {"role": "system", "content": "You are a professional career counselor."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=600
    )
    return response.choices[0].message.content


# --- Chatbot function ---
def career_chatbot(question, resume_text):
    prompt = f"""
    Resume: {resume_text}

    Question: {question}

    Answer as a helpful career counselor with clear reasoning.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a career guidance assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    return response.choices[0].message.content


# --- Streamlit UI ---
st.set_page_config(page_title="Career Guider App", page_icon="🎯", layout="wide")
st.title("🎯 Career Guider App")

st.write("Upload your resume or paste text to get personalized career guidance.")

# File upload
uploaded_file = st.file_uploader("Upload your resume (.txt format)", type=["txt"])

resume_text = ""
if uploaded_file is not None:
    resume_text = uploaded_file.read().decode("utf-8")
elif st.text_area("Or paste your resume text here:"):
    resume_text = st.session_state.get("resume_text", "")
    resume_text = st.text_area("Or paste your resume text here:")

# Analyze button
if st.button("Analyze Resume"):
    if resume_text.strip():
        with st.spinner("Analyzing your resume..."):
            result = analyze_resume(resume_text)
        st.subheader("📊 Resume Analysis")
        st.write(result)
    else:
        st.warning("Please upload or paste your resume first!")

# Chatbot section
st.subheader("💬 Career Chatbot")
user_question = st.text_input("Ask a career-related question:")

if st.button("Ask"):
    if resume_text.strip() and user_question.strip():
        with st.spinner("Thinking..."):
            answer = career_chatbot(user_question, resume_text)
        st.write("**Answer:**")
        st.write(answer)
    elif not resume_text.strip():
        st.warning("Upload or paste your resume first!")
    else:
        st.warning("Please enter a question.")


