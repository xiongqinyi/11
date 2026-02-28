from app.analyzer import analyze_match


def test_analyze_match_score_range():
    job = "Python FastAPI 微服务开发，3年经验，熟悉SQL和Docker"
    resume = "5年Python开发经验，使用FastAPI和Docker，熟悉MySQL"
    result = analyze_match(job, resume)
    assert 0 <= result["score"] <= 100
    assert "keyword_coverage" in result["breakdown"]


def test_analyze_match_missing_keywords():
    job = "需要掌握Kubernetes、ETL、Python"
    resume = "熟悉Python和数据分析"
    result = analyze_match(job, resume)
    assert any(k in result["missing_keywords"] for k in ["kubernetes", "etl"])
