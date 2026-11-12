# NAYANEE — 1 TO 3-MINUTE VIDEO DEMO SCRIPT & STORYBOARD

**Hackathon Theme:** ZEISS Theme 2 — No-Device Vision Intelligence & Accessible Clinical UX (Theme 1: AFI)  
**Target Video Duration:** 2 Minutes (Optimal for Hackathon Judges)  
**Tools to Record:** Windows Game Bar (`Win + Alt + R`), Loom, or OBS  

---

## Storyboard & Voiceover Breakdown

### [0:00 – 0:25] The Hook & Problem (Theme 2 Alignment)
- **Visual:** Browser showing Nayanee home screen (`http://localhost:8000`).
- **Screen Action:** Show the "Customer Intake" screen with the language cards (Kannada, Hindi, Tamil, Telugu, Malayalam, English). Type:
  - Patient Full Name: `Parvathamma B.`
  - Age: `62`
  - Language: Click on `ಕನ್ನಡ (Kannada)`
  - Click `Start Vision Interview →`
- **Voiceover:**
  > *"Hello judges. In thousands of rural optical stores across India, there is no autorefractor or eye-testing equipment—just a smartphone or a counter. Walk-in customers face language barriers and static 25-question forms. This is Nayanee: No-Device Vision Intelligence. Let's onboard a walk-in customer in her native language, Kannada."*

---

### [0:25 – 0:55] Native Voice & Adaptive Questioning (POC-01 & POC-02)
- **Visual:** The Interview screen opens. Active badge shows `Turn 1 • 👤 Patient: Parvathamma B. (62y)`.
- **Screen Action:** Click `🔊 ಪ್ರಶ್ನೆ ಆಲಿಸಿ (ಕೇಳಿ)`. Clear Kannada voice plays through speaker.
  - The voice asks: *"ನಮಸ್ಕಾರ, ನಿಮ್ಮ ಕಣ್ಣಿನಲ್ಲಿ ಮುಖ್ಯವಾಗಿ ಏನು ತೊಂದರೆ ಕಾಣಿಸ್ತಿದೆ?"*
  - Click the second option: `ಹತ್ತಿರದ್ದು ಅಥವಾ ಮೊಬೈಲ್-ಪೇಪರ್ ಓದಲು ಕಷ್ಟ ಆಗ್ತಿದೆ` (near reading blur).
  - Turn 2 loads with acute red flag question. Click `ಇಲ್ಲ, ಅಂತಹ ಯಾವುದೇ ತೊಂದರೆ ಇಲ್ಲ` (no acute symptoms).
- **Voiceover:**
  > *"Nayanee communicates in natural spoken audio—not literal machine translations, but caring, culturally authentic clinical phrasing. Parvathamma reports difficulty reading near text on her phone. Notice how the engine adapts: it automatically checks for clinical emergency red flags first, keeping patient safety front and center."*

---

### [0:55 – 1:25] Live Voice Recording & Zero-GPU SLU (POC-01 & POC-03)
- **Visual:** Progressing through turns.
- **Screen Action:** 
  - On the screen time question, tap the **🎤** microphone button.
  - Notice the button switches to **⏹️ Recording...** and real live audio waves animate as you speak: *"ಒಂದು ಗಂಟೆಗಿಂತ ಕಡಿಮೆ"* (or *"less than one hour"*).
  - Tap **⏹️** to send. The audio is transcribed and the zero-GPU intent matcher immediately selects the option.
  - Show how questions about progressive lens adaptation or previous spectacles are automatically pruned because Parvathamma never wore glasses.
- **Voiceover:**
  > *"Unlike rigid questionnaires, Nayanee's Information-Entropy engine calculates the most informative question next, automatically skipping irrelevant queries and pruning consultation time by over 25%. Our direct microphone audio pipeline records 16kHz PCM audio and analyzes it with our zero-GPU Clinical SLU engine, matching intent with 95% confidence without expensive cloud hardware."*

---

### [1:25 – 1:55] Optometrist Triage & Optical Lifestyle Guidance (POC-05)
- **Visual:** Interview concludes. Summary card appears: `✅ Functional Vision Profile Created for Parvathamma B.`.
- **Screen Action:** Click `🔍 View in Optometrist Portal`.
  - The Optometrist queue opens, showing `Parvathamma B. • 62 yrs • Female • KN • PENDING REVIEW`.
  - Click on her profile to inspect.
  - Point mouse to the `Optical & Lifestyle Design Considerations (Pre-Refraction)` box showing introductory reading aid recommendation and intermediate screen advice.
- **Voiceover:**
  > *"When the intake completes, the responses are structured into a Functional Vision Profile. In the Optometrist Review Portal, the practitioner sees her complete functional profile, domain confidence radar, and pre-refraction optical lifestyle guidance tailored for her presbyopia."*

---

### [1:55 – 2:15] Printable Consultation Slip & Closing (AFI Ethos)
- **Visual:** Click `🖨️ Print Consultation Slip`. A clean, printable consultation slip opens in a new tab.
- **Screen Action:** Scroll down to show the patient demographics, reported functional demands, acute triage clearance, and optometrist sign-off block.
- **Voiceover:**
  > *"With one tap, store staff can print an official consultation slip for subjective refraction. Nayanee requires zero specialized hardware, runs entirely on CPU, passes 39 automated tests, and turns any ordinary smartphone into an accessible vision intelligence terminal. Thank you."*
