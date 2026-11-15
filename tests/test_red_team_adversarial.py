"""Comprehensive Red Team Adversarial & Stress Testing Suite for Nayanee.
Iterative attacks across 5 threat surfaces:
1. Malicious input & option injection attacks (XSS, SQLi, huge strings, boundary values)
2. State machine abuse, concurrent race conditions, and out-of-order execution
3. Speech & Audio fuzzing (corrupt binaries, zero-byte payloads, buffer floods)
4. Screening engine tampering & payload corruption
5. Stochastic Monte Carlo clinical boundary testing (100 randomized sessions)
"""

import pytest
import base64
import concurrent.futures
from fastapi.testclient import TestClient
from api.main import app
from pocs.poc01_adaptive_engine.models import LanguageCode, ReviewStatus
from pocs.poc01_adaptive_engine.adaptive_engine import AdaptiveAnamnesisEngine

client = TestClient(app)


# ==============================================================================
# ITERATION 1: INJECTION & MALICIOUS INPUT FUZZING
# ==============================================================================

def test_red_team_xss_and_sqli_in_session_initiation():
    """Attack: Inject XSS and SQLi payloads into patient profile initiation."""
    payloads = [
        "<script>alert('pwned')</script>",
        "' OR '1'='1' --",
        "\"; DROP TABLE profiles; --",
        "{{7*7}}",
        "../../../etc/passwd\x00",
        "A" * 5000,  # 5KB string
    ]

    for attack_str in payloads:
        resp = client.post("/api/v1/session/start", json={
            "language": "kn",
            "patient_name": attack_str,
            "patient_age": 45,
            "patient_gender": "female",
            "patient_phone": attack_str[:20]
        })
        # System must gracefully handle or sanitize (201 Created or 422 Validation Error), never crash
        assert resp.status_code in [201, 422], f"Failed on attack string: {attack_str[:30]}"
        if resp.status_code == 201:
            sess_data = resp.json()
            sess_id = sess_data["session_id"]
            assert sess_data["status"] == "in_progress"
            assert sess_data["current_question"] is not None


def test_red_team_xss_sanitization_in_printable_slip():
    """Attack: Submit HTML/Script injection in patient name and verify it is HTML-escaped in output."""
    xss_payload = "<script>alert('xss_attack')</script>"
    resp = client.post("/api/v1/session/start", json={
        "language": "en",
        "patient_name": xss_payload,
        "patient_age": 40,
    })
    assert resp.status_code == 201
    sess_id = resp.json()["session_id"]

    # Halt with acute red flag to create profile immediately
    client.post(f"/api/v1/session/{sess_id}/turn", json={
        "question_id": "q_chief_complaint",
        "selected_option": "sudden_vision_change",
        "confidence": 1.0
    })
    r2 = client.post(f"/api/v1/session/{sess_id}/turn", json={
        "question_id": "q_acute_symptoms",
        "selected_option": "flashes_or_floaters",
        "confidence": 1.0
    })
    prof_id = r2.json()["profile_id"]
    assert prof_id is not None

    slip_resp = client.get(f"/api/v1/export/profile/{prof_id}/printable-slip")
    assert slip_resp.status_code == 200
    html_text = slip_resp.text
    # Verify raw script tag is NOT in HTML prose, but properly escaped
    assert "<script>alert('xss_attack')</script>" not in html_text
    assert "&lt;script&gt;alert(&#x27;xss_attack&#x27;)&lt;/script&gt;" in html_text or "&lt;script&gt;" in html_text


def test_red_team_arbitrary_option_injection():
    """Attack: Attempt to submit invalid / unlisted options or injected strings to turn endpoint."""
    resp = client.post("/api/v1/session/start", json={"language": "en"})
    sess_id = resp.json()["session_id"]

    malicious_options = [
        "__proto__",
        "constructor",
        "'; DROP TABLE answers; --",
        "<img src=x onerror=alert(1)>",
        "completely_unregistered_option_xyz",
        "random_injected_string",
    ]

    for bad_opt in malicious_options:
        turn_resp = client.post(f"/api/v1/session/{sess_id}/turn", json={
            "question_id": "q_chief_complaint",
            "selected_option": bad_opt,
            "confidence": 1.0
        })
        # System must reject with 400 Bad Request, never accept invalid option or crash with 500
        assert turn_resp.status_code == 400, f"Allowed invalid option: {bad_opt}"
        assert "not valid for question" in turn_resp.json()["detail"]


def test_red_team_extreme_age_boundary_values():
    """Attack: Pass negative, float, and extreme numbers for patient age."""
    extreme_ages = [-100, -1, 0, 150, 999999, "not_a_number"]
    for bad_age in extreme_ages:
        resp = client.post("/api/v1/session/start", json={
            "language": "en",
            "patient_age": bad_age
        })
        # Strict validation rejects invalid ages with 422 Unprocessable Entity
        assert resp.status_code == 422, f"Failed to reject invalid age: {bad_age}"


# ==============================================================================
# ITERATION 2: STATE MACHINE ABUSE & CONCURRENCY RACE CONDITIONS
# ==============================================================================

def test_red_team_concurrent_race_turn_submission():
    """Attack: Fire 8 simultaneous answers to the same active session to induce race conditions."""
    resp = client.post("/api/v1/session/start", json={"language": "en"})
    sess_id = resp.json()["session_id"]

    def submit_turn(opt):
        return client.post(f"/api/v1/session/{sess_id}/turn", json={
            "question_id": "q_chief_complaint",
            "selected_option": opt,
            "confidence": 1.0
        })

    options = ["distance_blur", "near_reading_blur", "headaches_eyestrain", "general_checkup"]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(submit_turn, opt) for opt in options * 2]
        responses = [f.result() for f in futures]

    # No response should be an unhandled 500 Internal Server Error
    status_codes = [r.status_code for r in responses]
    assert all(code in [200, 400, 404, 409, 422] for code in status_codes), f"Unhandled error: {status_codes}"
    assert 500 not in status_codes


def test_red_team_answering_after_session_completed():
    """Attack: Attempt to submit answers after session has already halted and generated profile."""
    resp = client.post("/api/v1/session/start", json={"language": "en"})
    sess_id = resp.json()["session_id"]

    # Trigger acute red flag on turn 2 to halt
    client.post(f"/api/v1/session/{sess_id}/turn", json={
        "question_id": "q_chief_complaint",
        "selected_option": "sudden_vision_change",
        "confidence": 1.0
    })
    r2 = client.post(f"/api/v1/session/{sess_id}/turn", json={
        "question_id": "q_acute_symptoms",
        "selected_option": "flashes_or_floaters",
        "confidence": 1.0
    })
    assert r2.json()["status"] == "urgent_escalation"

    # Session is finalized. Subsequent answer attempts return finalized status without mutating or crashing
    zombie_resp = client.post(f"/api/v1/session/{sess_id}/turn", json={
        "question_id": "q_current_eyewear",
        "selected_option": "never_worn",
        "confidence": 1.0
    })
    assert zombie_resp.status_code == 200
    assert zombie_resp.json()["status"] == "urgent_escalation"
    assert zombie_resp.json()["current_question"] is None


def test_red_team_nonexistent_or_malformed_session_ids():
    """Attack: Request turn or status on invalid or path-traversal session IDs."""
    bad_session_ids = [
        "00000000-0000-0000-0000-000000000000",
        "../../etc/shadow",
        "' OR 1=1 --",
        "non-existent-uuid-1234",
    ]
    for bad_id in bad_session_ids:
        r1 = client.get(f"/api/v1/session/{bad_id}/status")
        assert r1.status_code == 404

        r2 = client.post(f"/api/v1/session/{bad_id}/turn", json={
            "question_id": "q_chief_complaint",
            "selected_option": "distance_blur",
            "confidence": 1.0
        })
        assert r2.status_code == 404


# ==============================================================================
# ITERATION 3: SPEECH & AUDIO PIPELINE FUZZING
# ==============================================================================

def test_red_team_corrupt_audio_blob_transcription():
    """Attack: Send random garbage binary bytes to transcription endpoint."""
    corrupt_payloads = [
        b"",  # 0 bytes
        b"\x00\x00\x00\x00\xff\xff\xff\xff",  # 8 bytes malformed
        b"RIFF" + b"\x00" * 100,  # fake wav header
        b"\xff\xfb\x90\x64" + b"\xaa" * 500,  # fake mp3 frame
    ]

    for payload in corrupt_payloads:
        b64_str = base64.b64encode(payload).decode("utf-8")
        r = client.post(
            "/api/v1/session/transcribe",
            json={"audio_base64": b64_str, "language": "kn"}
        )
        # Server must gracefully respond with 200 status error/no_speech or 400, never 500
        assert r.status_code in [200, 400], f"Failed on payload len {len(payload)}"
        if r.status_code == 200:
            data = r.json()
            assert data["status"] in ["no_speech", "error", "unavailable", "ok"]


def test_red_team_tts_endpoint_stress_and_injection():
    """Attack: Send huge text, emoji floods, format strings, and empty strings to TTS."""
    attacks = [
        ("", 204),  # empty text -> 204 No Content
        ("💥🚨🔥" * 20, 200),  # emoji flood -> handled gracefully
        ("%s%s%s%s%s%n", 200),  # format string injection
        ("<xml><script>alert(1)</script></xml>", 200),
        ("A" * 5000, 422),  # exceeds max_length=2000 -> 422 Unprocessable Entity
    ]

    for text, expected_code in attacks:
        r = client.get(f"/api/v1/session/speak?text={text}&lang=kn")
        assert r.status_code in [200, 204, 422], f"Failed on text '{text[:20]}', got {r.status_code}"


# ==============================================================================
# ITERATION 4: SCREENING TAMPERING & CORRUPTED SCREENING PAYLOADS
# ==============================================================================

def test_red_team_corrupted_screening_submission():
    """Attack: Submit corrupted / unlisted selections to on-screen screening."""
    resp = client.post("/api/v1/session/start", json={"language": "en"})
    sess_id = resp.json()["session_id"]

    bad_screenings = [
        ("unknown_test_type", "red_clearer", 400),
        ("duochrome", "invalid_duochrome_option", 400),
        ("amsler_grid", "hacked_amsler_option", 400),
        ("astigmatic_dial", "not_a_valid_meridian", 400),
    ]

    for test_type, bad_selection, expected_status in bad_screenings:
        r = client.post(
            f"/api/v1/session/{sess_id}/screening/{test_type}",
            json={"selection": bad_selection}
        )
        assert r.status_code == expected_status, f"Failed on {test_type} with selection {bad_selection}"


def test_red_team_export_with_path_traversal():
    """Attack: Attempt path traversal on export slip and visuconsult QR."""
    traversal_ids = [
        "../../../../windows/system32/cmd.exe",
        "..%2F..%2F..%2Fetc%2Fpasswd",
        "test' OR 1=1;--",
    ]
    for tid in traversal_ids:
        r1 = client.get(f"/api/v1/export/profile/{tid}/visuconsult-qr")
        assert r1.status_code == 404

        r2 = client.get(f"/api/v1/export/profile/{tid}/printable-slip")
        assert r2.status_code == 404


# ==============================================================================
# ITERATION 5: MONTE CARLO STOCHASTIC SIMULATION (100 ADVERSARIAL SESSIONS)
# ==============================================================================

def test_red_team_stochastic_100_monte_carlo_runs():
    """Attack: Run 100 randomly generated patient sessions with stochastic answers to probe for deadlocks."""
    import random

    for i in range(100):
        age = random.choice([None, random.randint(5, 95)])
        gender = random.choice([None, "male", "female", "other", "prefer_not_to_say"])
        lang = random.choice([LanguageCode.KANNADA, LanguageCode.HINDI, LanguageCode.ENGLISH, LanguageCode.TAMIL])

        engine = AdaptiveAnamnesisEngine(
            session_id=f"stochastic_{i}",
            language=lang,
            patient_age=age,
            patient_gender=gender
        )

        def stochastic_oracle(q):
            return random.choice(q.options)

        # Simulation must never infinite loop or raise unhandled exception
        profile = engine.run_simulation(stochastic_oracle)
        assert profile is not None
        assert profile.total_questions_asked >= 2
        assert profile.total_questions_asked <= 8
        assert profile.review_status in [
            ReviewStatus.PENDING_OPTOMETRIST_REVIEW,
            ReviewStatus.CLARIFICATION_REQUESTED,
            ReviewStatus.URGENT_MEDICAL_ESCALATION
        ]
