

def hard_match(resume, jd) -> float:
    resume_words = set(resume["normalized_text"].split())
    jd_words = set(jd["normalized_text"].split())
    if not jd_words:
        return 0.0
    return len(resume_words & jd_words) / len(jd_words)


def soft_match(resume, jd) -> float:
    # Simple approximation for demo
    resume_len = len(resume["normalized_text"].split())
    jd_len = len(jd["normalized_text"].split())
    if resume_len + jd_len == 0:
        return 0
    return min(resume_len, jd_len) / max(resume_len, jd_len)


def run_match(resume, jd) -> dict:
    h_score = hard_match(resume, jd)
    s_score = soft_match(resume, jd)

    # Total score out of 100
    total_score = round((h_score + s_score) / 2 * 100, 2)

    verdict = "Strong Fit" if total_score > 70 else "Weak Fit"

    return {
        "resume": resume["file_name"],
        "jd": jd["file_name"],
        "hard_score": round(h_score * 100, 2),
        "soft_score": round(s_score * 100, 2),
        "total_score": total_score,
        "verdict": verdict
    }
