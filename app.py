import streamlit as st
from backend.resume_parse import MyResumeParser
from backend.jd_parse import JDParser
from backend.jd_match import run_match

# ---------------- Page Config ----------------
st.set_page_config(page_title="ResuCheck", page_icon="📄", layout="wide")

# ---------------- Custom CSS ----------------
st.markdown(
    """
    <style>
    /* Light background */
    .stApp {
        background-color: #f5f7fa;
    }

    /* Center align title and slogan */
    .title-container {
        text-align: center;
        padding: 40px;
    }

    .title-container h1 {
        color: #0d3b66;
        font-size: 60px;
        margin-bottom: 10px;
    }

    .title-container h4 {
        color: #3f88c5;
        font-size: 24px;
    }

    /* Style buttons */
    div.stButton > button:first-child {
        background-color: #3f88c5;
        color: white;
        height: 50px;
        width: 100%;
        border-radius: 8px;
        font-size: 18px;
    }

    div.stButton > button:hover {
        background-color: #0d3b66;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- Header ----------------
st.markdown(
    """
    <div class="title-container">
        <h1>ResuCheck</h1>
        <h4>You make the call, we tell you who to call</h4>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- Resume Upload ----------------
st.markdown("### Upload Resumes (PDF/DOCX)")
uploaded_resumes = st.file_uploader("Select one or more resumes", type=["pdf", "docx"], accept_multiple_files=True)

# ---------------- Job Description ----------------
st.markdown("### Job Description")
jd_text = st.text_area("Type Job Description here", height=150)
uploaded_jd = st.file_uploader("Or Upload JD (PDF/DOCX)", type=["pdf", "docx"], key="jd_upload")

# ---------------- Initialize parsers ----------------
resume_parser = MyResumeParser()
jd_parser = JDParser()

# ---------------- Run Matching ----------------
if st.button("Run Matching"):

    if not uploaded_resumes:
        st.warning("Please upload at least one resume!")
    elif not jd_text and not uploaded_jd:
        st.warning("Please type or upload a Job Description!")
    else:
        # Parse resumes
        resumes = resume_parser.parse_multiple(files_list=uploaded_resumes)

        # Parse JD
        if uploaded_jd:
            jd_data = jd_parser.parse_file(uploaded_jd)
        else:
            jd_data = jd_parser.parse_text(jd_text)

        # Run matching for each resume
        matches = []
        for r in resumes:
            match_result = run_match(r, jd_data)
            matches.append(match_result)

        # Display results
        st.markdown("### Match Results")
        for m in matches:
            st.subheader(f"Resume: {m['resume']}")

            st.markdown(f"**Hard Score:** {m['hard_score']}%")
            st.progress(int(m['hard_score']))

            st.markdown(f"**Soft Score:** {m['soft_score']}%")
            st.progress(int(m['soft_score']))

            st.markdown(f"**Total Score:** {m['total_score']}%")
            st.progress(int(m['total_score']))

            if m['verdict'] == "Strong Fit":
                st.success(f"Verdict: {m['verdict']}")
            else:
                st.warning(f"Verdict: {m['verdict']}")

            st.markdown("---")
