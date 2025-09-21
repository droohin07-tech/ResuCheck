import streamlit as st
from backend import resume_parse, jd_parse, jd_match

st.set_page_config(page_title="ResuCheck", page_icon="📄", layout="wide")

st.title("ResuCheck")
st.subheader("You make the call, we tell you who to call")

# Initialize in-memory storage
if "resumes" not in st.session_state:
    st.session_state.resumes = []
if "jds" not in st.session_state:
    st.session_state.jds = []
if "matches" not in st.session_state:
    st.session_state.matches = []

# Upload resumes
uploaded_resumes = st.file_uploader(
    "Upload Resumes (PDF/DOCX)", type=["pdf", "docx"], accept_multiple_files=True
)
for file in uploaded_resumes:
    parsed = resume_parse.parse_resume(file)
    if parsed not in st.session_state.resumes:
        st.session_state.resumes.append(parsed)

# Upload or type JD
st.markdown("### Job Description")
jd_text = st.text_area("Type Job Description here")
uploaded_jd = st.file_uploader("Or Upload JD (PDF/DOCX)", type=["pdf", "docx"], key="jd_upload")
parsed_jd = None
if uploaded_jd:
    parsed_jd = jd_parse.parse_jd(file=uploaded_jd)
elif jd_text:
    parsed_jd = jd_parse.parse_jd(typed_text=jd_text)

if parsed_jd and parsed_jd not in st.session_state.jds:
    st.session_state.jds.append(parsed_jd)

# Run matches
if st.button("Run Matching"):
    st.session_state.matches = []
    for resume in st.session_state.resumes:
        for jd in st.session_state.jds:
            match = jd_match.run_match(resume, jd)
            st.session_state.matches.append(match)

# Display results
if st.session_state.matches:
    st.markdown("### Match Results")
    for m in st.session_state.matches:
        st.write(f"**Resume:** {m['resume']} | **JD:** {m['jd']}")
        st.write(f"Hard Score: {m['hard_score']} | Soft Score: {m['soft_score']} | Verdict: {m['verdict']}")
        st.write("---")
