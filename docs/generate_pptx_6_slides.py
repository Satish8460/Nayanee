"""Generates an executive-grade, visually polished 6-slide widescreen (.pptx) presentation
for Nayanee — ZEISS Hackathon Final Submission.
Team: Group Coders | Satish SM, Tejaswini C B | BMSIT
Themes: Theme 2 (No-Device Vision Intelligence) & Theme 1 (AFI)
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE


def build_final_6_slide_deck(output_paths: list = None):
    if output_paths is None:
        output_paths = [
            "docs/Nayanee_Final_Presentation_Coders_6_Slides.pptx",
        ]
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    FONT_FAMILY = "Segoe UI"

    # Executive High-Contrast Color System
    BG_DARK = RGBColor(6, 21, 45)          # #06152D (Deep Navy)
    BG_CARD = RGBColor(14, 38, 77)         # #0E264D (Card Navy)
    BG_CARD_BORDER = RGBColor(30, 68, 128) # #1E4480
    ACCENT_CYAN = RGBColor(0, 210, 255)    # #00D2FF (Electric Cyan)
    ACCENT_BLUE = RGBColor(0, 114, 255)    # #0072FF (ZEISS Cobalt)
    ACCENT_GREEN = RGBColor(0, 230, 118)   # #00E676 (Emerald Green)
    ACCENT_RED = RGBColor(255, 82, 82)     # #FF5252 (Warning Crimson)
    ACCENT_ORANGE = RGBColor(255, 171, 0)  # #FFAB00 (Amber Glare)
    TEXT_LIGHT = RGBColor(240, 246, 255)   # #F0F6FF
    TEXT_MUTED = RGBColor(140, 168, 204)   # #8CA8CC
    WHITE = RGBColor(255, 255, 255)

    def paint_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_top_nav(slide, title_text, category_pill, slide_num, total_slides="06"):
        # Header Box
        tx = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(8.5), Inches(0.95))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_sub = tf.paragraphs[0]
        p_sub.text = "NAYANEE (ನಯनी) • ZEISS HACKATHON FINAL SUBMISSION  |  GROUP CODERS (BMSIT)"
        p_sub.font.size = Pt(9.0)
        p_sub.font.bold = True
        p_sub.font.color.rgb = ACCENT_CYAN
        p_sub.space_after = Pt(2)

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(21)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE

        # Pill Tag (Top Right)
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.3), Inches(0.42), Inches(3.2), Inches(0.46))
        pill.fill.solid()
        pill.fill.fore_color.rgb = BG_CARD
        pill.line.color.rgb = ACCENT_CYAN
        pill.line.width = Pt(1)
        tf_p = pill.text_frame
        p_p = tf_p.paragraphs[0]
        p_p.text = category_pill
        p_p.font.size = Pt(9.5)
        p_p.font.bold = True
        p_p.font.color.rgb = ACCENT_CYAN
        p_p.alignment = PP_ALIGN.CENTER

        # Slide Number
        num_box = slide.shapes.add_textbox(Inches(11.0), Inches(7.08), Inches(1.5), Inches(0.3))
        tf_n = num_box.text_frame
        p_n = tf_n.paragraphs[0]
        p_n.text = f"{slide_num} / {total_slides}"
        p_n.font.size = Pt(9.5)
        p_n.font.color.rgb = TEXT_MUTED
        p_n.alignment = PP_ALIGN.RIGHT

    def create_metric_tile(slide, left, top, width, height, stat_value, stat_label, accent_color=ACCENT_CYAN):
        tile = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        tile.fill.solid()
        tile.fill.fore_color.rgb = BG_CARD
        tile.line.color.rgb = BG_CARD_BORDER
        tile.line.width = Pt(1)

        tx = slide.shapes.add_textbox(left, top + Inches(0.08), width, height - Inches(0.12))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = stat_value
        p1.font.size = Pt(20)
        p1.font.bold = True
        p1.font.color.rgb = accent_color
        p1.alignment = PP_ALIGN.CENTER

        p2 = tf.add_paragraph()
        p2.text = stat_label
        p2.font.size = Pt(8.2)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_MUTED
        p2.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 1: EXECUTIVE VISION — THE RURAL & RETAIL OPTICAL DILEMMA
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    paint_background(s1)
    add_top_nav(s1, "No-Device Vision Intelligence for Walk-In Retail", "Theme 2 (Primary) & Theme 1 (AFI)", "01")

    # Presenter Subtitle Bar
    pres_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.7), Inches(0.3))
    tf_pres = pres_box.text_frame
    p_pres = tf_pres.paragraphs[0]
    p_pres.text = "Presented by Group Coders: Satish SM, Tejaswini C B  |  BMS Institute of Technology & Management"
    p_pres.font.size = Pt(9.5)
    p_pres.font.color.rgb = TEXT_MUTED

    # Left Column: The Problem Card
    left_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.6), Inches(4.15))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = BG_CARD
    left_card.line.color.rgb = ACCENT_RED
    left_card.line.width = Pt(1.5)

    tx_l = s1.shapes.add_textbox(Inches(1.05), Inches(1.85), Inches(5.1), Inches(3.8))
    tf_l = tx_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "THE RURAL & RETAIL OPTICAL DILEMMA"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED
    p.space_after = Pt(10)

    problems = [
        ("Zero Hardware Capex", "Small clinics & optical stores cannot afford $15,000 autorefractors—just a smartphone or a front counter."),
        ("24-Question Survey Fatigue", "Static lifestyle surveys (e.g. ZEISS Vision Profile) suffer >40% drop-off due to tedious multi-slider forms."),
        ("Language & Literacy Divide", "Over 85% of Indian walk-in patients speak regional Indic languages; English intake forms alienate them."),
        ("Commercial Red-Flag Blindness", "Commercial questionnaires focus only on selling lenses, ignoring acute retinal tears or glaucoma emergencies.")
    ]
    for title, desc in problems:
        p = tf_l.add_paragraph()
        p.text = f"✕  {title}: "
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT

        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(6)

    # Right Column: The Nayanee Solution Card
    right_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.7), Inches(5.7), Inches(4.15))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = BG_CARD
    right_card.line.color.rgb = ACCENT_GREEN
    right_card.line.width = Pt(1.5)

    tx_r = s1.shapes.add_textbox(Inches(7.05), Inches(1.85), Inches(5.2), Inches(3.8))
    tf_r = tx_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "THE NAYANEE BREAKTHROUGH (AFI ETHOS)"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(10)

    solutions = [
        ("Zero Hardware Dependency", "Captures complete functional vision demands on any commodity ₹6,000 Android smartphone or tablet."),
        ("6 Native Indic Languages", "Communicates naturally via voice in Kannada, Hindi, Tamil, Telugu, Malayalam, and English with audio narration."),
        ("Active Bayesian Adaptiveness", "Information-theoretic engine cuts intake by 67% (7–8 questions in <90s vs 24 questions in 7–10 minutes)."),
        ("Deterministic Clinical Safety", "Hardcoded acute red-flag sentinel halts on emergency symptoms with zero hallucination and direct hospital triage.")
    ]
    for title, desc in solutions:
        p = tf_r.add_paragraph()
        p.text = f"✓  {title}: "
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT

        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(6)

    # Bottom Metric Strip
    create_metric_tile(s1, Inches(0.8), Inches(6.05), Inches(2.7), Inches(0.85), "$0", "HARDWARE EQUIPMENT CAPEX", ACCENT_GREEN)
    create_metric_tile(s1, Inches(3.7), Inches(6.05), Inches(2.7), Inches(0.85), "6", "NATIVE INDIC LANGUAGES", ACCENT_CYAN)
    create_metric_tile(s1, Inches(6.8), Inches(6.05), Inches(2.7), Inches(0.85), "< 90s", "INTAKE COMPLETION TIME", ACCENT_CYAN)
    create_metric_tile(s1, Inches(9.7), Inches(6.05), Inches(2.8), Inches(0.85), "100%", "ZERO-GPU CPU EXECUTION", ACCENT_BLUE)

    # =========================================================================
    # SLIDE 2: MATHEMATICAL INNOVATION — ACTIVE BAYESIAN ANAMNESIS
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    paint_background(s2)
    add_top_nav(s2, "Active Bayesian Inference & Adaptive Anamnesis", "Algorithmic Innovation", "02")

    # Left Column: Mathematical Formulation
    card2_l = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(4.35))
    card2_l.fill.solid()
    card2_l.fill.fore_color.rgb = BG_CARD
    card2_l.line.color.rgb = ACCENT_CYAN
    card2_l.line.width = Pt(1.5)

    tx2_l = s2.shapes.add_textbox(Inches(1.05), Inches(1.68), Inches(5.1), Inches(4.0))
    tf2_l = tx2_l.text_frame
    tf2_l.word_wrap = True

    p = tf2_l.paragraphs[0]
    p.text = "ACTIVE INFERENCE & INFORMATION GAIN"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(8)

    math_points = [
        ("Domain Uncertainty Vector", "Tracks entropy U(D) in [0.0, 1.0] across 6 axes: Distance, Near, Intermediate, Lifestyle, Eyewear, Red-Flag."),
        ("InfoGain Ranking Equation", "Scores candidate questions: InfoGain(q) = W_base(q) × U(D_q) × B_chief × B_age × B_gender dynamically at every turn."),
        ("Physiological Age Priors", "Age ≥40 boosts Near domain by 1.25× and Intermediate by 1.15×; Age <35 boosts Lifestyle/Screen domain by 1.20×."),
        ("Gender Optometric Priors", "Female ≥40 boosts dry-eye risk (1.25×) and Near reach (33cm forearm); Male boosts driving transit (1.05×)."),
        ("Entropy Decay Queue", "Recorded answers consume domain entropy (U(D) ← U(D) - 0.55 × W_base), naturally pivoting to unexplored domains.")
    ]
    for t, d in math_points:
        p = tf2_l.add_paragraph()
        p.text = f"• {t}: "
        p.font.size = Pt(9.2)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(5)

    # Right Column: Pruning & Consistency
    card2_r = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(4.35))
    card2_r.fill.solid()
    card2_r.fill.fore_color.rgb = BG_CARD
    card2_r.line.color.rgb = ACCENT_BLUE
    card2_r.line.width = Pt(1.5)

    tx2_r = s2.shapes.add_textbox(Inches(7.05), Inches(1.68), Inches(5.2), Inches(4.0))
    tf2_r = tx2_r.text_frame
    tf2_r.word_wrap = True

    p = tf2_r.paragraphs[0]
    p.text = "TREE PRUNING & CONTRADICTION SENTINEL"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    p.space_after = Pt(8)

    pruning_points = [
        ("Conditional Pruning", "Selecting 'never_worn' instantly prunes glasses age, satisfaction, and contact lens routine questions."),
        ("Prerequisite Gating", "Contact lens wear time and dry-eye routine questions only appear if patient explicitly wears contacts."),
        ("Real-Time Contradiction Matrix", "Detects cognitive conflicts (e.g. reporting near reading blur but zero strain, or 'never worn' but 2yo glasses)."),
        ("67% Question Reduction", "Averages 7.2 questions (under 90s) vs 24 questions (7–10m) in ZEISS Vision Profile without clinical depth loss."),
        ("Fatigue Cap Safeguard", "Strict 8-question maximum prevents cognitive exhaustion and random clicking (satisficing).")
    ]
    for t, d in pruning_points:
        p = tf2_r.add_paragraph()
        p.text = f"✓ {t}: "
        p.font.size = Pt(9.2)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(5)

    # Bottom Metric Strip
    create_metric_tile(s2, Inches(0.8), Inches(6.05), Inches(2.7), Inches(0.85), "7.2", "AVG QUESTIONS ASKED", ACCENT_CYAN)
    create_metric_tile(s2, Inches(3.7), Inches(6.05), Inches(2.7), Inches(0.85), "< 2 ms", "INFERENCE TURN LATENCY", ACCENT_GREEN)
    create_metric_tile(s2, Inches(6.8), Inches(6.05), Inches(2.7), Inches(0.85), "67%", "REDUCTION VS 24-QN FORMS", ACCENT_CYAN)
    create_metric_tile(s2, Inches(9.7), Inches(6.05), Inches(2.8), Inches(0.85), "100%", "DETERMINISTIC SAFETY", ACCENT_BLUE)

    # =========================================================================
    # SLIDE 3: ZERO-HARDWARE CLINICAL SCREENING SUITE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    paint_background(s3)
    add_top_nav(s3, "Zero-Hardware Refractive & Macular Screening Suite", "Device-Free Triaging", "03")

    # Left Column: 3 Screen Tests
    card3_l = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(4.35))
    card3_l.fill.solid()
    card3_l.fill.fore_color.rgb = BG_CARD
    card3_l.line.color.rgb = ACCENT_GREEN
    card3_l.line.width = Pt(1.5)

    tx3_l = s3.shapes.add_textbox(Inches(1.05), Inches(1.68), Inches(5.1), Inches(4.0))
    tf3_l = tx3_l.text_frame
    tf3_l.word_wrap = True

    p = tf3_l.paragraphs[0]
    p.text = "3 CALIBRATED ON-SCREEN TESTS"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(8)

    tests_points = [
        ("Red-Green Duochrome Test", "Evaluates longitudinal chromatic aberration (650nm Red vs 535nm Green). Red clearer indicates myopia/under-correction; Green clearer indicates hyperopia/over-minusing."),
        ("Astigmatic Clock Dial", "Visualizes the Conoid of Sturm at 30° radial meridians (12-to-6, 1-to-7) on Retina/OLED displays, identifying dominant cylinder axis for JCC refinement."),
        ("Amsler Grid Macular Guard", "Evaluates central 10° of visual field. Detects metamorphopsia (wavy lines) or scotomas (dark spots), flagging macular edema or Age-Related Macular Degeneration (AMD)."),
        ("Screen Agnostic Calibration", "Pure HTML5 Canvas and CSS responsive vector rendering; works on any mobile screen without hardware calibration tools.")
    ]
    for t, d in tests_points:
        p = tf3_l.add_paragraph()
        p.text = f"• {t}: "
        p.font.size = Pt(9.2)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(6)

    # Right Column: Acute Red-Flag Emergency Sentinel
    card3_r = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(4.35))
    card3_r.fill.solid()
    card3_r.fill.fore_color.rgb = BG_CARD
    card3_r.line.color.rgb = ACCENT_RED
    card3_r.line.width = Pt(1.5)

    tx3_r = s3.shapes.add_textbox(Inches(7.05), Inches(1.68), Inches(5.2), Inches(4.0))
    tf3_r = tx3_r.text_frame
    tf3_r.word_wrap = True

    p = tf3_r.paragraphs[0]
    p.text = "TURN-2 INVARIANT EMERGENCY CIRCUIT BREAKER"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED
    p.space_after = Pt(8)

    safety_points = [
        ("Invariant Turn-2 Trigger", "Every patient is probed for acute red flags on Turn 2: sudden vision loss, severe unilateral ocular pain, or flashes/floaters."),
        ("Instant Triage Halt", "If an acute red flag is reported, the session halts immediately. It does NOT waste critical time asking about reading distance or sunglasses."),
        ("Emergency Status Escalation", "Flips state to URGENT MEDICAL TRIAGE, warning the patient of retinal tear or angle-closure glaucoma risks."),
        ("Referral Pass Generation", "Generates an urgent ophthalmology referral pass with red-flag audit logs ready for tertiary hospital emergency departments."),
        ("Zero Hallucination Guarantee", "Deterministic state machine; never guesses a medical diagnosis or dispenses glasses when pathology is suspected.")
    ]
    for t, d in safety_points:
        p = tf3_r.add_paragraph()
        p.text = f"✓ {t}: "
        p.font.size = Pt(9.2)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(5)

    # Bottom Metric Strip
    create_metric_tile(s3, Inches(0.8), Inches(6.05), Inches(2.7), Inches(0.85), "3", "CALIBRATED SCREEN TESTS", ACCENT_GREEN)
    create_metric_tile(s3, Inches(3.7), Inches(6.05), Inches(2.7), Inches(0.85), "10°", "CENTRAL MACULAR GUARD", ACCENT_CYAN)
    create_metric_tile(s3, Inches(6.8), Inches(6.05), Inches(2.7), Inches(0.85), "Turn 2", "SAFETY CIRCUIT BREAKER", ACCENT_RED)
    create_metric_tile(s3, Inches(9.7), Inches(6.05), Inches(2.8), Inches(0.85), "100%", "SCREEN HARDWARE AGNOSTIC", ACCENT_BLUE)

    # =========================================================================
    # SLIDE 4: INTERACTIVE VISUAL PERCEPTION SIMULATOR
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    paint_background(s4)
    add_top_nav(s4, "Interactive Visual Perception Simulator", "Retail Psychology & Optical Physics", "04")

    # Left Column: The Problem & Simulator Architecture
    card4_l = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(4.35))
    card4_l.fill.solid()
    card4_l.fill.fore_color.rgb = BG_CARD
    card4_l.line.color.rgb = ACCENT_ORANGE
    card4_l.line.width = Pt(1.5)

    tx4_l = s4.shapes.add_textbox(Inches(1.05), Inches(1.68), Inches(5.1), Inches(4.0))
    tf4_l = tx4_l.text_frame
    tf4_l.word_wrap = True

    p = tf4_l.paragraphs[0]
    p.text = "SOLVING 'THE INVISIBLE PRODUCT DILEMMA'"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ORANGE
    p.space_after = Pt(8)

    sim_arch_points = [
        ("The Retail Bottleneck", "Ophthalmic lenses are transparent pieces of plastic. A ₹1,200 generic stock lens and a ₹8,000 ZEISS lens look identical to a walk-in patient."),
        ("Cognitive Skepticism", "Patients reject premium lenses because they cannot experience the optical physics prior to purchase."),
        ("Hardware-Accelerated Split View", "Engineered using CSS clip-path dynamically bound to a range slider at 60 FPS without heavy WebGL GPU overhead."),
        ("Interactive Touch Slider", "Patient drags the slider across the screen, revealing real-time before-and-after optical clarity on their own smartphone."),
        ("Retail Conversion Impact", "Bridges the gap between clinical recommendation and patient willingness-to-pay through experiential proof.")
    ]
    for t, d in sim_arch_points:
        p = tf4_l.add_paragraph()
        p.text = f"• {t}: "
        p.font.size = Pt(9.2)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(5)

    # Right Column: 4 Complaint-Driven Scenarios
    card4_r = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(4.35))
    card4_r.fill.solid()
    card4_r.fill.fore_color.rgb = BG_CARD
    card4_r.line.color.rgb = ACCENT_CYAN
    card4_r.line.width = Pt(1.5)

    tx4_r = s4.shapes.add_textbox(Inches(7.05), Inches(1.68), Inches(5.2), Inches(4.0))
    tf4_r = tx4_r.text_frame
    tf4_r.word_wrap = True

    p = tf4_r.paragraphs[0]
    p.text = "4 ANAMNESIS-DRIVEN REALISTIC SCENARIOS"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(8)

    scenarios = [
        ("DriveSafe Night Road", "Standard: Blinding LED high-beam starburst halo obscuring a roadside pedestrian. ZEISS DriveSafe: 64% glare attenuation reveals pedestrian & lane lines."),
        ("SmartLife Progressive", "Standard: Narrow 10mm reading corridor with lateral swim distortion and head strain. ZEISS SmartLife: Edge-to-edge panoramic reading zone."),
        ("BlueProtect Digital Screen", "Standard: 400–455nm high-energy blue scatter causing hazy low contrast and brow fatigue. ZEISS BlueProtect: Pitch-black text contrast."),
        ("ClearView Single Vision", "Standard: Spherical peripheral defocus and edge blur when looking sideways. ZEISS ClearView: 3× wider crystal-clear zone from center to margin."),
        ("Dynamic Auto-Selection", "Simulator automatically boots to the exact scenario matching the patient's self-reported chief complaint.")
    ]
    for t, d in scenarios:
        p = tf4_r.add_paragraph()
        p.text = f"✓ {t}: "
        p.font.size = Pt(9.2)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(4)

    # Bottom Metric Strip
    create_metric_tile(s4, Inches(0.8), Inches(6.05), Inches(2.7), Inches(0.85), "4", "DYNAMIC SCENARIO MODES", ACCENT_ORANGE)
    create_metric_tile(s4, Inches(3.7), Inches(6.05), Inches(2.7), Inches(0.85), "60 FPS", "SPLIT SLIDER RENDERING", ACCENT_GREEN)
    create_metric_tile(s4, Inches(6.8), Inches(6.05), Inches(2.7), Inches(0.85), "64%", "HEADLIGHT GLARE REDUCTION", ACCENT_CYAN)
    create_metric_tile(s4, Inches(9.7), Inches(6.05), Inches(2.8), Inches(0.85), "3×", "WIDER CLEARVIEW ZONE", ACCENT_BLUE)

    # =========================================================================
    # SLIDE 5: ZEISS RETAIL INTEROPERABILITY & PRACTICE HANDOVER
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    paint_background(s5)
    add_top_nav(s5, "ZEISS VISUCONSULT 500 Interoperability & Slip", "Ecosystem Integration", "05")

    # Left Column: VISUCONSULT 500 QR & Printable Slip
    card5_l = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(4.35))
    card5_l.fill.solid()
    card5_l.fill.fore_color.rgb = BG_CARD
    card5_l.line.color.rgb = ACCENT_BLUE
    card5_l.line.width = Pt(1.5)

    tx5_l = s5.shapes.add_textbox(Inches(1.05), Inches(1.68), Inches(5.1), Inches(4.0))
    tf5_l = tx5_l.text_frame
    tf5_l.word_wrap = True

    p = tf5_l.paragraphs[0]
    p.text = "ZEISS VISUCONSULT 500 DIGITAL BRIDGE"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    p.space_after = Pt(8)

    interop_points = [
        ("Pure-Python Vector SVG QR Generator", "Generates compact vector QR codes offline without external cloud dependencies, encoding patient anamnesis and screening."),
        ("Practice iPad Scanning", "Optometrist scans the QR with VISUCONSULT 500 iPad camera, instantly loading refraction parameters, corridor lengths, and coating tiers."),
        ("Sanitized Printable Optical Slip", "HTML5 print layout (@media print) generates standard 80mm thermal receipt slips or A4 PDFs with optometrist sign-off block."),
        ("Progressive Adaptation Risk (0–100)", "Quantifies non-adaptation risk based on age, cylinder, and working posture, recommending 14mm short vs 18mm standard corridor."),
        ("TBUT Tear-Film Warning", "Alerts practitioner to dry eye tear-film breakup before prescribing reading addition for female presbyopes.")
    ]
    for t, d in interop_points:
        p = tf5_l.add_paragraph()
        p.text = f"• {t}: "
        p.font.size = Pt(9.2)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(5)

    # Right Column: Emerging Market Ergonomics
    card5_r = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(4.35))
    card5_r.fill.solid()
    card5_r.fill.fore_color.rgb = BG_CARD
    card5_r.line.color.rgb = ACCENT_CYAN
    card5_r.line.width = Pt(1.5)

    tx5_r = s5.shapes.add_textbox(Inches(7.05), Inches(1.68), Inches(5.2), Inches(4.0))
    tf5_r = tx5_r.text_frame
    tf5_r.word_wrap = True

    p = tf5_r.paragraphs[0]
    p.text = "ZEISS PORTFOLIO & EMERGING MARKET LOGIC"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(8)

    market_points = [
        ("Two-Wheeler Transit Safety", "Recognizes motorcycle/scooter commute vector; escalates to 1.60 Shatterproof Polycarbonate / Trivex (ANSI Z87.1 road protection)."),
        ("Sports Impact Protection", "Ball/racket sports trigger high-impact polycarbonate; water activities trigger SkyPol polarized lenses; cycling triggers PhotoFusion X."),
        ("OfficeLens Focal Ergonomics", "Maps occupational posture to Maximum Intermediate Distance (M.I.D.): Book (100cm), Desk (200cm), Room (400cm)."),
        ("Contact Lens Routine Intelligence", "Detects contact lens fatigue and evening dry-eye, recommending backup glasses and re-wetting drops."),
        ("DuraVision Coating Selection", "Platinum for durability; BlueProtect for heavy digital work; DriveSafe for night road reflection.")
    ]
    for t, d in market_points:
        p = tf5_r.add_paragraph()
        p.text = f"✓ {t}: "
        p.font.size = Pt(9.2)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(5)

    # Bottom Metric Strip
    create_metric_tile(s5, Inches(0.8), Inches(6.05), Inches(2.7), Inches(0.85), "1-Click", "VISUCONSULT 500 QR BRIDGE", ACCENT_BLUE)
    create_metric_tile(s5, Inches(3.7), Inches(6.05), Inches(2.7), Inches(0.85), "80mm / A4", "THERMAL & PRINT SLIP", ACCENT_CYAN)
    create_metric_tile(s5, Inches(6.8), Inches(6.05), Inches(2.7), Inches(0.85), "0–100", "ADAPTATION RISK SCORE", ACCENT_GREEN)
    create_metric_tile(s5, Inches(9.7), Inches(6.05), Inches(2.8), Inches(0.85), "ANSI Z87.1", "ROAD & SPORTS SAFETY", ACCENT_CYAN)

    # =========================================================================
    # SLIDE 6: TECH STACK, RED TEAM SECURITY, IMPACT & ROADMAP
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    paint_background(s6)
    add_top_nav(s6, "Full Tech Stack, Red Team Hardening & Roadmap", "Production Readiness & Verification", "06")

    # Left Column: Full Tech Stack & Security
    card6_l = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(4.35))
    card6_l.fill.solid()
    card6_l.fill.fore_color.rgb = BG_CARD
    card6_l.line.color.rgb = ACCENT_GREEN
    card6_l.line.width = Pt(1.5)

    tx6_l = s6.shapes.add_textbox(Inches(1.05), Inches(1.68), Inches(5.1), Inches(4.0))
    tf6_l = tx6_l.text_frame
    tf6_l.word_wrap = True

    p = tf6_l.paragraphs[0]
    p.text = "FULL TECH STACK & RED TEAM HARDENING"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(8)

    tech_points = [
        ("Core Stack", "Python 3.12, FastAPI 0.110+, Pydantic v2 (Rust-backed validation), Uvicorn async ASGI. Total RAM footprint < 120 MB."),
        ("Frontend & Speech", "Zero-Framework Vanilla HTML5/CSS3/ES6+ (<180 KB payload), W3C Web Speech API + gTTS server-side audio fallback."),
        ("5-Iteration Red Team Hardening", "Tested XSS injection, 8-thread concurrent race conditions, audio fuzzing, and invalid options. Patched XSS via html.escape; whitelisted screening inputs."),
        ("Stochastic Monte Carlo Testing", "100 stochastic simulated runs across all ages, genders, and languages with zero deadlocks and 100% completion."),
        ("85 / 85 Automated Tests", "Comprehensive pytest test suite covering unit logic, API contracts, speech pipelines, and security attacks in 4.06 seconds.")
    ]
    for t, d in tech_points:
        p = tf6_l.add_paragraph()
        p.text = f"• {t}: "
        p.font.size = Pt(9.2)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(5)

    # Right Column: Live Deployment & Roadmap
    card6_r = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(4.35))
    card6_r.fill.solid()
    card6_r.fill.fore_color.rgb = BG_CARD
    card6_r.line.color.rgb = ACCENT_CYAN
    card6_r.line.width = Pt(1.5)

    tx6_r = s6.shapes.add_textbox(Inches(7.05), Inches(1.68), Inches(5.2), Inches(4.0))
    tf6_r = tx6_r.text_frame
    tf6_r.word_wrap = True

    p = tf6_r.paragraphs[0]
    p.text = "DEPLOYMENT, REPOSITORY & ROADMAP"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(8)

    roadmap_points = [
        ("Live Demonstration Access", "Equipped with 1-click Cloudflare Quick Tunnel (share_nayanee.bat) for zero-config public HTTPS testing on judges' mobile phones."),
        ("Production PWA Kiosk", "Service Worker (sw.js) + Web Manifest (manifest.json) for 1-tap installation on Android/iPad clinic reception counters."),
        ("Near-Term Roadmap (2–4 wks)", "On-device Vosk WebAssembly speech recognition for 100% offline rural camps; optometrist dim-room dark mode."),
        ("Major Roadmap (3–6 mos)", "OpenCV WebAssembly selfie-camera pupillometry (monocular PD & seg-height) with credit-card scaling; ABDM/FHIR locker sync."),
        ("Open Source Repository", "Clean, documented, production-ready codebase with CI automation: github.com/Satish8460/Nayanee.")
    ]
    for t, d in roadmap_points:
        p = tf6_r.add_paragraph()
        p.text = f"✓ {t}: "
        p.font.size = Pt(9.2)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(5)

    # Bottom Metric Strip
    create_metric_tile(s6, Inches(0.8), Inches(6.05), Inches(2.7), Inches(0.85), "85 / 85", "CI TEST SUITE PASSING", ACCENT_GREEN)
    create_metric_tile(s6, Inches(3.7), Inches(6.05), Inches(2.7), Inches(0.85), "4.06s", "TEST EXECUTION TIME", ACCENT_CYAN)
    create_metric_tile(s6, Inches(6.8), Inches(6.05), Inches(2.7), Inches(0.85), "5 Cycles", "RED TEAM SECURITY AUDIT", ACCENT_BLUE)
    create_metric_tile(s6, Inches(9.7), Inches(6.05), Inches(2.8), Inches(0.85), "Open Source", "GITHUB.COM/SATISH8460/NAYANEE", ACCENT_CYAN)

    # Save to disk
    for out_p in output_paths:
        try:
            prs.save(out_p)
            print(f"✨ Successfully generated 6-slide final presentation: {out_p}")
        except PermissionError:
            print(f"⚠️ Could not write to {out_p} (file in use).")


if __name__ == "__main__":
    build_final_6_slide_deck()
