import pdfplumber
import docx2txt
from io import BytesIO

def extract_text(uploaded_file) -> str:
    """
    Extract text from an uploaded PDF or DOCX file (Streamlit uploaded file).
    Returns plain text.
    """
    filename = getattr(uploaded_file, "name", "")
    extension = filename.split(".")[-1].lower()

    if extension == "pdf":
        text = ""
        with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text.strip()

    elif extension == "docx":
        # docx2txt accepts file-like object
        text = docx2txt.process(uploaded_file)
        return text.strip()

    else:
        return ""
