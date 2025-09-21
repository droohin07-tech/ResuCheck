import os
from backend.database import get_connection
from backend.utilities import clean_text
import docx2txt
import pdfplumber

class JDParser:

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

    def parse_jd(self, text: str = None, file_path: str = None) -> int:
        if file_path:
            raw_text = self.extract_text(file_path)
        elif text:
            raw_text = text
        else:
            return None

        normalized_text = clean_text(raw_text)

        # Save to DB
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO job_descriptions (file_name, text_content, normalized_text)
            VALUES (?, ?, ?)
        """, (os.path.basename(file_path) if file_path else "typed_jd", raw_text, normalized_text))
        jd_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return jd_id
