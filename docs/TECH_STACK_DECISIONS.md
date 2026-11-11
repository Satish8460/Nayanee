# Technology Decision Records (TDR)

**Project:** Nayanee (ನಯನಿ)  
**Status:** Approved  

---

## TDR-001: Backend Framework Selection
- **Decision:** Python 3.12 with **FastAPI** + **Pydantic v2**.
- **Context:** High-performance async REST & WebSocket support, rapid decision tree execution, microsecond latency.
- **Consequences:** Low latency (< 15 ms request processing overhead), automated OpenAPI docs, strong type validation.

---

## TDR-002: Frontend Architecture
- **Decision:** **Accessible HTML5 + Modern CSS + PWA Service Worker**.
- **Context:** Must render on mobile browsers (Android Chrome, Samsung Internet) with fast initial load (< 250 KB footprint), responsive touch controls, and high-contrast typography.
- **Consequences:** Runs instantly without requiring app store installation; supports offline caching via `sw.js`.

---

## TDR-003: Adaptive Decision Engine Logic
- **Decision:** **Hybrid Information-Entropy Scoring + Clinical Rule Hierarchy**.
- **Context:** Zero latency, deterministic explainability, zero cloud inference cost, zero hallucination risk.
- **Consequences:** Runs in < 0.1 ms on standard CPU, 100% auditable, reproducible in tests.

---

## TDR-004: Multilingual Voice Architecture
- **Decision:** **Server-Streamed MP3 (gTTS) + Multi-Tier Fallback (Web Speech API + Synthesizer Earcons)**.
- **Context:** Standard Windows and Android OS do not pre-install Dravidian speech packs (Kannada, Telugu, Tamil, Malayalam). Streaming MP3 audio via HTML5 Audio ensures 100% audible voice on every client without requiring OS speech pack installation.

---

## TDR-005: Clinical Spoken-Language Understanding (SLU) & Intent Lexicon Matching
- **Decision:** **Multilingual Clinical Lexicon + Token Overlap Scoring**.
- **Context:** Spoken customer responses in Indic languages (e.g. "ದೂರದ್ದು ಸರಿಯಾಗಿ ಕಾಣಿಸ್ತಿಲ್ಲ" or "ಮೊಬೈಲ್ ಓದಲು ಕಷ್ಟ") need to be accurately mapped to clinical canonical option IDs (e.g. `distance_blur`, `near_reading_blur`) without sending audio to expensive third-party NLU cloud providers.
- **Consequences:** Runs in < 1 ms on CPU, matches regional colloquial variants, produces explainable confidence scores.

---

## TDR-006: Patient Demographics & Multi-Session Intake Flow
- **Decision:** **Session-scoped Demographics Collection + Dual View State**.
- **Context:** Intake requires tracking patient name, age, gender, and reference numbers for clinical handover while enabling seamless consecutive patient intakes in busy retail stores.
- **Consequences:** Optometrist dashboard immediately identifies each patient, consultation slips contain identity metadata, and store staff can reset for the next patient with one click.
