import streamlit as st
import requests

st.set_page_config(page_title="AI Resume Screening", layout="wide")

st.title("AI Resume Screening & Ranking System")

st.write("Upload multiple resumes and a job description to rank candidates.")

# Upload resumes
resumes = st.file_uploader(
    "Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

# Job description input
job_desc = st.text_area(
    "Paste Job Description",
    height=150
)

# Button
if st.button("Rank Candidates"):
    if not resumes or not job_desc:
        st.warning("Please upload resumes and enter job description")
    else:
        with st.spinner("Ranking resumes..."):
            files = [("resumes", r) for r in resumes]

            response = requests.post(
                "http://127.0.0.1:8000/rank",
                files=files,
                data={"job_desc": job_desc}
            )

        if response.status_code == 200:
            results = response.json()["ranked_candidates"]

            st.success("Ranking completed ✅")

            for r in results:
                st.markdown(f"""
                ### 🏅 Rank {r['rank']} – {r['resume']}
                - **Final Score:** {r['final_score']}
                - **BERT Score:** {r['bert_score']}
                - **Skill Match:** {r['skill_match']}
                - **Extracted Skills:** {", ".join(r['skills'])}
                """)
        else:
            st.error("Error connecting to backend")
