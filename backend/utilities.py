import re
import unicodedata

def clean_text(text: str) -> str:
    """
    Normalize text: lowercase, remove extra spaces, NFKD unicode normalize.
    """
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_email(text: str) -> str:
    match = re.search(r'[\w.-]+@[\w.-]+', text)
    return match.group(0) if match else ""

def extract_name(text: str) -> str:
    # naive approach: first line
    lines = text.split("\n")
    for line in lines:
        if line.strip():
            return line.strip()
    return ""
