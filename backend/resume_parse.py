import os
from typing import List, Dict
from backend.utilities import extract_text  # Your existing extraction function

class MyResumeParser:
    SUPPORTED_EXTENSIONS = [".pdf", ".docx"]

    def __init__(self):
        pass

    def parse_file(self, file) -> Dict:
        """
        Accepts uploaded file from Streamlit
        """
        raw_text = extract_text(file)
        normalized_text = " ".join(raw_text.lower().split())
        return {
            "file_name": getattr(file, "name", "typed_resume"),
            "raw_text": raw_text,
            "normalized_text": normalized_text
        }

    def parse_multiple(self, files_list: List) -> List[Dict]:
        parsed = []
        for f in files_list:
            parsed.append(self.parse_file(f))
        return parsed
