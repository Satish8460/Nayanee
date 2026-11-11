"""Unit & Integration tests for Clinical Spoken Language Understanding (SLU).
Tests semantic analysis of spoken Indic and English transcripts against clinical options.
"""

from fastapi.testclient import TestClient
from api.main import app
from pocs.poc01_adaptive_engine.speech_analyzer import analyze_transcript_for_question


client = TestClient(app)


def test_spoken_kannada_distance_blur_analysis():
    opt, conf, label = analyze_transcript_for_question(
        "q_chief_complaint", "ದೂರದ್ದು ಸರಿಯಾಗಿ ಕಾಣಿಸ್ತಿಲ್ಲ", language_code="kn"
    )
    assert opt == "distance_blur"
    assert conf >= 0.70
    assert "ದೂರದ್ದು" in label


def test_spoken_kannada_near_reading_blur_analysis():
    opt, conf, label = analyze_transcript_for_question(
        "q_chief_complaint", "ಮೊಬೈಲ್ ಪೇಪರ್ ಓದಲು ಕಷ್ಟ ಆಗ್ತಿದೆ", language_code="kn"
    )
    assert opt == "near_reading_blur"
    assert conf >= 0.70
    assert "ಹತ್ತಿರದ್ದು" in label or "ಮೊಬೈಲ್" in label


def test_spoken_kannada_headaches_analysis():
    opt, conf, label = analyze_transcript_for_question(
        "q_chief_complaint", "ವಿಪರೀತ ತಲೆನೋವು ಮತ್ತು ಕಣ್ಣು ಆಯಾಸ", language_code="kn"
    )
    assert opt == "headaches_eyestrain"
    assert conf >= 0.70


def test_spoken_kannada_acute_red_flag_none():
    opt, conf, label = analyze_transcript_for_question(
        "q_acute_symptoms", "ಇಲ್ಲ ಅಂತಹ ಯಾವುದೇ ತೊಂದರೆ ಇಲ್ಲ", language_code="kn"
    )
    assert opt == "no_acute_symptoms"
    assert conf >= 0.70


def test_spoken_hindi_analysis():
    opt, conf, label = analyze_transcript_for_question(
        "q_chief_complaint", "दूर का काफी धुंधला दिखता है", language_code="hi"
    )
    assert opt == "distance_blur"
    assert conf >= 0.70


def test_spoken_english_analysis():
    opt, conf, label = analyze_transcript_for_question(
        "q_chief_complaint", "I have difficulty reading my mobile phone", language_code="en"
    )
    assert opt == "near_reading_blur"
    assert conf >= 0.70


def test_api_analyze_answer_endpoint():
    resp = client.post(
        "/api/v1/session/analyze-answer",
        json={
            "question_id": "q_chief_complaint",
            "transcript": "ದೂರದ್ದು ಮಸುಕಾಗಿದೆ",
            "language": "kn"
        }
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["selected_option"] == "distance_blur"
    assert data["confidence"] >= 0.70
    assert len(data["label"]) > 0
