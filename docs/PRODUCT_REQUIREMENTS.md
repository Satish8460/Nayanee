# Nayanee — Product Requirements Document (PRD)

**Document Version:** 1.0.0  
**Status:** Completed & Validated  

---

## 1. Problem Statement

1. **Information Asymmetry in Optical Retail:** Customers in semi-urban and rural retail shops or vision camps often cannot clearly describe whether their difficulties stem from near work, distance blur, astigmatic distortion, glare, or presbyopic transitions.
2. **Language & Dialect Barriers:** India has rich linguistic diversity. Optical staff in multi-state catchment areas frequently cannot converse fluently in the customer's mother tongue (e.g., Kannada, Tamil, Telugu, Malayalam, Hindi).
3. **Rigid or Superficial Questionnaires:** Static paper forms or rigid surveys ask 25+ irrelevant questions (causing fatigue and drop-off) or skip critical lifestyle context (e.g., night driving, prolonged mobile screen usage, tailoring, welding).
4. **Unreliable Data Handover:** Optometrists receive hasty verbal summaries, missing crucial red flags (e.g., sudden onset vision loss, halos around lights, unmanaged diabetes) or contradictory statements.

---

## 2. Target Personas

### Persona A: Smt. Parvathamma (Rural Customer, Age 52, Mandya, Karnataka)
- **Primary Language:** Kannada (monolingual).
- **Tech Literacy:** Low (uses WhatsApp voice notes, YouTube).
- **Vision Concern:** Trouble threading sewing needles and reading bus numbers at dusk.
- **Goal:** Speak naturally in Kannada on a phone/kiosk and have her daily vision difficulties understood.

### Persona B: Rajesh Kumar (Semi-urban Optical Store Assistant, Age 28, Belagavi)
- **Role:** First point of contact at an optical shop.
- **Pain Point:** Limited clinical optometry knowledge; high shop rush; struggles with dialect differences.
- **Goal:** Guided, automated interview tool that collects customer history reliably while he prepares the lens trial frame.

### Persona C: Dr. Ananya Sharma (Consulting Optometrist, Bangalore)
- **Role:** Reviews refractive cases and prescribers corrective lenses.
- **Pain Point:** Spends 60% of refraction time teasing out lifestyle needs and history instead of performing clinical retinoscopy/subjective refraction.
- **Goal:** A structured, unambiguous Functional Vision Profile with flagged contradictions, lifestyle context, and clinical escalation alerts.

---

## 3. Functional Requirements

- **FR-01 (Multilingual Speech-First):** 6 languages (Kannada, Hindi, Tamil, Telugu, Malayalam, English) with voice and text fallback.
- **FR-02 (Adaptive Anamnesis):** Information-entropy dynamic prioritization pruning irrelevant branches (cutting questions by 27% to 82%).
- **FR-03 (Contradiction & Red-Flag Sentinels):** Real-time contradiction detection and immediate safety halt on acute ocular emergencies.
- **FR-04 (Functional Vision Profile):** Structured, traceable clinical profile separating customer reports from interpretations.
- **FR-05 (Optometrist Review & Decision Support):** Web triage dashboard, ergonomic lens guidance, 1-click clipboard EHR copy, and printable consultation intake slip.
