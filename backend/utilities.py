import re
import unicodedata
from typing import List

# ---------------- Text Cleaning ---------------- #
def clean_text(text: str) -> str:
    if not text:
        return ""
    # Normalize unicode characters
    text = unicodedata.normalize("NFKD", text)
    # Remove non-printable characters
    text = "".join(c for c in text if c.isprintable())
    # Lowercase
    text = text.lower()
    # Remove extra spaces and newlines
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ---------------- Email Extraction ---------------- #
def extract_email(text: str) -> str:
    """
    Extract the first email found in the text.
    Returns empty string if none found.
    """
    match = re.search(r'[\w.-]+@[\w.-]+', text)
    return match.group(0) if match else ""

# ---------------- Skill Matching ---------------- #
def match_skills(text: str, skill_list: List[str]) -> List[str]:
    """
    Given text and a list of skills, return the skills found in the text.
    """
    text_lower = text.lower()
    matched = [skill for skill in skill_list if skill.lower() in text_lower]
    return matched

# ---------------- Name Extraction ---------------- #
def extract_name(text: str) -> str:
    """
    Simple heuristic: take the first non-empty line as the name.
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return lines[0] if lines else ""

# ---------------- Education Extraction (Optional) ---------------- #
def extract_education(text: str) -> List[str]:
    """
    Extract common education keywords from text.
    """
    education_keywords = [
        "bachelor", "b.e", "b.tech", "bsc", "mba",
        "master", "m.e", "m.tech", "msc", "phd"
    ]
    return match_skills(text, education_keywords)
