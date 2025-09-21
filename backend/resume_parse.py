import os
import re
from typing import Dict
import docx2txt
import pdfplumber
from backend.database import get_connection
from backend.utilities import clean_text, list_to_str

class ResumeParser:

    SUPPORTED_EXTENSIONS = [".pdf", ".docx"]

    def extract_text(self, file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return text
        elif ext == ".docx":
            return docx2txt.process(file_path)
        else:
            return ""

    def parse_resume(self, file_path: str) -> int:
        raw_text = self.extract_text(file_path)
        if not raw_text:
            return None

        normalized_text = clean_text(raw_text)

        # Extract fields
        name = raw_text.split("\n")[0].strip()
        email_match = re.search(r"[\w.-]+@[\w.-]+", raw_text)
        email = email_match.group(0) if email_match else ""
        skills = list_to_str([])  # Skills will come from JD, no default

        # Save to DB
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO resumes (file_name, raw_text, normalized_text, name, email, skills)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (os.path.basename(file_path), raw_text, normalized_text, name, email, skills))
        resume_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return resume_id
