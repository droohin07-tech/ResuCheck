from backend.utilities import clean_text, extract_email, extract_name
import pdfplumber
import docx2txt

def get_text(file) -> str:
    """
    Extract text from PDF or DOCX
    """
    text = ""
    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    elif file.name.endswith(".docx"):
        text = docx2txt.process(file)
    return text

def parse_resume(file) -> dict:
    raw_text = get_text(file)
    normalized_text = clean_text(raw_text)
    return {
        "file_name": file.name,
        "raw_text": raw_text,
        "normalized_text": normalized_text,
        "name": extract_name(raw_text),
        "email": extract_email(raw_text)
    }
