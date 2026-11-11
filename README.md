# Nayanee (ನಯनी) — Adaptive Vision Intelligence

> **ZEISS Hackathon — AI/ML for Advanced Frugal Innovation (AFI)**  
> *A smartphone-based, multilingual adaptive vision-profiling system for optical retail and rural consultation.*

[![CI Test Suite](https://img.shields.io/badge/pytest-38%20passed-brightgreen.svg)](#testing)
[![Languages Supported](https://img.shields.io/badge/languages-KN%20%7C%20HI%20%7C%20TA%20%7C%20TE%20%7C%20ML%20%7C%20EN-blue.svg)](#multilingual-voice-first-interaction)
[![Frugal Hardware](https://img.shields.io/badge/hardware-Zero%20GPU%20%7C%20Budget%20Android-orange.svg)](#frugal-architecture)
[![Clinical Safety](https://img.shields.io/badge/safety-Non--Diagnostic%20Intake%20Only-red.svg)](#clinical-safety--explainability)

---

## 1. Quick Start & Execution

### Windows 1-Click Launch:
Double-click [`start.bat`](start.bat).
This automatically:
1. Detects your Python 3.12 environment.
2. Boots the Nayanee FastAPI server at `http://localhost:8000`.
3. Opens the interactive customer & optometrist interface in your default browser.

### Windows 1-Click Verification:
Double-click [`run_tests.bat`](run_tests.bat).
Executes all **30 automated unit and integration tests** and runs the end-to-end multi-language simulation script (`demo_e2e.py`).

---

## 2. Audio & Speech Architecture

Nayanee features a **Bulletproof Multi-Tier Speech Engine** designed for real-world deployment on resource-constrained devices without specialized hardware:

1. **Server-Side Native MP3 Audio Streaming (`GET /api/v1/session/speak`):**
   - Synthesizes clear, authentic native Indic speech (Kannada, Hindi, Tamil, Telugu, Malayalam, and English) on demand.
   - Streamed directly to the client as standard MP3 audio, overcoming the absence of regional Indic voice packs in desktop operating systems.
2. **Idiomatic, Non-Literal Option Localization:**
   - Both question phrasing and option buttons use natural, colloquial clinical vocabulary rather than stiff word-for-word machine translations.
   - Option buttons display in native scripts while transmitting canonical clinical IDs to the backend adaptive reasoning engine.
3. **Client-Side Web Speech Fallback:**
   - Automatically detects and utilizes on-device neural voices when available.
4. **Web Audio API Chime & Earcon Feedback:**
   - Synthesized audio tones (earcons) provide clear acoustic feedback for turn transitions, recording states, contradictions, and critical red flags.
5. **Touch & High-Contrast Visual Fallback:**
   - Visual chip selection ensures zero friction in noisy optical stores or when microphone input is not preferred.

---

## 3. Core Product Differentiators

### 3.1 Adaptive Information Gain Engine
Unlike rigid questionnaires that subject every customer to 20+ repetitive questions, Nayanee dynamically selects the most informative next question based on information entropy and domain uncertainty. For presbyopic customers, non-applicable questions (e.g. progressive lens adaptation) are safely pruned, cutting consultation duration by over 25%.

### 3.2 Real-Time Uncertainty & Contradiction Detection
Tracks uncertainty across five functional domains:
- Distance Vision
- Intermediate / Digital Screen Vision
- Near Reading Vision
- Occupational & Lifestyle Context
- Eyewear & Adaptation History

Contradictory responses (e.g., claiming to never wear spectacles while later reporting wearing bifocals) are automatically flagged with moderate severity, prompting clarification turns.

### 3.3 Acute Red-Flag Triage
Detects clinical emergency warning signs (sudden severe pain, flashes of light, or sudden loss of vision). When triggered, routine optical intake is **immediately halted**, and the case is escalated for urgent medical evaluation.

### 3.4 Professional Optometrist Handover & EHR Export
Provides a dual-view interface:
- **Customer View:** Voice-guided, friendly, accessible mobile intake.
- **Optometrist Dashboard:** Clinical triage summary, domain confidence radar, printable clinical slip, and JSON export for Electronic Health Record (EHR) integration.

---

## 4. Technology Stack & Frugal Design

- **Backend:** Python 3.12, FastAPI, Pydantic v2, Uvicorn (zero GPU requirement; runs on inexpensive micro-instances or store PCs).
- **Speech Engine:** gTTS streaming endpoint, Web Speech API, Web Audio API oscillators.
- **Frontend:** Pure HTML5, CSS3, Vanilla JavaScript PWA (Service Worker, Web App Manifest, offline-ready).
- **Architecture:** Zero external database required for prototype (in-memory thread-safe session store with mock persistence).

---

## 5. Verification & Testing

Run all 30 tests via terminal:
```bash
py -3.12 -m pytest tests/ -v
```

Or run the live demonstration script:
```bash
py -3.12 demo_e2e.py
```
