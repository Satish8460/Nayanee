"""Tests for Frontend Static Assets and PWA Service Worker Serving.
"""

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_manifest_serving():
    resp = client.get("/static/manifest.json")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Nayanee — Adaptive Vision Intelligence"
    assert data["short_name"] == "Nayanee"
    assert data["start_url"] == "/"


def test_service_worker_serving():
    resp = client.get("/static/sw.js")
    assert resp.status_code == 200
    assert "nayanee-cache-v1" in resp.text
    assert "addEventListener('fetch'" in resp.text


def test_frontend_root_content():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "<!DOCTYPE html>" in resp.text
    assert "manifest.json" in resp.text
    assert "serviceWorker" in resp.text


def test_screening_and_zeiss_multilingual_localization():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text

    # Verify SCREENING_I18N contains all 6 languages
    assert "const SCREENING_I18N =" in html
    for lang in ["kn:", "hi:", "ta:", "te:", "ml:", "en:"]:
        assert lang in html

    # Verify all 3 on-screen tests are present in dictionary
    assert "duochrome:" in html
    assert "astigmatic_dial:" in html
    assert "amsler_grid:" in html

    # Verify ZEISS recommendation localization exists for all 6 languages
    assert "const ZEISS_I18N =" in html
    assert "smartlife:" in html
    assert "digital:" in html
    assert "drivesafe:" in html
    assert "clearview:" in html


def test_voice_narration_integration_in_frontend():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text

    # Audio buttons and status indicators
    assert 'id="screeningAudioBtn"' in html
    assert 'id="screeningAudioStatus"' in html
    assert "playScreeningAudio" in html
    assert "playZeissAudio" in html
    assert "zeissAudioBtn" in html
    assert "/api/v1/session/speak?text=" in html

