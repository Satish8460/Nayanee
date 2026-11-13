# POC-07 INTEGRATION PLAN: ZEISS LENS RECOMMENDER & ON-SCREEN SCREENING

**Feature:** Integration of Deterministic ZEISS Lens Recommender & Interactive On-Screen Visual Functional Tests into Nayanee Production Application.  
**Theme Alignment:** ZEISS Hackathon Theme 2 (Primary) & Theme 1 (AFI).  
**Repository Branch:** `main`  
**Git Remote:** `https://github.com/Satish8460/Nayanee.git`  

---

## 🎯 Objective
Integrate the verified, deterministic algorithms from `pocs/poc07_zeiss_matcher_and_screening/` into the core FastAPI backend and frontend UI, enabling:
1. **Interactive On-Screen Functional Vision Screening:** Optional 45-second calibrated tests (Duochrome, Astigmatic Clock Dial, Amsler Grid) directly in the browser.
2. **Automated ZEISS Lens & Coating Recommendations:** Multi-factor optical rules engine outputting specific ZEISS products (Digital, SmartLife Progressive, DriveSafe, ClearView, PhotoFusion X) with clinical rationales and store dispensing notes.
3. **Optometrist Portal & Printable Slip Display:** Instant visibility of recommended ZEISS lens solutions on the optometrist triage dashboard and 1-click printable receipt slip.

---

## 🏗️ Architectural Phases

### Phase 1: Data Model & Backend API Integration
- **Files to modify:**
  - `pocs/poc01_adaptive_engine/models.py`:
    - Add `onscreen_screening_results: Dict[str, Any]` and `zeiss_recommendation: Optional[Dict[str, Any]]` fields to `FunctionalVisionProfile`.
  - `pocs/poc01_adaptive_engine/profile_generator.py`:
    - Invoke `ZeissLensRecommender.recommend(profile, onscreen_test_results)` when building the final `FunctionalVisionProfile`.
  - `api/routes_session.py`:
    - Add endpoint `POST /api/v1/session/{session_id}/screening/{test_type}` to submit on-screen test responses (`duochrome`, `astigmatic_dial`, `amsler_grid`).
    - If `amsler_grid` reports metamorphopsia or scotoma, automatically trigger the deterministic **emergency clinical halt** (`ReviewStatus.URGENT_MEDICAL_ESCALATION`).

### Phase 2: Optometrist Review Portal & Printable Slip
- **Files to modify:**
  - `api/clinical_export.py`:
    - Add a styled **ZEISS Ophthalmic Lens Recommendation Block** to the printable consultation slip (`/printable-slip`):
      - Primary Lens & Family (e.g., *ZEISS SmartLife Progressive - Near Priority*)
      - Recommended Coating (e.g., *ZEISS DuraVision BlueProtect*)
      - Recommended Index (e.g., *1.60 High Index*)
      - Optician Dispensing Instructions
      - On-Screen Screening Findings (Duochrome balance, Astigmatic meridian, Amsler grid clearance)
  - `api/routes_optometrist.py`:
    - Ensure `zeiss_recommendation` and `onscreen_screening_results` are serialized in `GET /api/v1/profiles/{profile_id}`.

### Phase 3: Frontend UI & Interactive Testing UX
- **Files to modify:**
  - `frontend/index.html`:
    - **Customer Intake Flow:**
      - After question turns complete (or via a "Quick On-Screen Vision Check" button), render calibrated, high-contrast SVG optotypes:
        1. *Duochrome Balance (Split Red/Green)*: Single tap (`Red Clearer`, `Green Clearer`, `Equally Sharp`).
        2. *Astigmatic Clock Dial*: Single tap on meridian line or `All Lines Equal`.
        3. *Amsler Grid*: Single tap (`All Lines Straight`, `Wavy Distortion`, `Dark Patch`).
      - On the completion summary card, display a customer-friendly **"Your Recommended ZEISS Eyewear Solution"** card.
    - **Optometrist Portal View:**
      - In the patient profile detail pane, render an **Executive ZEISS Lens Dispensing Card** featuring the ZEISS product badge, coating badge, progression corridor, and optician fitting instructions.

### Phase 4: Automated Verification & CI
- **Files to modify:**
  - `tests/test_api_endpoints.py`:
    - Add integration tests for `/screening/{test_type}` endpoints.
    - Verify that emergency Amsler findings trigger urgent escalation.
    - Verify that printable slip contains the recommended ZEISS product name.
  - Run full test suite: `py -3.12 -m pytest tests/ -v` (Target: 100% pass rate).

---

## 🔒 Engineering Constraints
1. **Zero Flakiness:** All tests must be 100% deterministic and runnable on CPU (<80 MB RAM).
2. **No External ML Dependencies:** Rely strictly on pure optical physics and standard SVG DOM elements.
3. **Backward Compatibility:** All existing 48 tests and current intake flows must remain 100% functional.
