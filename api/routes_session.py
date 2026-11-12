"""Session REST & WebSocket Routes for Nayanee Multilingual Intake.
"""

import uuid
import json
import base64
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException, status, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

from pocs.poc01_adaptive_engine.models import (
    LanguageCode,
    Question,
    FunctionalVisionProfile,
    ReviewStatus,
)
from pocs.poc01_adaptive_engine.adaptive_engine import AdaptiveAnamnesisEngine
from pocs.poc01_adaptive_engine.profile_generator import build_functional_profile
from pocs.poc01_adaptive_engine.questions_bank import get_question_by_id
from pocs.poc01_adaptive_engine.speech_analyzer import analyze_transcript_for_question
from pocs.poc02_multilingual_speech.multilingual_pipeline import MultilingualSpeechPipeline
from pocs.poc02_multilingual_speech.mock_providers import (
    SimulatedIndicASRProvider,
    SimulatedBrowserLocalASRProvider,
    SimulatedTTSProvider,
)
from .session_store import store

import io
from fastapi.responses import Response

try:
    from gtts import gTTS
    HAS_GTTS = True
except ImportError:
    HAS_GTTS = False

try:
    import speech_recognition as sr
    HAS_SR = True
except ImportError:
    HAS_SR = False

router = APIRouter(prefix="/api/v1/session", tags=["Session"])

primary_asr = SimulatedIndicASRProvider()
secondary_asr = SimulatedBrowserLocalASRProvider()
tts_provider = SimulatedTTSProvider()
speech_pipeline = MultilingualSpeechPipeline(primary_asr, secondary_asr, tts_provider)


class StartSessionRequest(BaseModel):
    language: LanguageCode = LanguageCode.ENGLISH
    patient_name: Optional[str] = "Anonymous Patient"
    patient_age: Optional[int] = None
    patient_gender: Optional[str] = None
    patient_phone: Optional[str] = None
    demographics: Optional[Dict[str, Any]] = Field(default_factory=dict)


class LocalizedOption(BaseModel):
    id: str
    label: str


class QuestionPayload(BaseModel):
    id: str
    category: str
    domain: str
    text: str
    options: List[str]
    localized_options: List[LocalizedOption] = Field(default_factory=list)
    tts_audio_base64: Optional[str] = None
    selection_rationale: Optional[str] = None


class SessionResponse(BaseModel):
    session_id: str
    status: str
    language: LanguageCode
    turn_index: int
    current_question: Optional[QuestionPayload] = None
    profile_id: Optional[str] = None
    review_status: Optional[str] = None
    contradictions_count: int = 0
    red_flags_count: int = 0


class SubmitTurnRequest(BaseModel):
    question_id: str
    selected_option: str
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)


class SubmitAudioTurnRequest(BaseModel):
    question_id: str
    audio_base64: str
    expected_option: Optional[str] = None


class AnalyzeAnswerRequest(BaseModel):
    question_id: str
    transcript: str
    language: LanguageCode = LanguageCode.ENGLISH


class AnalyzeAnswerResponse(BaseModel):
    selected_option: str
    confidence: float
    label: str


def format_question_payload(q: Question, lang: LanguageCode) -> QuestionPayload:
    lang_key = lang.value if hasattr(lang, "value") else str(lang)
    localized_text = q.text_translations.get(lang_key, q.text_en)
    tts_res = speech_pipeline.synthesize_question(localized_text, lang_key)
    audio_b64 = None
    if tts_res.audio_data_bytes:
        audio_b64 = base64.b64encode(tts_res.audio_data_bytes).decode("utf-8")

    opts_map = q.options_translations.get(lang_key, {})
    localized_options = []
    for opt in q.options:
        label = opts_map.get(opt, opt.replace("_", " ").title())
        localized_options.append(LocalizedOption(id=opt, label=label))

    return QuestionPayload(
        id=q.id,
        category=q.category.value,
        domain=q.domain.value,
        text=localized_text,
        options=q.options,
        localized_options=localized_options,
        tts_audio_base64=audio_b64,
        selection_rationale=f"Base information weight: {q.base_information_weight}",
    )


@router.get("/speak")
def stream_speech_audio(text: str, lang: str = "en"):
    """Streams real native-voice MP3 audio across Kannada, Hindi, Tamil, Telugu, Malayalam, and English."""
    if HAS_GTTS and text.strip():
        try:
            lang_code = lang.lower().split("-")[0]
            tts = gTTS(text=text, lang=lang_code, slow=False)
            mp3_buffer = io.BytesIO()
            tts.write_to_fp(mp3_buffer)
            mp3_buffer.seek(0)
            return Response(content=mp3_buffer.read(), media_type="audio/mpeg")
        except Exception:
            pass
    return Response(content=b"", media_type="audio/mpeg", status_code=204)


@router.post("/start", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def start_session(req: StartSessionRequest):
    session_id = str(uuid.uuid4())
    p_name = req.patient_name.strip() if req.patient_name and req.patient_name.strip() else "Anonymous Patient"
    engine = AdaptiveAnamnesisEngine(
        session_id=session_id,
        language=req.language,
        patient_name=p_name,
        patient_age=req.patient_age,
        patient_gender=req.patient_gender,
        patient_phone=req.patient_phone,
    )
    store.save_engine(session_id, engine)

    first_q = engine.select_next_question()
    if not first_q:
        raise HTTPException(status_code=500, detail="Failed to initialize first question.")

    return SessionResponse(
        session_id=session_id,
        status="in_progress",
        language=req.language,
        turn_index=1,
        current_question=format_question_payload(first_q, req.language),
        contradictions_count=0,
        red_flags_count=0,
    )


@router.post("/{session_id}/turn", response_model=SessionResponse)
def submit_turn(session_id: str, req: SubmitTurnRequest):
    engine = store.get_engine(session_id)
    if not engine:
        existing_profile = store.get_profile_by_session(session_id)
        if existing_profile:
            return SessionResponse(
                session_id=session_id,
                status="completed" if not existing_profile.red_flags else "urgent_escalation",
                language=existing_profile.customer_language,
                turn_index=existing_profile.total_questions_asked,
                current_question=None,
                profile_id=existing_profile.profile_id,
                review_status=existing_profile.review_status.value,
                contradictions_count=len(existing_profile.contradictions),
                red_flags_count=len(existing_profile.red_flags),
            )
        raise HTTPException(status_code=404, detail="Session not found or expired.")

    try:
        q = get_question_by_id(req.question_id)
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid question ID: {req.question_id}")

    if req.selected_option not in q.options:
        raise HTTPException(
            status_code=400,
            detail=f"Option '{req.selected_option}' is not valid for question '{q.id}'. Allowed: {q.options}",
        )

    engine.record_answer(q, req.selected_option, confidence=req.confidence)

    next_q = engine.select_next_question()

    if next_q:
        return SessionResponse(
            session_id=session_id,
            status="in_progress",
            language=engine.language,
            turn_index=len(engine.turn_history) + 1,
            current_question=format_question_payload(next_q, engine.language),
            contradictions_count=len(engine.contradictions),
            red_flags_count=len(engine.red_flags),
        )

    avg_unc = sum(engine.domain_uncertainty.values()) / len(engine.domain_uncertainty)
    profile = build_functional_profile(
        session_id=session_id,
        language=engine.language,
        answers=engine.answers,
        turn_history=engine.turn_history,
        contradictions=engine.contradictions,
        red_flags=engine.red_flags,
        uncertainty_score=avg_unc,
        engine_type="adaptive",
        patient_name=getattr(engine, "patient_name", "Anonymous Patient"),
        patient_age=getattr(engine, "patient_age", None),
        patient_gender=getattr(engine, "patient_gender", None),
        patient_phone=getattr(engine, "patient_phone", None),
    )
    store.save_profile(profile)

    final_status = "urgent_escalation" if profile.red_flags else "completed"

    return SessionResponse(
        session_id=session_id,
        status=final_status,
        language=engine.language,
        turn_index=len(engine.turn_history),
        current_question=None,
        profile_id=profile.profile_id,
        review_status=profile.review_status.value,
        contradictions_count=len(profile.contradictions),
        red_flags_count=len(profile.red_flags),
    )


@router.post("/analyze-answer", response_model=AnalyzeAnswerResponse)
def analyze_answer_endpoint(req: AnalyzeAnswerRequest):
    """Analyzes a spoken or typed transcript and maps it to the best matching question option."""
    opt, conf, label = analyze_transcript_for_question(
        req.question_id, req.transcript, req.language.value
    )
    return AnalyzeAnswerResponse(
        selected_option=opt,
        confidence=conf,
        label=label,
    )


@router.post("/{session_id}/audio-turn", response_model=SessionResponse)
def submit_audio_turn(session_id: str, req: SubmitAudioTurnRequest):
    engine = store.get_engine(session_id)
    if not engine:
        raise HTTPException(status_code=404, detail="Session not found.")

    try:
        audio_bytes = base64.b64decode(req.audio_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 audio payload.")

    asr_res, confirm_prompt = speech_pipeline.process_incoming_audio(
        audio_bytes, engine.language.value
    )

    q = get_question_by_id(req.question_id)
    if req.expected_option and req.expected_option in q.options:
        selected_option = req.expected_option
        conf = asr_res.confidence
    else:
        opt, match_conf, _ = analyze_transcript_for_question(
            req.question_id, asr_res.normalized_transcript, engine.language.value
        )
        selected_option = opt
        conf = min(asr_res.confidence, match_conf)

    return submit_turn(
        session_id,
        SubmitTurnRequest(
            question_id=req.question_id,
            selected_option=selected_option,
            confidence=conf,
        ),
    )


@router.websocket("/{session_id}/ws")
async def websocket_session_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    engine = store.get_engine(session_id)
    if not engine:
        await websocket.send_json({"error": "Session not found."})
        await websocket.close()
        return

    try:
        while True:
            data_text = await websocket.receive_text()
            data = json.loads(data_text)
            action = data.get("action")

            if action == "answer":
                qid = data.get("question_id")
                option = data.get("selected_option")
                req = SubmitTurnRequest(question_id=qid, selected_option=option)
                resp = submit_turn(session_id, req)
                await websocket.send_json(resp.model_dump())
                if resp.status in ["completed", "urgent_escalation"]:
                    break
            elif action == "ping":
                await websocket.send_json({"pong": True})
            else:
                await websocket.send_json({"warning": f"Unknown action: {action}"})

    except WebSocketDisconnect:
        pass
    except Exception as exc:
        await websocket.send_json({"error": str(exc)})
        await websocket.close()


@router.get("/{session_id}/status")
def get_session_status(session_id: str):
    engine = store.get_engine(session_id)
    if not engine:
        prof = store.get_profile_by_session(session_id)
        if prof:
            return {
                "session_id": session_id,
                "status": "completed",
                "profile_id": prof.profile_id,
                "review_status": prof.review_status.value,
            }
        raise HTTPException(status_code=404, detail="Session not found.")

    return {
        "session_id": session_id,
        "status": "in_progress",
        "turns_completed": len(engine.turn_history),
        "domain_uncertainty": {k.value: round(v, 3) for k, v in engine.domain_uncertainty.items()},
        "contradictions_count": len(engine.contradictions),
        "red_flags_count": len(engine.red_flags),
    }


class TranscribeAudioRequest(BaseModel):
    audio_base64: str
    language: str = "en"


@router.post("/transcribe")
def transcribe_recorded_audio(req: TranscribeAudioRequest):
    """Transcribes real browser-recorded 16kHz PCM WAV audio in native Indic languages."""
    if not HAS_SR:
        return {"transcript": "", "status": "unavailable", "detail": "SpeechRecognition package not installed"}

    try:
        wav_bytes = base64.b64decode(req.audio_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 audio payload.")

    if len(wav_bytes) < 44:
        return {"transcript": "", "status": "no_speech", "detail": "Recording too short"}

    lang_map = {
        "kn": "kn-IN",
        "hi": "hi-IN",
        "ta": "ta-IN",
        "te": "te-IN",
        "ml": "ml-IN",
        "en": "en-IN",
    }
    google_lang = lang_map.get(req.language, "en-IN")

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(io.BytesIO(wav_bytes)) as source:
            audio_data = recognizer.record(source)
        transcript = recognizer.recognize_google(audio_data, language=google_lang)
        return {"transcript": transcript, "status": "ok", "language": google_lang}
    except sr.UnknownValueError:
        return {"transcript": "", "status": "no_speech", "detail": "Could not detect clear speech"}
    except sr.RequestError as exc:
        return {"transcript": "", "status": "network_error", "detail": str(exc)}
    except Exception as exc:
        return {"transcript": "", "status": "error", "detail": str(exc)}
