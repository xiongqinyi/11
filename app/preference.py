from __future__ import annotations

from dataclasses import dataclass

from app.storage import load_preferences, save_preferences


@dataclass
class RecruiterPreference:
    keyword_weight: float = 0.4
    skill_weight: float = 0.4
    experience_weight: float = 0.2

    def normalize(self) -> None:
        total = self.keyword_weight + self.skill_weight + self.experience_weight
        if total <= 0:
            self.keyword_weight, self.skill_weight, self.experience_weight = 0.4, 0.4, 0.2
            return
        self.keyword_weight /= total
        self.skill_weight /= total
        self.experience_weight /= total


def get_preference(recruiter_id: str) -> RecruiterPreference:
    prefs = load_preferences().get(recruiter_id)
    if not prefs:
        return RecruiterPreference()
    return RecruiterPreference(**prefs)


def update_preference(recruiter_id: str, keyword_cov: float, skill_sim: float, exp_match: float, decision: str) -> RecruiterPreference:
    pref = get_preference(recruiter_id)
    lr = 0.08
    signal = 1 if decision == "accept" else -1

    pref.keyword_weight += lr * signal * (keyword_cov - 0.5)
    pref.skill_weight += lr * signal * (skill_sim - 0.5)
    pref.experience_weight += lr * signal * (exp_match - 0.5)

    pref.keyword_weight = max(0.05, min(0.85, pref.keyword_weight))
    pref.skill_weight = max(0.05, min(0.85, pref.skill_weight))
    pref.experience_weight = max(0.05, min(0.85, pref.experience_weight))
    pref.normalize()

    all_prefs = load_preferences()
    all_prefs[recruiter_id] = {
        "keyword_weight": pref.keyword_weight,
        "skill_weight": pref.skill_weight,
        "experience_weight": pref.experience_weight,
    }
    save_preferences(all_prefs)
    return pref
