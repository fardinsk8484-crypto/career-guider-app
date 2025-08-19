import os
import streamlit as st
from openai import OpenAI

# Load API key securely (must be set in Streamlit Cloud -> Settings -> Secrets)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Career Guider App", layout="wide")

st.title("💼 Career Guider App")

st.write("Upload your resume and job description to get AI-powered career guidance.")

# File uploader for resume
uploaded_resume = st.file_uploader("Upload your Resume (PDF/DOCX)", type=["pdf", "docx"], key="resume_uploader")

# Resume text input (alternative to upload)
resume_text = st.text_area("Or paste your resume text here:", key="resume_input")

# File uploader for job description
uploaded_job = st.file_uploader("Upload Job Description (PDF/DOCX)", type=["pdf", "docx"], key="job_uploader")

# Job description text input
job_description = st.text_area("Or paste the job description here:", key="job_input")

# Submit button
if st.button("🔍 Analyze Match", key="analyze_button"):
    if not resume_text and not uploaded_resume:
        st.error("⚠️ Please provide a resume (upload or paste).")
    elif not job_description and not uploaded_job:
        st.error("⚠️ Please provide a job description (upload or paste).")
    else:
        with st.spinner("Analyzing your resume... ⏳"):
            # Combine input sources
            final_resume = resume_text if resume_text else "Uploaded resume file"
            final_job = job_description if job_description else "Uploaded job file"

            prompt = f"""
            You are an expert career consultant.
            Compare the following resume and job description.
            Provide:
            1. Match percentage
            2. Key missing skills
            3. Suggestions to improve the resume for this role

            Resume:
            {final_resume}

            Job Description:
            {final_job}
            """

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful career advisor."},
                        {"role": "user", "content": prompt}
                    ]
                )

                result = response.choices[0].message.content
                st.success("✅ Analysis Complete!")
                st.write(result)

            except Exception as e:
                st.error(f"❌ Error: {e}")
