from backend.database import get_connection
from backend.utilities import clean_text, str_to_list, list_to_str

class JDMatcher:

    def compute_hard_score(self, resume_text: str, jd_text: str) -> float:
        """
        Simple keyword match percentage
        """
        resume_words = set(clean_text(resume_text).split())
        jd_words = set(clean_text(jd_text).split())
        matches = resume_words.intersection(jd_words)
        return len(matches) / len(jd_words) if jd_words else 0.0

    def compute_soft_score(self, resume_text: str, jd_text: str) -> float:
        """
        Dummy semantic match (placeholder for embeddings/LLM)
        """
        # For now, just a random placeholder
        import random
        return round(random.uniform(0.6, 0.95), 2)

    def match_resume_to_jd(self, resume_id: int, jd_id: int):
        conn = get_connection()
        cursor = conn.cursor()

        # Fetch resume and JD
        cursor.execute("SELECT normalized_text FROM resumes WHERE id = ?", (resume_id,))
        resume_text = cursor.fetchone()[0]

        cursor.execute("SELECT normalized_text FROM job_descriptions WHERE id = ?", (jd_id,))
        jd_text = cursor.fetchone()[0]

        hard_score = self.compute_hard_score(resume_text, jd_text)
        soft_score = self.compute_soft_score(resume_text, jd_text)
        verdict = "Suitable" if hard_score > 0.5 and soft_score > 0.7 else "Review"

        # Store match
        cursor.execute("""
            INSERT INTO matches (resume_id, jd_id, hard_score, soft_score, verdict)
            VALUES (?, ?, ?, ?, ?)
        """, (resume_id, jd_id, hard_score, soft_score, verdict))
        conn.commit()
        conn.close()

        return {"hard_score": hard_score, "soft_score": soft_score, "verdict": verdict}
