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
