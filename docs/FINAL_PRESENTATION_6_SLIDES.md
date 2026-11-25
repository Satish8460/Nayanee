# NAYANEE (ನಯनी) — Final Project Presentation (6-Slide Deck)

**Hackathon:** ZEISS Hackathon — Final Submission  
**Team:** Group Coders  
**Members:** Satish SM, Tejaswini C B  
**Institution:** BMS Institute of Technology & Management (BMSIT)  
**Primary Theme:** Theme 2 — No-Device Vision Intelligence & Accessible Clinical UX  
**Complementary Theme:** Theme 1 — AI/ML for Advanced Frugal Innovation (AFI)  
**PowerPoint File:** [`docs/Nayanee_Final_Presentation_Coders_6_Slides_v3.pptx`](file:///d:/Project/Nayanee/docs/Nayanee_Final_Presentation_Coders_6_Slides_v3.pptx)  

---

## SLIDE 1: Executive Vision — No-Device Vision Intelligence for Walk-In Retail
*Category Pill:* **Theme 2 (Primary) & Theme 1 (AFI)**  
*Slide Number:* **01 / 06**

### Left Column: The Rural & Retail Optical Dilemma (Problem & AFI Ethos)
* ✕ **Zero Hardware Equipment:** Small clinics & optical shops cannot afford $15,000 autorefractors—just a phone or front counter.
* ✕ **24-Question Survey Fatigue:** Static lifestyle surveys (e.g. ZEISS Vision Profile) suffer >40% drop-off due to tedious multi-slider forms.
* ✕ **Language & Literacy Barrier:** Over 85% of Indian walk-in patients speak regional Indic languages; English intake forms alienate them.
* ✕ **Commercial Red-Flag Blindness:** Commercial questionnaires focus only on selling lenses, ignoring acute retinal tears or glaucoma emergencies.

### Right Column: Embedded Figure
* **Fig 1: Multi-Lingual Intake Kiosk (6 Indic Languages + Demographics)**
* *Caption:* Touch-First Kiosk: Kannada, Hindi, Tamil, Telugu, Malayalam & English. Captures age and gender to initialize Bayesian physiological priors.

### Bottom Metrics
* **$0** Hardware Equipment Capex | **6** Native Indic Languages | **< 90s** Intake Completion Time | **100%** Zero-GPU CPU Execution

---

## SLIDE 2: Mathematical Foundation — Active Bayesian Inference & Adaptive Anamnesis
*Category Pill:* **Algorithmic Innovation**  
*Slide Number:* **02 / 06**

### Left Column: Active Inference & Information Gain
* • **Domain Uncertainty Vector:** Tracks remaining entropy $U(D) \in [0.0, 1.0]$ across 6 clinical axes: Distance, Near, Screen, Lifestyle, Eyewear, Red-Flag.
* • **InfoGain Ranking Equation:** Dynamically scores candidate questions at every turn:  
  $$\text{InfoGain}(q) = W_{\text{base}}(q) \times U(D_q) \times B_{\text{chief}} \times B_{\text{age}} \times B_{\text{gender}}$$
* • **Physiological Age & Gender Priors:** Age $\ge 40$ boosts Near domain ($1.25\times$); Female $\ge 40$ boosts dry-eye risk ($1.25\times$) and shorter forearm reach ($33\text{ cm}$).
* • **Tree Pruning & Contradiction Matrix:** Selecting `never_worn` prunes 3 questions; catches conflicting answers (e.g. near blur vs zero strain).
* • **67% Question Reduction:** Averages 7.2 questions (under 90s) vs 24 questions (7–10m) in ZEISS Vision Profile without clinical depth loss.

### Right Column: Embedded Figure
* **Fig 2: Active Anamnesis Turn 1 (Kannada UI + English Subtitle)**
* *Caption:* Spoken Audio Playback 🔊 + Touch-Response Chief Complaint Tiles. Prominent full-card presentation preserving every colloquial phrasing detail.

### Bottom Metrics
* **7.2** Avg Questions Asked | **< 2 ms** Inference Turn Latency | **67%** Reduction vs 24-Qn Forms | **100%** Deterministic Safety

---

## SLIDE 3: Zero-Hardware Clinical Screening Suite & Turn-2 Circuit Breaker
*Category Pill:* **Device-Free Triaging**  
*Slide Number:* **03 / 06**

### Left Column: 3 On-Screen Tests & Turn-2 Sentinel
* • **Red-Green Duochrome Test:** Evaluates longitudinal chromatic aberration (650nm Red vs 535nm Green). Red clearer indicates myopia; Green clearer indicates hyperopia/over-minusing.
* • **Astigmatic Clock Dial:** Visualizes the Conoid of Sturm at 30° radial meridians on Retina/OLED displays, identifying dominant cylinder axis for JCC refinement.
* • **Amsler Grid Macular Guard:** Evaluates central 10° of visual field. Detects metamorphopsia (wavy lines) or scotomas (blind spots), flagging macular edema or AMD.
* • **Turn-2 Invariant Circuit Breaker:** Every patient is probed for acute red flags on Turn 2. Flashes, floaters, or severe pain immediately halt intake with urgent hospital triage.
* • **Zero Hallucination Guarantee:** Deterministic state machine; generates an emergency ophthalmology pass and never dispenses glasses when pathology is suspected.

### Right Column: 2×2 Prominent Clinical Showcase (4 Large Un-diminished Figures)
* **Fig 3: Duochrome (Spherical Balance)** — *Red (650nm) vs Green (535nm)*: Evaluates Myopia/Hyperopia Accommodation Balance.
* **Fig 4: Astigmatic Clock Dial Fan** — *30° Radial Cylindrical Meridians*: Identifies Principal Astigmatic Axis.
* **Fig 5: Amsler Grid Macular Guard** — *Central 10° Foveal Field Check*: Detects Metamorphopsia & Macular Edema.
* **Fig 6: Spoken Red-Flag Emergency Triage** — *Voice Waveform + Instant Speech SLU*: Immediate Emergency Halt on Acute Symptoms.

### Bottom Metrics
* **3** Calibrated Screen Tests | **10°** Central Macular Guard | **Turn 2** Safety Circuit Breaker | **100%** Screen Hardware Agnostic

---

## SLIDE 4: Interactive Visual Perception Simulator
*Category Pill:* **Retail Psychology & Optical Physics**  
*Slide Number:* **04 / 06**

### Left Column: Solving "The Invisible Product Dilemma"
* • **The Retail Bottleneck:** Ophthalmic lenses are transparent pieces of plastic. A ₹1,200 generic stock lens and a ₹8,000 ZEISS lens look identical to a walk-in patient.
* • **Hardware-Accelerated Split Slider:** Engineered using CSS `clip-path` dynamically bound to a range slider at 60 FPS without heavy WebGL GPU overhead.
* • **DriveSafe Night Road:** Standard: Blinding LED high-beam starburst halo obscuring a roadside pedestrian. ZEISS DriveSafe: 64% glare attenuation reveals pedestrian & lane lines.
* • **SmartLife Progressive:** Standard: Narrow 10mm reading corridor with lateral swim distortion and head strain. ZEISS SmartLife: Edge-to-edge panoramic reading zone.
* • **BlueProtect & ClearView:** Digital blue scatter relief (BlueProtect); 3× wider peripheral clear zone vs standard spherical stock lens edge blur (ClearView).

### Right Column: Embedded Figure
* **Fig 7: Real-Time ZEISS Match & Split Perception Simulator**
* *Caption:* Progressive Adaptation Risk: 20/100 (LOW) • Interactive Split Slider showing Standard Progressive vs SmartLife Wide Panoramic.

### Bottom Metrics
* **4** Dynamic Scenario Modes | **60 FPS** Split Slider Rendering | **64%** Headlight Glare Reduction | **3×** Wider ClearView Zone

---

## SLIDE 5: ZEISS Retail Interoperability & Practice Handover
*Category Pill:* **Ecosystem Integration**  
*Slide Number:* **05 / 06**

### Left Column: ZEISS VISUCONSULT 500 Digital Bridge
* • **Pure-Python Vector SVG QR Generator:** Generates compact vector QR codes offline without external cloud dependencies, encoding patient anamnesis and screening.
* • **Practice iPad Scanning:** Optometrist scans the QR with VISUCONSULT 500 iPad camera, instantly loading refraction parameters, corridor lengths, and coating tiers.
* • **Sanitized Printable Optical Slip:** HTML5 print layout (`@media print`) generates standard 80mm thermal receipt slips or A4 PDFs with optometrist sign-off block.
* • **Two-Wheeler Transit Safety:** Recognizes motorcycle/scooter commute vector; escalates to 1.60 Shatterproof Polycarbonate / Trivex (ANSI Z87.1 road protection).
* • **OfficeLens Focal Ergonomics:** Maps occupational posture to Maximum Intermediate Distance (M.I.D.): Book (100cm), Desk (200cm), Room (400cm).

### Right Column: Embedded Figure
* **Fig 8: Standardized VISUCONSULT 500 Optical Slip**
* *Caption:* Includes Anamnesis, ZEISS Match, SVG QR & Optometrist Sign-off Block for seamless practice handover.

### Bottom Metrics
* **1-Click** VISUCONSULT 500 QR Bridge | **80mm / A4** Thermal & Print Slip | **0–100** Adaptation Risk Score | **ANSI Z87.1** Road & Sports Safety

---

## SLIDE 6: Full Tech Stack, Red Team Hardening & Roadmap
*Category Pill:* **Production Readiness & Verification**  
*Slide Number:* **06 / 06**

### Left Column: Full Tech Stack & Red Team Hardening
* • **Core Backend Stack:** Python 3.12, FastAPI 0.110+, Pydantic v2 (Rust-backed validation), Uvicorn async ASGI. Total RAM footprint < 120 MB.
* • **Frontend & Speech:** Zero-Framework Vanilla HTML5/CSS3/ES6+ (<180 KB payload), W3C Web Speech API + gTTS server-side audio fallback.
* • **5-Iteration Red Team Hardening:** Tested XSS injection, 8-thread concurrent race conditions, audio fuzzing, and invalid options. Patched XSS via `html.escape`; whitelisted screening inputs.
* • **85 / 85 Automated Tests:** Comprehensive pytest test suite covering unit logic, API contracts, speech pipelines, and 100 stochastic Monte Carlo runs in 4.06 seconds.

### Right Column: Deployment, Repository & Roadmap
* ✓ **Live Demonstration Access:** Equipped with 1-click Cloudflare Quick Tunnel (`share_nayanee.bat`) for zero-config public HTTPS testing on judges' mobile phones.
* ✓ **Production PWA Kiosk:** Service Worker (`sw.js`) + Web Manifest (`manifest.json`) for 1-tap installation on Android/iPad clinic reception counters.
* ✓ **Near-Term Roadmap (2–4 wks):** On-device Vosk WebAssembly speech recognition for 100% offline rural camps; optometrist dim-room dark mode.
* ✓ **Major Roadmap (3–6 mos):** OpenCV WebAssembly selfie-camera pupillometry (monocular PD & seg-height) with credit-card scaling; ABDM/FHIR locker sync.
* ★ **GitHub Repository:** [https://github.com/Satish8460/Nayanee](https://github.com/Satish8460/Nayanee) (Complete, production-grade open source codebase with CI automation).

### Bottom Metrics
* **85 / 85** CI Test Suite Passing | **4.06s** Test Execution Time | **5 Cycles** Red Team Security Audit | **GitHub** [https://github.com/Satish8460/Nayanee](https://github.com/Satish8460/Nayanee)
