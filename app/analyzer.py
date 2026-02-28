import re
from collections import Counter

from app.preference import get_preference

STOP_WORDS = {
    "的",
    "和",
    "与",
    "及",
    "并",
    "for",
    "and",
    "the",
    "a",
    "an",
    "to",
    "in",
    "on",
    "with",
}

EXPERIENCE_PAT = re.compile(r"(\d{1,2})\s*年")



def tokenize(text: str) -> list[str]:
    chunks = re.split(r"[^\w\u4e00-\u9fff\+\#]+", text.lower())
    return [c for c in chunks if len(c) > 1 and c not in STOP_WORDS]



def keyword_coverage(job_text: str, resume_text: str) -> tuple[float, list[str]]:
    job_tokens = set(tokenize(job_text))
    resume_tokens = set(tokenize(resume_text))
    if not job_tokens:
        return 0.0, []
    hit = job_tokens & resume_tokens
    missing = sorted(job_tokens - resume_tokens)
    return len(hit) / len(job_tokens), missing[:15]



def skill_similarity(job_text: str, resume_text: str) -> float:
    job_counter = Counter(tokenize(job_text))
    resume_counter = Counter(tokenize(resume_text))
    vocab = set(job_counter) | set(resume_counter)
    if not vocab:
        return 0.0
    dot = sum(job_counter[w] * resume_counter[w] for w in vocab)
    jn = sum(v * v for v in job_counter.values()) ** 0.5
    rn = sum(v * v for v in resume_counter.values()) ** 0.5
    if jn == 0 or rn == 0:
        return 0.0
    return dot / (jn * rn)



def experience_match(job_text: str, resume_text: str) -> float:
    job_years = [int(x) for x in EXPERIENCE_PAT.findall(job_text)]
    resume_years = [int(x) for x in EXPERIENCE_PAT.findall(resume_text)]
    if not job_years:
        return 0.6
    if not resume_years:
        return 0.2
    req = max(job_years)
    own = max(resume_years)
    if own >= req:
        return 1.0
    return max(0.0, own / req)



def analyze_match(job_text: str, resume_text: str, recruiter_id: str = "default") -> dict:
    keyword_cov, missing = keyword_coverage(job_text, resume_text)
    skill_sim = skill_similarity(job_text, resume_text)
    exp_match = experience_match(job_text, resume_text)

    pref = get_preference(recruiter_id)
    raw = (
        pref.keyword_weight * keyword_cov
        + pref.skill_weight * skill_sim
        + pref.experience_weight * exp_match
    )
    score = int(round(raw * 100))

    preference_boost = raw - (
        0.4 * keyword_cov + 0.4 * skill_sim + 0.2 * exp_match
    )

    if score >= 80:
        summary = "候选人与岗位高度匹配，建议优先安排面试。"
    elif score >= 60:
        summary = "候选人与岗位中度匹配，建议结合业务重点复核。"
    else:
        summary = "候选人与岗位匹配度较低，建议谨慎推进。"

    return {
        "score": max(0, min(100, score)),
        "breakdown": {
            "keyword_coverage": round(keyword_cov, 4),
            "skill_similarity": round(skill_sim, 4),
            "experience_match": round(exp_match, 4),
            "preference_boost": round(preference_boost, 4),
        },
        "missing_keywords": missing,
        "summary": summary,
    }
