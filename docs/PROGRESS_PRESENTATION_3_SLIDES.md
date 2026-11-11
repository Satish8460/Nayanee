# NAYANEE — 3-SLIDE PROGRESS PRESENTATION

**Hackathon:** ZEISS Hackathon  
**Primary Theme:** Theme 2 — No-Device Vision Intelligence & Accessible Clinical UX  
**Complementary Theme:** Theme 1 — AI/ML for Advanced Frugal Innovation (AFI)  
**Supporting Theme:** Theme 4 — AI-Powered Digital Experiences  
**Repository:** https://github.com/Satish8460/Nayanee  

---

## SLIDE 1: The Problem & The No-Device Vision

### The Challenge in Rural & Retail Optical Stores
- In thousands of optical stores and rural vision centers across India and the Global South, there is **no dedicated eye-testing hardware — just a phone or a counter**.
- Walk-in customers face a broken consultation flow:
  1. **Rigid Questionnaires:** 20–30 question static forms fatigue customers with irrelevant questions.
  2. **Language Barrier:** Customers speak native Indic languages (Kannada, Hindi, Tamil, Telugu, Malayalam), while forms are in English.
  3. **The Unsafe LLM Trap:** Generic AI chatbots hallucinate optical prescriptions, lack medical safety boundaries, and require expensive cloud GPUs.

### The Nayanee Solution
- A lightweight, smartphone-native, voice-guided anamnesis system that captures a walk-in customer's functional visual needs to generate actionable eyewear recommendations and optometrist triage — **using zero specialized hardware**.

---

## SLIDE 2: Technical Breakthroughs & Novelty

### 1. Information-Theoretic Question Pruning (POC-01)
- Calculates **Shannon Entropy** across 5 functional vision domains (Distance, Near, Digital Screen, Environment, Eyewear History).
- Dynamically selects the highest information-gain question next and prunes non-applicable inquiries (reducing consultation duration by **> 25%** for presbyopic customers).

### 2. Dravidian-First Voice Architecture (POC-02)
- Solves OS regional voice-pack deficiencies by streaming native Indic MP3 speech on-demand from the server (`/api/v1/session/speak`).
- Uses authentic, culturally grounded clinical phrasing rather than mechanical Google Translate word-for-word text.

### 3. Zero-GPU Clinical Spoken-Language Understanding (POC-03)
- Real-time intent parser (`speech_analyzer.py`) maps free-form spoken native responses directly to clinical categories with match confidence scores ($0.0 - 1.0$) on ordinary CPU.

### 4. Deterministic Clinical Safety Sentinel
- Hardcoded acute red-flag triage sentinel (sudden pain, flashes of light, or sudden vision loss) **halts routine intake immediately**, routing emergency cases to ophthalmology with **zero hallucination risk**.

---

## SLIDE 3: Impact, Traction & Frugal Architecture

### 1. Remote Optometrist Decision Support (POC-05)
- **Optical Lifestyle Advisor:** Generates pre-refraction optical considerations based on screen workload (> 8 hrs $\rightarrow$ blue filter, intermediate corridors) and outdoor exposure ($\rightarrow$ UV400 / photochromic).
- **Printable Consultation Slip:** Instant HTML slip (`/printable-slip`) formatted for store thermal/A4 printers with optometrist sign-off block and EMR export.

### 2. Advanced Frugal Innovation (AFI Ethos)
- Runs on commodity hardware: any Android smartphone, store laptop, or a **$35 Raspberry Pi** (< 80 MB RAM footprint, zero GPU, zero API per-query token fees).

### 3. Verification & Readiness
- **38 / 38 automated unit & integration tests passing** in `< 1.5s` (`run_tests.bat`).
- Tested with multi-language end-to-end simulations (`demo_e2e.py`).
- One-click launch via `start.bat`.
