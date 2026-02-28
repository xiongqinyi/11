from dataclasses import dataclass, field


@dataclass
class AnalyzeResponse:
    score: int
    breakdown: dict[str, float]
    missing_keywords: list[str] = field(default_factory=list)
    summary: str = ""


@dataclass
class FeedbackRequest:
    recruiter_id: str
    job_description: str
    resume_text: str
    decision: str


@dataclass
class ResumeOpenedRequest:
    platform: str
    recruiter_id: str
    job_description: str
    resume_text: str
    candidate_name: str | None = None
