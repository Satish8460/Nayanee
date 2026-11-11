"""Tests for Optical Lifestyle Advisor and Demonstration Seeding.
"""

from fastapi.testclient import TestClient
from api.main import app
from pocs.poc01_adaptive_engine.models import (
    FunctionalVisionProfile,
    LanguageCode,
    ReviewStatus,
)
from pocs.poc01_adaptive_engine.lifestyle_advisor import OpticalLifestyleAdvisor

client = TestClient(app)


def test_optical_lifestyle_advisor_screen_and_glare():
    profile = FunctionalVisionProfile(
        session_id="test_sess_lifestyle",
        customer_language=LanguageCode.HINDI,
        total_questions_asked=8,
        distance_vision_status={"clarity_rating": "often", "night_glare_difficulty": "severe_glare_avoids_driving"},
        near_vision_status={"mobile_reading_status": "significant_blur_holds_far", "has_presbyopic_indicators": True},
        lifestyle_occupational_context={"daily_screen_hours": "more_than_eight", "outdoor_sun_exposure": "majority_outdoors_heavy_sun"},
        eyewear_history={"current_modality": "distance_only", "glasses_age": "more_than_two_years"},
        review_status=ReviewStatus.PENDING_OPTOMETRIST_REVIEW,
    )

    guidance = OpticalLifestyleAdvisor.generate_recommendations(profile)
    categories = [g["category"] for g in guidance]

    assert "Digital Ergonomics" in categories
    assert "Driving Safety" in categories
    assert "Near Vision Support" in categories
    assert "Environmental Protection" in categories
    assert "Eyewear Wear & Tear" in categories


def test_seed_demo_cases_api():
    resp = client.post("/api/v1/profiles/seed-demo")
    assert resp.status_code == 200
    profiles = resp.json()
    assert len(profiles) >= 4

    pids = [p["profile_id"] for p in profiles]
    assert "demo-kn-parvathamma" in pids
    assert "demo-hi-rajesh-screen" in pids
    assert "demo-ta-muthuvel-contra" in pids
    assert "demo-te-srinivas-redflag" in pids
