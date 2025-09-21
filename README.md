# ResuCheck

**Slogan:** *You make the call, we tell you who to call*

---

## Overview

ResuCheck is a **web-based resume screening tool** designed for placement teams and students.  
It analyzes uploaded resumes and job descriptions (JD) to calculate **hard and soft match scores** and provides a **total relevance score** along with a **fit verdict**.

- **Hard match:** Checks for required keywords and skills.  
- **Soft match:** Semantic/contextual fit using text analysis.  
- **Total score:** Weighted average of hard and soft match (out of 100).  
- **Verdict:** Strong Fit or Weak Fit.

This project uses **Python, Streamlit, and lightweight parsing modules**. It runs entirely in the browser with no local database required.

---

## Features

- Upload **multiple resumes** (PDF or DOCX).  
- Input JD **via typing or file upload**.  
- Calculates **hard, soft, and total scores**.  
- Color-coded verdicts and **progress bars** for easy visualization.  
- Clean, minimal, professional UI.  
- Fully deployable on **Streamlit Cloud**.

---

## Tech Stack

- Python 3.x  
- Streamlit  
- pdfplumber (PDF text extraction)  
- docx2txt (DOCX text extraction)  
- Git & GitHub (version control)

---

## Project Structure

ResuCheck/
│
├── app.py # Main Streamlit app
├── backend/
│ ├── init.py
│ ├── resume_parse.py # Resume parsing
│ ├── jd_parse.py # Job description parsing
│ ├── jd_match.py # Hard + soft match logic
│ └── utilities.py # Text extraction & helpers
├── requirements.txt # Python dependencies
├── README.md
