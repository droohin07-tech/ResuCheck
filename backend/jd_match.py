from typing import Dict, List
from sentence_transformers import SentenceTransformer, util

class JDMatcher:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the semantic similarity model
        """
        self.model = SentenceTransformer(model_name)

    def match(self, resume: Dict, jd: Dict) -> Dict:
        """
        Compare a parsed resume with a parsed job description
        Returns relevance score, missing elements, and verdict
        """
        resume_text = resume["normalized_text"]
        jd_text = jd["normalized_text"]

        # ----- Soft match (semantic similarity) -----
        embeddings = self.model.encode([resume_text, jd_text], convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()
        semantic_score = round(similarity * 100, 2)  # scale 0-100

        # ----- Hard match (skills + education) -----
        jd_skills = set(jd["structured"].get("skills", []))
        resume_text_lower = resume_text.lower()

        present_skills = [s for s in jd_skills if s.lower() in resume_text_lower]
        missing_skills = list(jd_skills - set(present_skills))

        jd_education = jd["structured"].get("education", [])
        missing_education = [e for e in jd_education if e.lower() not in resume_text_lower]

        missing_elements = missing_skills + missing_education

        # ----- Final score -----
        hard_score = (len(present_skills) / len(jd_skills) * 100) if jd_skills else 0
        final_score = round((0.7 * semantic_score) + (0.3 * hard_score), 2)

        # ----- Verdict -----
        if final_score >= 75:
            verdict = "Suitable"
        elif final_score >= 50:
            verdict = "Needs Review"
        else:
            verdict = "Not Suitable"

        return {
            "file_name": resume["file_name"],
            "semantic_score": semantic_score,
            "hard_score": hard_score,
            "final_score": final_score,
            "missing_elements": missing_elements,
            "verdict": verdict
        }

    def batch_match(self, resumes: List[Dict], jd: Dict) -> List[Dict]:
        """
        Run matching for multiple resumes against one JD
        """
        results = []
        for r in resumes:
            result = self.match(r, jd)
            results.append(result)
        return results