import pdfplumber
import docx2txt
from typing import Dict
from .utilities import clean_text, extract_education, match_skills

class JDParser:
    def parse(self, jd_text: str = None, jd_file=None, skill_list=None) -> Dict:

        if jd_file:
            file_name = getattr(jd_file, "name", "")
            extension = file_name.lower().split(".")[-1]
            if extension == "pdf":
                text = self.pdf(jd_file)
            elif extension == "docx":
                text = self.docx(jd_file)
            else:
                raise ValueError(f"Unsupported file type: {extension}")
        elif jd_text:
            text = jd_text
        else:
            text = ""

        normalized_text = clean_text(text)

        structured = {
            "skills": match_skills(text, skill_list) if skill_list else [],
            "education": extract_education(text)
        }

        return {
            "raw_text": text,
            "normalized_text": normalized_text,
            "structured": structured
        }

    # ---------------- Private helpers ---------------- #
    def pdf(self, file) -> str:
        text = ""
        try:
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error reading PDF: {e}")
        return text

    def docx(self, file) -> str:
        try:
            text = docx2txt.process(file)
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            text = ""
        return text