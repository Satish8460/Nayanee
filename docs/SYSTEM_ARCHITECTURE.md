# Nayanee — System Architecture & Component Design

**Status:** Completed & Validated  

---

## 1. High-Level Architecture Diagram

```mermaid
flowchart TD
    subgraph ClientLayer ["Client Layer (Smartphone / Tablet / Desktop)"]
        UI["Accessible Mobile Web UI (HTML5 + CSS3 + PWA)"]
        AudioCap["Audio Capture & Speech Synthesizer Client"]
        LocalCache["Session State & Local Storage (Offline resilience)"]
    end

    subgraph Gateway ["API & Orchestration Layer (FastAPI Backend)"]
        APIRouter["FastAPI REST & WebSocket Gateway"]
        SessionMgr["Interview Session Manager"]
    end

    subgraph IntelligenceEngine ["Intelligence & Reasoning Engine"]
        SpeechAbs["Speech Abstraction Layer (ASR / TTS Provider Routing)"]
        AdaptiveEngine["Adaptive Anamnesis Engine (Entropy & Rule Evaluator)"]
        ContradictionDetector["Contradiction & Validation Engine"]
        ProfileBuilder["Functional Vision Profile Generator"]
        LifestyleAdvisor["Ergonomic Lifestyle & Lens Guidance Engine"]
        EscalationMatrix["Clinical Red-Flag & Escalation Sentinel"]
    end

    subgraph ReviewLayer ["Professional Workflow Layer"]
        ReviewPortal["Optometrist Review Interface"]
        PrintableSlip["Printable Consultation Intake Slip"]
        AuditLog["Audit & Traceability Store"]
    end

    UI <--> |Voice Audio / Text / WebSocket| APIRouter
    APIRouter --> SessionMgr
    SessionMgr --> SpeechAbs
    SessionMgr --> AdaptiveEngine
    AdaptiveEngine <--> ContradictionDetector
    AdaptiveEngine <--> EscalationMatrix
    AdaptiveEngine --> ProfileBuilder
    ProfileBuilder --> LifestyleAdvisor
    LifestyleAdvisor --> ReviewPortal
    LifestyleAdvisor --> PrintableSlip
```

---

## 2. Core Subsystems

1. **Multilingual Speech Abstraction Subsystem:** 4-tier speech cascade (Cloud Indic $\to$ Web Speech API $\to$ Acoustic Earcon Synthesizer $\to$ Visual Text Chips).
2. **Adaptive Anamnesis Subsystem:** Domain uncertainty tracking across 6 functional dimensions with dynamic entropy reduction.
3. **Contradiction & Red-Flag Sentinels:** Evaluates bidirectional consistency matrix and enforces immediate emergency halting upon acute ocular symptoms.
4. **Clinical Export & Decision Support:** Generates plain text EMR/EHR briefings and printable physical consultation intake slips.
