from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from app.analyzer import analyze_match
from app.preference import update_preference


@dataclass
class AnalyzeRequest:
    job_description: str
    resume_text: str
    recruiter_id: str = "default"


@dataclass
class FeedbackRequest:
    recruiter_id: str
    job_description: str
    resume_text: str
    decision: str



def analyze_resume(req: AnalyzeRequest) -> dict:
    return analyze_match(req.job_description, req.resume_text, req.recruiter_id)



def feedback(req: FeedbackRequest) -> dict:
    result = analyze_match(req.job_description, req.resume_text, req.recruiter_id)
    b = result["breakdown"]
    pref = update_preference(
        recruiter_id=req.recruiter_id,
        keyword_cov=b["keyword_coverage"],
        skill_sim=b["skill_similarity"],
        exp_match=b["experience_match"],
        decision=req.decision,
    )
    return {
        "message": "偏好模型已更新",
        "updated_weights": asdict(pref),
    }


if __name__ == "__main__":
    sample = AnalyzeRequest(
        recruiter_id="demo",
        job_description="Python 后端，3年经验，熟悉 Docker 与 SQL",
        resume_text="4年Python后端经验，FastAPI + Docker，熟悉MySQL",
    )
    print(json.dumps(analyze_resume(sample), ensure_ascii=False, indent=2))
