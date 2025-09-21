from backend.utilities import clean_text
import pdfplumber
import docx2txt

def get_text(file=None, typed_text=None) -> str:
    """
    Get JD text from uploaded file or typed input
    """
    text = ""
    if typed_text:
        text = typed_text
    elif file:
        if file.name.endswith(".pdf"):
            with pdfplumber.open(file) as pdf:
                text = "\n".join([page.extract_text() or "" for page in pdf.pages])
        elif file.name.endswith(".docx"):
            text = docx2txt.process(file)
    return text

def parse_jd(file=None, typed_text=None) -> dict:
    raw_text = get_text(file, typed_text)
    normalized_text = clean_text(raw_text)
    return {
        "file_name": file.name if file else "typed_jd",
        "text_content": raw_text,
        "normalized_text": normalized_text
    }
