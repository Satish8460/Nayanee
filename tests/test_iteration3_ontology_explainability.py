"""Tests for Iteration 3 & Iteration 4.
"""

from fastapi.testclient import TestClient
from api.main import app
from pocs.poc01_adaptive_engine.models import (
    FunctionalVisionProfile,
    LanguageCode,
    ReviewStatus,
    RedFlagAlert,
    SeverityLevel,
)
from pocs.poc01_adaptive_engine.questions_bank import get_question_by_id
from pocs.poc01_adaptive_engine.explainability import ExplainabilityReport
from api.session_store import store

client = TestClient(app)


def test_systemic_health_question_in_ontology():
    q = get_question_by_id("q_systemic_health")
    assert q.id == "q_systemic_health"
    assert "diabetes_only" in q.options
    assert "kn" in q.text_translations
    assert "ಮಧುಮೇಹ" in q.text_translations["kn"]


def test_explainability_clinical_handover_summary():
    profile = FunctionalVisionProfile(
        session_id="test_sess_exp",
        customer_language=LanguageCode.KANNADA,
        total_questions_asked=6,
        distance_vision_status={"clarity_rating": "often", "night_glare_difficulty": "severe_glare_avoids_driving"},
        near_vision_status={"mobile_reading_status": "significant_blur_holds_far", "has_presbyopic_indicators": True},
        lifestyle_occupational_context={"daily_screen_hours": "five_to_eight", "digital_visual_fatigue_risk": True},
        eyewear_history={"current_modality": "distance_only", "glasses_age": "more_than_two_years"},
        red_flags=[
            RedFlagAlert(
                symptom="flashes_or_floaters",
                trigger_question_id="q_acute_symptoms",
                trigger_answer="flashes_or_floaters",
                urgency=SeverityLevel.CRITICAL,
                clinical_note="Urgent retinal specialist consultation advised.",
            )
        ],
        review_status=ReviewStatus.URGENT_MEDICAL_ESCALATION,
    )

    summary_text = ExplainabilityReport.generate_clinical_handover_summary(profile)
    assert "NAYANEE FUNCTIONAL VISION INTAKE REPORT" in summary_text
    assert "Distance Vision Clarity: often" in summary_text
    assert "Presbyopic Indicator: YES" in summary_text
    assert "Digital Visual Fatigue Risk: ELEVATED" in summary_text
    assert "CRITICAL RED-FLAG SAFETY ESCALATIONS" in summary_text
    assert "flashes_or_floaters" in summary_text


def test_clinical_export_api_endpoints():
    profile = FunctionalVisionProfile(
        profile_id="prof_export_test",
        session_id="sess_export_test",
        customer_language=LanguageCode.HINDI,
        total_questions_asked=7,
        distance_vision_status={"clarity_rating": "sometimes"},
        near_vision_status={"mobile_reading_status": "clear_at_normal_distance", "has_presbyopic_indicators": False},
        lifestyle_occupational_context={"daily_screen_hours": "two_to_four", "digital_visual_fatigue_risk": False},
        eyewear_history={"current_modality": "never_worn"},
        review_status=ReviewStatus.PENDING_OPTOMETRIST_REVIEW,
    )
    store.save_profile(profile)

    resp = client.get("/api/v1/export/profile/prof_export_test/summary-text")
    assert resp.status_code == 200
    assert "text/plain" in resp.headers["content-type"]
    assert "NAYANEE FUNCTIONAL VISION INTAKE REPORT" in resp.text
    assert "Language: HI" in resp.text
