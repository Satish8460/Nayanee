"""Automated End-to-End API Tests for Nayanee Service Layer.
"""

import base64
import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.session_store import store
from pocs.poc01_adaptive_engine.models import ReviewStatus

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_session_store():
    store.clear()
    yield
    store.clear()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "kn" in data["supported_languages"]


def test_serve_frontend():
    response = client.get("/")
    assert response.status_code == 200
    assert "Nayanee" in response.text
    assert "Adaptive Vision Intelligence" in response.text


def test_stream_speech_audio_endpoint():
    """Confirms /api/v1/session/speak returns audio MP3 data."""
    resp = client.get("/api/v1/session/speak?text=ನಮಸ್ಕಾರ&lang=kn")
    assert resp.status_code == 200
    assert "audio/mpeg" in resp.headers["content-type"]
    assert len(resp.content) > 1000


def test_complete_customer_session_kannada():
    start_resp = client.post("/api/v1/session/start", json={"language": "kn"})
    assert start_resp.status_code == 201
    session_data = start_resp.json()
    session_id = session_data["session_id"]
    assert session_data["language"] == "kn"
    assert session_data["turn_index"] == 1
    assert "ಕಣ್ಣಿನಲ್ಲಿ" in session_data["current_question"]["text"]
    assert "localized_options" in session_data["current_question"]
    loc_opts = session_data["current_question"]["localized_options"]
    assert len(loc_opts) > 0
    assert any("ದೂರದ್ದು" in o["label"] for o in loc_opts)

    turn1_resp = client.post(
        f"/api/v1/session/{session_id}/turn",
        json={"question_id": "q_chief_complaint", "selected_option": "near_reading_blur"},
    )
    assert turn1_resp.status_code == 200
    t1_data = turn1_resp.json()
    assert t1_data["current_question"]["id"] == "q_acute_symptoms"

    turn2_resp = client.post(
        f"/api/v1/session/{session_id}/turn",
        json={"question_id": "q_acute_symptoms", "selected_option": "no_acute_symptoms"},
    )
    assert turn2_resp.status_code == 200

    curr_data = turn2_resp.json()
    turns = 0
    while curr_data["status"] == "in_progress" and turns < 10:
        turns += 1
        q = curr_data["current_question"]
        choice = q["options"][0]
        if q["id"] == "q_near_mobile_reading":
            choice = "significant_blur_holds_far"
        elif q["id"] == "q_current_eyewear":
            choice = "never_worn"

        turn_resp = client.post(
            f"/api/v1/session/{session_id}/turn",
            json={"question_id": q["id"], "selected_option": choice},
        )
        assert turn_resp.status_code == 200
        curr_data = turn_resp.json()

    assert curr_data["status"] == "completed"
    assert curr_data["profile_id"] is not None
    profile_id = curr_data["profile_id"]

    prof_resp = client.get(f"/api/v1/profiles/{profile_id}")
    assert prof_resp.status_code == 200
    res_data = prof_resp.json()
    prof = res_data["profile"]
    assert prof["customer_language"] == "kn"
    assert prof["near_vision_status"]["has_presbyopic_indicators"] is True
    assert prof["eyewear_history"]["current_modality"] == "never_worn"
    assert prof["review_status"] == "pending_optometrist_review"
    assert "lifestyle_guidance" in res_data
    assert len(res_data["lifestyle_guidance"]) >= 1


def test_api_audio_turn_processing():
    start_resp = client.post("/api/v1/session/start", json={"language": "kn"})
    session_id = start_resp.json()["session_id"]

    mock_audio = base64.b64encode(b"near reading blur mobile").decode("utf-8")
    turn_resp = client.post(
        f"/api/v1/session/{session_id}/audio-turn",
        json={
            "question_id": "q_chief_complaint",
            "audio_base64": mock_audio,
            "expected_option": "near_reading_blur",
        },
    )
    assert turn_resp.status_code == 200
    data = turn_resp.json()
    assert data["turn_index"] == 2
    assert data["current_question"]["id"] == "q_acute_symptoms"


def test_api_acute_red_flag_escalation():
    start_resp = client.post("/api/v1/session/start", json={"language": "en"})
    session_id = start_resp.json()["session_id"]

    client.post(
        f"/api/v1/session/{session_id}/turn",
        json={"question_id": "q_chief_complaint", "selected_option": "sudden_vision_change"},
    )

    rf_resp = client.post(
        f"/api/v1/session/{session_id}/turn",
        json={"question_id": "q_acute_symptoms", "selected_option": "sudden_vision_drop"},
    )
    assert rf_resp.status_code == 200
    data = rf_resp.json()
    assert data["status"] == "urgent_escalation"
    assert data["review_status"] == ReviewStatus.URGENT_MEDICAL_ESCALATION.value
    assert data["red_flags_count"] >= 1
    assert data["current_question"] is None


def test_optometrist_review_workflow():
    start_resp = client.post("/api/v1/session/start", json={"language": "hi"})
    session_id = start_resp.json()["session_id"]

    client.post(
        f"/api/v1/session/{session_id}/turn",
        json={"question_id": "q_chief_complaint", "selected_option": "sudden_vision_change"},
    )
    end_resp = client.post(
        f"/api/v1/session/{session_id}/turn",
        json={"question_id": "q_acute_symptoms", "selected_option": "flashes_or_floaters"},
    )
    profile_id = end_resp.json()["profile_id"]

    list_resp = client.get("/api/v1/profiles")
    assert list_resp.status_code == 200
    profiles = list_resp.json()
    assert len(profiles) == 1
    assert profiles[0]["profile_id"] == profile_id
    assert profiles[0]["has_red_flags"] is True

    review_payload = {
        "reviewer_name": "Dr. Ananya Sharma",
        "decision": "urgent_medical_escalation",
        "clinical_notes": "Urgent fundus and retinal evaluation recommended due to reported flashes.",
        "recommended_action": "Refer to tertiary ophthalmology center immediately",
    }
    rev_resp = client.post(f"/api/v1/profiles/{profile_id}/review", json=review_payload)
    assert rev_resp.status_code == 200
    updated_prof = rev_resp.json()
    assert updated_prof["review_status"] == "urgent_medical_escalation"


def test_session_with_patient_demographics():
    start_resp = client.post(
        "/api/v1/session/start",
        json={
            "language": "kn",
            "patient_name": "Savitri Amma",
            "patient_age": 58,
            "patient_gender": "Female",
            "patient_phone": "9876543210"
        }
    )
    assert start_resp.status_code == 201
    s_data = start_resp.json()
    session_id = s_data["session_id"]

    # Trigger red flag to complete session immediately
    client.post(
        f"/api/v1/session/{session_id}/turn",
        json={"question_id": "q_chief_complaint", "selected_option": "sudden_vision_change"}
    )
    end_resp = client.post(
        f"/api/v1/session/{session_id}/turn",
        json={"question_id": "q_acute_symptoms", "selected_option": "sudden_vision_drop"}
    )
    assert end_resp.status_code == 200
    profile_id = end_resp.json()["profile_id"]

    prof_resp = client.get(f"/api/v1/profiles/{profile_id}")
    assert prof_resp.status_code == 200
    p = prof_resp.json()["profile"]
    assert p["patient_name"] == "Savitri Amma"
    assert p["patient_age"] == 58
    assert p["patient_gender"] == "Female"

    slip_resp = client.get(f"/api/v1/export/profile/{profile_id}/printable-slip")
    assert slip_resp.status_code == 200
    assert "Savitri Amma" in slip_resp.text
    assert "58" in slip_resp.text
