import pdfplumber
import docx2txt
from typing import Dict
from .utilities import clean_text, extract_email, extract_name, extract_education

class ResumeParser:
    SUPPORTED_EXTENSIONS = [".pdf", ".docx"]

    def parse_file(self, file) -> Dict:
        file_name = getattr(file, "name", "uploaded_file")
        extension = file_name.lower().split(".")[-1]

        # Extract text
        if extension == "pdf":
            text = self.pdf(file)
        elif extension == "docx":
            text = self.docx(file)
        else:
            raise ValueError(f"Unsupported file type: {extension}")

        if not text:
            return None

        normalized_text = clean_text(text)
        structured_fields = {
            "name": extract_name(text),
            "email": extract_email(text),
            "education": extract_education(text)
        }

        return {
            "file_name": file_name,
            "raw_text": text,
            "normalized_text": normalized_text,
            "structured": structured_fields
        }

    # ---------------- Private helpers ---------------- #
    def pdf(self, file) -> str:
        text = ""
        try:
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
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
