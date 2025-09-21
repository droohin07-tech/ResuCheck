import streamlit as st
import pandas as pd

from backend.resume_parse import ResumeParser
from backend.jd_parse import JDParser
from backend.jd_match import JDMatcher

# ------------------ APP CONFIG ------------------ #
st.set_page_config(
    page_title="ResuCheck",
    page_icon="📄",
    layout="wide"
)

st.title("📄 ResuCheck")
st.subheader("You make the call, we tell you who to call")
st.markdown("---")

# ------------------ INIT BACKEND ------------------ #
resume_parser = ResumeParser()
jd_parser = JDParser()
matcher = JDMatcher()

# ------------------ SIDEBAR ------------------ #
st.sidebar.header("Upload Options")

resume_files = st.sidebar.file_uploader(
    "Upload Resumes (PDF/DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

jd_file = st.sidebar.file_uploader(
    "Upload Job Description (PDF/DOCX)",
    type=["pdf", "docx"]
)

jd_text = st.sidebar.text_area("Or paste Job Description here:")

# ------------------ PROCESSING ------------------ #
if st.sidebar.button("Run Matching"):
    if not resume_files:
        st.error("Please upload at least one resume.")
    elif not (jd_file or jd_text.strip()):
        st.error("Please provide a job description (file or text).")
    else:
        with st.spinner("Parsing and matching..."):
            # Parse JD
            jd_data = jd_parser.parse(jd_text=jd_text, jd_file=jd_file)

            # Parse resumes
            resumes_data = []
            for r in resume_files:
                parsed = resume_parser.parse_file(r)
                if parsed:
                    resumes_data.append(parsed)

            # Match resumes vs JD
            results = matcher.batch_match(resumes_data, jd_data)

            # Convert to DataFrame
            df = pd.DataFrame(results)

        # ------------------ RESULTS ------------------ #
        st.success("✅ Matching completed!")

        st.markdown("### Results Dashboard")
        st.dataframe(df, use_container_width=True)

        # Download results
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv,
            file_name="resucheck_results.csv",
            mime="text/csv",
        )
