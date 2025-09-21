import re
import unicodedata

def clean_text(text: str) -> str:
    """
    Normalize text for semantic matching:
    - lowercase
    - remove accents
    - remove extra spaces
    """
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r'\s+', ' ', text)
    return text.lower().strip()

def list_to_str(lst: list) -> str:
    return ", ".join(lst)

def str_to_list(s: str) -> list:
    return [x.strip() for x in s.split(",") if x.strip()]
