"""Adversarial and Reliability Unit Tests for Nayanee.
"""

from fastapi.testclient import TestClient
from api.main import app
from pocs.poc01_adaptive_engine.models import LanguageCode
from pocs.poc05_field_validation.adversarial_runner import AdversarialHarness

client = TestClient(app)


def test_mid_session_language_switching():
    res = AdversarialHarness.run_mid_session_language_switch(
        LanguageCode.ENGLISH, LanguageCode.KANNADA
    )
    assert res["initial_language"] == "en"
    assert res["final_language"] == "kn"
    assert res["turn_count"] == 3
    assert res["turns_language_switch_supported"] is True


def test_api_rejects_injected_or_invalid_options():
    start_resp = client.post("/api/v1/session/start", json={"language": "en"})
    session_id = start_resp.json()["session_id"]

    malicious_inputs = [
        "'; DROP TABLE sessions; --",
        "<script>alert(1)</script>",
        "random_unsupported_string_option",
        "",
    ]

    for bad in malicious_inputs:
        resp = client.post(
            f"/api/v1/session/{session_id}/turn",
            json={"question_id": "q_chief_complaint", "selected_option": bad},
        )
        assert resp.status_code == 400
        assert "is not valid for question" in resp.json()["detail"]


def test_acoustic_noise_triggering_degradation():
    clean_audio = b"Sample clear audio"
    noisy_audio = AdversarialHarness.simulate_acoustic_noise(clean_audio, noise_snr_db=5.0)
    assert noisy_audio == b"NOISY_CORRUPTED_AUDIO_PAYLOAD"
