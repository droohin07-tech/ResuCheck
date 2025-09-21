from typing import Dict
from backend.utilities import extract_text

class JDParser:
    def parse_file(self, file) -> Dict:
        """
        Parse JD from uploaded PDF/DOCX file
        """
        raw_text = extract_text(file)
        normalized_text = " ".join(raw_text.lower().split())
        return {
            "file_name": getattr(file, "name", "JD_file"),
            "raw_text": raw_text,
            "normalized_text": normalized_text
        }

    def parse_text(self, text: str) -> Dict:
        """
        Parse JD from typed text
        """
        normalized_text = " ".join(text.lower().split())
        return {
            "file_name": "typed_JD",
            "raw_text": text,
            "normalized_text": normalized_text
        }
