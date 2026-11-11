"""Tests for WebSocket Real-time Session Streaming and Printable Slip Export.
"""

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_printable_slip_export():
    resp = client.get("/api/v1/export/profile/demo-kn-parvathamma/printable-slip")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    html = resp.text
    assert "NAYANEE" in html
    assert "Optical Consultation Slip" in html
    assert "Functional Vision Profile" in html
    assert "Pre-Refraction Optical Guidance" in html
    assert "Optometrist Refraction & Clinical Notes" in html


def test_websocket_realtime_session_flow():
    start_resp = client.post("/api/v1/session/start", json={"language": "kn"})
    assert start_resp.status_code == 201
    session_id = start_resp.json()["session_id"]

    with client.websocket_connect(f"/api/v1/session/{session_id}/ws") as ws:
        ws.send_json({"action": "ping"})
        msg = ws.receive_json()
        assert msg == {"pong": True}

        ws.send_json({
            "action": "answer",
            "question_id": "q_chief_complaint",
            "selected_option": "near_reading_blur"
        })
        turn_reply = ws.receive_json()
        assert turn_reply["session_id"] == session_id
        assert turn_reply["turn_index"] == 2
        assert turn_reply["current_question"]["id"] == "q_acute_symptoms"
