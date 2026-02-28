from app.main import AnalyzeRequest, FeedbackRequest, analyze_resume, feedback


def test_analyze_with_text():
    result = analyze_resume(
        AnalyzeRequest(
            job_description='Python开发，3年经验，熟悉Docker',
            resume_text='4年Python后端开发，熟悉Docker和FastAPI',
            recruiter_id='demo',
        )
    )
    assert 'score' in result
    assert 0 <= result['score'] <= 100


def test_feedback():
    result = feedback(
        FeedbackRequest(
            recruiter_id='demo',
            job_description='Python开发，3年经验，熟悉Docker',
            resume_text='4年Python后端开发，熟悉Docker和FastAPI',
            decision='accept',
        )
    )
    assert 'updated_weights' in result
