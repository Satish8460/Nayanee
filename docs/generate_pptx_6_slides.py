"""Generates an executive-grade, visually polished 6-slide widescreen (.pptx) presentation
for Nayanee — ZEISS Hackathon Final Submission.
Team: Group Coders | Satish SM, Tejaswini C B | BMSIT
Themes: Theme 2 (No-Device Vision Intelligence) & Theme 1 (AFI)

LIGHT THEME & EXECUTIVE CLINICAL TYPOGRAPHY SYSTEM:
- Background: Soft Pristine Slate-White (#F4F6FA)
- Cards: Pure Crisp White (#FFFFFF) with Elegant Subtle Borders (#CBD5E1)
- Accents: ZEISS Cobalt (#0052CC), Emerald Clinical (#00875A), Crimson (#DE350B), Amber (#D97706)
- Typography: Segoe UI, Deep Charcoal (#091E42) for Titles, Slate (#334155) for Body
- Visual Hierarchy: Generous spacing, filled card proportions, zero empty voids
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE


def build_final_6_slide_deck(output_paths: list = None):
    if output_paths is None:
        output_paths = [
            "docs/Nayanee_Final_Presentation_Coders_6_Slides_Light.pptx",
            "docs/Nayanee_Final_Presentation_Coders_6_Slides.pptx",
            "docs/Nayanee_Final_Presentation_Coders_6_Slides_v2.pptx",
        ]
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Executive Light Medical/Clinical Palette
    BG_CANVAS = RGBColor(244, 246, 250)    # #F4F6FA (Crisp executive background)
    BG_CARD = RGBColor(255, 255, 255)      # #FFFFFF (Pristine White Card)
    BORDER_DEFAULT = RGBColor(205, 215, 228)# #CDD7E4 (Subtle Card Border)

    # High-Authority Brand & Clinical Accents
    ZEISS_BLUE = RGBColor(0, 82, 204)      # #0052CC (ZEISS Optical Blue)
    ZEISS_DARK = RGBColor(9, 30, 66)       # #091E42 (Deep Pitch Charcoal Navy)
    ACCENT_GREEN = RGBColor(0, 135, 90)    # #00875A (Clinical Health Green)
    ACCENT_RED = RGBColor(222, 53, 11)     # #DE350B (Triage Alert Crimson)
    ACCENT_AMBER = RGBColor(217, 119, 6)   # #D97706 (Glare Amber)
    ACCENT_TEAL = RGBColor(0, 141, 165)    # #008DA5 (Screener Cyan-Teal)

    # Typography Colors
    TEXT_HEAD = RGBColor(9, 30, 66)        # #091E42 (Sharp Headline Black-Navy)
    TEXT_TITLE_SUB = RGBColor(0, 82, 204)  # #0052CC (ZEISS Blue Accent)
    TEXT_BOLD = RGBColor(23, 43, 77)       # #172B4D (Deep Readable Charcoal)
    TEXT_BODY = RGBColor(71, 85, 105)      # #475569 (Medium Slate Gray)
    TEXT_MUTED = RGBColor(100, 116, 139)   # #64748B (Muted Metadata)
    PILL_BG = RGBColor(235, 242, 255)      # #EBF2FF (Soft Ice Blue Pill)
    PILL_BORDER = RGBColor(179, 212, 255)  # #B3D4FF

    def paint_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_CANVAS
        bg.line.fill.background()
        return bg

    def add_top_nav(slide, title_text, category_pill, slide_num, total_slides="06", presenter_sub=None):
        # Header Box
        tx = slide.shapes.add_textbox(Inches(0.7), Inches(0.35), Inches(8.8), Inches(1.15))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_sub = tf.paragraphs[0]
        if presenter_sub:
            p_sub.text = presenter_sub
        else:
            p_sub.text = "NAYANEE (ನಯनी) • ZEISS HACKATHON FINAL SUBMISSION  |  GROUP CODERS (BMSIT)"
        p_sub.font.size = Pt(12.5)
        p_sub.font.bold = True
        p_sub.font.color.rgb = TEXT_TITLE_SUB
        p_sub.space_after = Pt(2)

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(28)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_HEAD

        # Pill Tag (Top Right)
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.2), Inches(0.42), Inches(3.45), Inches(0.55))
        pill.fill.solid()
        pill.fill.fore_color.rgb = PILL_BG
        pill.line.color.rgb = PILL_BORDER
        pill.line.width = Pt(1.5)
        tf_p = pill.text_frame
        p_p = tf_p.paragraphs[0]
        p_p.text = category_pill
        p_p.font.size = Pt(12.5)
        p_p.font.bold = True
        p_p.font.color.rgb = ZEISS_BLUE
        p_p.alignment = PP_ALIGN.CENTER

        # Slide Number
        num_box = slide.shapes.add_textbox(Inches(10.8), Inches(7.05), Inches(1.8), Inches(0.35))
        tf_n = num_box.text_frame
        p_n = tf_n.paragraphs[0]
        p_n.text = f"{slide_num} / {total_slides}"
        p_n.font.size = Pt(12.0)
        p_n.font.bold = True
        p_n.font.color.rgb = TEXT_MUTED
        p_n.alignment = PP_ALIGN.RIGHT

    def create_metric_tile(slide, left, top, width, height, stat_value, stat_label, accent_color=ZEISS_BLUE):
        tile = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        tile.fill.solid()
        tile.fill.fore_color.rgb = BG_CARD
        tile.line.color.rgb = BORDER_DEFAULT
        tile.line.width = Pt(1.5)

        tx = slide.shapes.add_textbox(left, top + Inches(0.08), width, height - Inches(0.12))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = stat_value
        p1.font.size = Pt(27)
        p1.font.bold = True
        p1.font.color.rgb = accent_color
        p1.alignment = PP_ALIGN.CENTER

        p2 = tf.add_paragraph()
        p2.text = stat_label
        p2.font.size = Pt(10.5)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_MUTED
        p2.alignment = PP_ALIGN.CENTER

    card_top = Inches(1.55)
    card_h = Inches(4.3)
    card_w = Inches(5.8)
    col1_l = Inches(0.7)
    col2_l = Inches(6.8)
    m_top = Inches(5.95)
    m_w = Inches(2.8)
    m_h = Inches(0.95)

    # =========================================================================
    # SLIDE 1: EXECUTIVE VISION — THE RURAL & RETAIL OPTICAL DILEMMA
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    paint_background(s1)
    add_top_nav(s1, "No-Device Vision Intelligence for Walk-In Retail", "Theme 2 (Primary) & Theme 1 (AFI)", "01",
                presenter_sub="NAYANEE (ನಯनी)  •  PRESENTED BY GROUP CODERS: SATISH SM, TEJASWINI C B (BMSIT)")

    # Left Column: The Problem Card
    left_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, col1_l, card_top, card_w, card_h)
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = BG_CARD
    left_card.line.color.rgb = ACCENT_RED
    left_card.line.width = Pt(2.0)

    tx_l = s1.shapes.add_textbox(col1_l + Inches(0.28), card_top + Inches(0.22), card_w - Inches(0.56), card_h - Inches(0.4))
    tf_l = tx_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "THE RURAL & RETAIL OPTICAL DILEMMA"
    p.font.size = Pt(16.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED
    p.space_after = Pt(12)

    problems = [
        ("Zero Hardware Capex", "Small clinics & retail stores cannot afford $15,000 autorefractors—just a phone or a front counter."),
        ("24-Question Survey Fatigue", "Static lifestyle surveys (e.g. ZEISS Vision Profile) suffer >40% drop-off due to tedious multi-slider forms."),
        ("Language & Literacy Divide", "Over 85% of Indian walk-in patients speak regional Indic languages; English intake forms alienate them."),
        ("Commercial Red-Flag Blindness", "Commercial questionnaires focus only on selling lenses, ignoring acute retinal tears or glaucoma emergencies.")
    ]
    for title, desc in problems:
        p = tf_l.add_paragraph()
        p.text = f"✕  {title}: "
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_BOLD

        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(10)

    # Right Column: The Nayanee Solution Card
    right_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, col2_l, card_top, card_w, card_h)
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = BG_CARD
    right_card.line.color.rgb = ACCENT_GREEN
    right_card.line.width = Pt(2.0)

    tx_r = s1.shapes.add_textbox(col2_l + Inches(0.28), card_top + Inches(0.22), card_w - Inches(0.56), card_h - Inches(0.4))
    tf_r = tx_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "THE NAYANEE BREAKTHROUGH (AFI ETHOS)"
    p.font.size = Pt(16.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(12)

    solutions = [
        ("Zero Hardware Dependency", "Captures complete functional vision demands on any commodity ₹6,000 Android smartphone or tablet."),
        ("6 Native Indic Languages", "Communicates naturally via voice in Kannada, Hindi, Tamil, Telugu, Malayalam, and English with audio narration."),
        ("Active Bayesian Adaptiveness", "Information-theoretic engine cuts intake by 67% (7–8 questions in <90s vs 24 questions in 7–10 minutes)."),
        ("Deterministic Clinical Safety", "Hardcoded acute red-flag sentinel halts on emergency symptoms with zero hallucination and direct hospital triage.")
    ]
    for title, desc in solutions:
        p = tf_r.add_paragraph()
        p.text = f"✓  {title}: "
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_BOLD

        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(10)

    # Bottom Metric Strip
    create_metric_tile(s1, Inches(0.7), m_top, m_w, m_h, "$0", "HARDWARE EQUIPMENT CAPEX", ACCENT_GREEN)
    create_metric_tile(s1, Inches(3.73), m_top, m_w, m_h, "6", "NATIVE INDIC LANGUAGES", ZEISS_BLUE)
    create_metric_tile(s1, Inches(6.8), m_top, m_w, m_h, "< 90s", "INTAKE COMPLETION TIME", ZEISS_BLUE)
    create_metric_tile(s1, Inches(9.83), m_top, m_w, m_h, "100%", "ZERO-GPU CPU EXECUTION", ZEISS_BLUE)

    # =========================================================================
    # SLIDE 2: MATHEMATICAL INNOVATION — ACTIVE BAYESIAN ANAMNESIS
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    paint_background(s2)
    add_top_nav(s2, "Active Bayesian Inference & Adaptive Anamnesis", "Algorithmic Innovation", "02")

    # Left Column: Mathematical Formulation
    card2_l = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, col1_l, card_top, card_w, card_h)
    card2_l.fill.solid()
    card2_l.fill.fore_color.rgb = BG_CARD
    card2_l.line.color.rgb = ZEISS_BLUE
    card2_l.line.width = Pt(2.0)

    tx2_l = s2.shapes.add_textbox(col1_l + Inches(0.28), card_top + Inches(0.22), card_w - Inches(0.56), card_h - Inches(0.4))
    tf2_l = tx2_l.text_frame
    tf2_l.word_wrap = True

    p = tf2_l.paragraphs[0]
    p.text = "ACTIVE INFERENCE & INFORMATION GAIN"
    p.font.size = Pt(16.5)
    p.font.bold = True
    p.font.color.rgb = ZEISS_BLUE
    p.space_after = Pt(12)

    math_points = [
        ("Domain Uncertainty Vector", "Tracks remaining entropy U(D) in [0.0, 1.0] across 6 clinical axes: Distance, Near, Screen, Lifestyle, Eyewear, Red-Flag."),
        ("InfoGain Ranking Equation", "Dynamically scores candidate questions at every turn: InfoGain(q) = W_base(q) × U(D_q) × B_chief × B_age × B_gender."),
        ("Physiological Age & Gender Priors", "Age ≥40 boosts Near domain (1.25×); Female ≥40 boosts dry-eye risk (1.25×) and shorter forearm reach (33cm)."),
        ("Entropy Decay Queue", "Recorded answers consume domain entropy (U(D) ← U(D) - 0.55 × W_base), naturally pivoting without brittle decision trees.")
    ]
    for t, d in math_points:
        p = tf2_l.add_paragraph()
        p.text = f"• {t}: "
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_BOLD
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(10)

    # Right Column: Pruning & Consistency
    card2_r = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, col2_l, card_top, card_w, card_h)
    card2_r.fill.solid()
    card2_r.fill.fore_color.rgb = BG_CARD
    card2_r.line.color.rgb = ZEISS_BLUE
    card2_r.line.width = Pt(2.0)

    tx2_r = s2.shapes.add_textbox(col2_l + Inches(0.28), card_top + Inches(0.22), card_w - Inches(0.56), card_h - Inches(0.4))
    tf2_r = tx2_r.text_frame
    tf2_r.word_wrap = True

    p = tf2_r.paragraphs[0]
    p.text = "TREE PRUNING & CONTRADICTION SENTINEL"
    p.font.size = Pt(16.5)
    p.font.bold = True
    p.font.color.rgb = ZEISS_BLUE
    p.space_after = Pt(12)

    pruning_points = [
        ("Conditional Tree Pruning", "Selecting 'never_worn' instantly prunes glasses age, satisfaction, and contact lens routine questions."),
        ("Prerequisite Gating", "Contact lens wear time and dry-eye routine questions only appear if the patient explicitly wears contact lenses."),
        ("Real-Time Contradiction Matrix", "Detects cognitive conflicts (e.g. reporting near reading blur but zero strain, or 'never worn' but 2yo glasses)."),
        ("67% Question Reduction", "Averages 7.2 questions (under 90s) vs 24 questions (7–10m) in ZEISS Vision Profile without clinical depth loss.")
    ]
    for t, d in pruning_points:
        p = tf2_r.add_paragraph()
        p.text = f"✓ {t}: "
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_BOLD
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(10)

    # Bottom Metric Strip
    create_metric_tile(s2, Inches(0.7), m_top, m_w, m_h, "7.2", "AVG QUESTIONS ASKED", ZEISS_BLUE)
    create_metric_tile(s2, Inches(3.73), m_top, m_w, m_h, "< 2 ms", "INFERENCE TURN LATENCY", ACCENT_GREEN)
    create_metric_tile(s2, Inches(6.8), m_top, m_w, m_h, "67%", "REDUCTION VS 24-QN FORMS", ZEISS_BLUE)
    create_metric_tile(s2, Inches(9.83), m_top, m_w, m_h, "100%", "DETERMINISTIC SAFETY", ZEISS_BLUE)

    # =========================================================================
    # SLIDE 3: ZERO-HARDWARE CLINICAL SCREENING SUITE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    paint_background(s3)
    add_top_nav(s3, "Zero-Hardware Refractive & Macular Screening Suite", "Device-Free Triaging", "03")

    # Left Column: 3 Screen Tests
    card3_l = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, col1_l, card_top, card_w, card_h)
    card3_l.fill.solid()
    card3_l.fill.fore_color.rgb = BG_CARD
    card3_l.line.color.rgb = ACCENT_GREEN
    card3_l.line.width = Pt(2.0)

    tx3_l = s3.shapes.add_textbox(col1_l + Inches(0.28), card_top + Inches(0.22), card_w - Inches(0.56), card_h - Inches(0.4))
    tf3_l = tx3_l.text_frame
    tf3_l.word_wrap = True

    p = tf3_l.paragraphs[0]
    p.text = "3 CALIBRATED ON-SCREEN TESTS"
    p.font.size = Pt(16.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(12)

    tests_points = [
        ("Red-Green Duochrome Test", "Evaluates longitudinal chromatic aberration (650nm Red vs 535nm Green). Red clearer indicates myopia; Green clearer indicates hyperopia/over-minusing."),
        ("Astigmatic Clock Dial", "Visualizes the Conoid of Sturm at 30° radial meridians on Retina/OLED displays, identifying dominant cylinder axis for JCC refinement."),
        ("Amsler Grid Macular Guard", "Evaluates central 10° of visual field. Detects metamorphopsia (wavy lines) or scotomas (blind spots), flagging macular edema or AMD."),
        ("Screen Agnostic Calibration", "Pure HTML5 Canvas and CSS responsive vector rendering; works on any mobile screen without specialized hardware calibration tools.")
    ]
    for t, d in tests_points:
        p = tf3_l.add_paragraph()
        p.text = f"• {t}: "
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_BOLD
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(10)

    # Right Column: Acute Red-Flag Emergency Sentinel
    card3_r = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, col2_l, card_top, card_w, card_h)
    card3_r.fill.solid()
    card3_r.fill.fore_color.rgb = BG_CARD
    card3_r.line.color.rgb = ACCENT_RED
    card3_r.line.width = Pt(2.0)

    tx3_r = s3.shapes.add_textbox(col2_l + Inches(0.28), card_top + Inches(0.22), card_w - Inches(0.56), card_h - Inches(0.4))
    tf3_r = tx3_r.text_frame
    tf3_r.word_wrap = True

    p = tf3_r.paragraphs[0]
    p.text = "TURN-2 INVARIANT EMERGENCY CIRCUIT BREAKER"
    p.font.size = Pt(16.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED
    p.space_after = Pt(12)

    safety_points = [
        ("Invariant Turn-2 Trigger", "Every patient is probed for acute red flags on Turn 2: sudden vision loss, severe unilateral ocular pain, or flashes/floaters."),
        ("Instant Triage Halt", "If an acute red flag is reported, the session halts immediately. It does NOT waste critical time asking about reading distance or sunglasses."),
        ("Emergency Status Escalation", "Flips state to URGENT MEDICAL TRIAGE, warning the patient of retinal tear or angle-closure glaucoma risks."),
        ("Zero Hallucination Guarantee", "Deterministic state machine; generates an emergency ophthalmology pass and never dispenses glasses when pathology is suspected.")
    ]
    for t, d in safety_points:
        p = tf3_r.add_paragraph()
        p.text = f"✓ {t}: "
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_BOLD
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(10)

    # Bottom Metric Strip
    create_metric_tile(s3, Inches(0.7), m_top, m_w, m_h, "3", "CALIBRATED SCREEN TESTS", ACCENT_GREEN)
    create_metric_tile(s3, Inches(3.73), m_top, m_w, m_h, "10°", "CENTRAL MACULAR GUARD", ACCENT_TEAL)
    create_metric_tile(s3, Inches(6.8), m_top, m_w, m_h, "Turn 2", "SAFETY CIRCUIT BREAKER", ACCENT_RED)
    create_metric_tile(s3, Inches(9.83), m_top, m_w, m_h, "100%", "SCREEN HARDWARE AGNOSTIC", ZEISS_BLUE)

    # =========================================================================
    # SLIDE 4: INTERACTIVE VISUAL PERCEPTION SIMULATOR
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    paint_background(s4)
    add_top_nav(s4, "Interactive Visual Perception Simulator", "Retail Psychology & Optical Physics", "04")

    # Left Column: The Problem & Simulator Architecture
    card4_l = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, col1_l, card_top, card_w, card_h)
    card4_l.fill.solid()
    card4_l.fill.fore_color.rgb = BG_CARD
    card4_l.line.color.rgb = ACCENT_AMBER
    card4_l.line.width = Pt(2.0)

    tx4_l = s4.shapes.add_textbox(col1_l + Inches(0.28), card_top + Inches(0.22), card_w - Inches(0.56), card_h - Inches(0.4))
    tf4_l = tx4_l.text_frame
    tf4_l.word_wrap = True

    p = tf4_l.paragraphs[0]
    p.text = "SOLVING 'THE INVISIBLE PRODUCT DILEMMA'"
    p.font.size = Pt(16.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER
    p.space_after = Pt(12)

    sim_arch_points = [
        ("The Retail Bottleneck", "Ophthalmic lenses are transparent pieces of plastic. A ₹1,200 generic stock lens and a ₹8,000 ZEISS lens look identical to a walk-in patient."),
        ("Cognitive Skepticism", "Patients reject premium lenses because they cannot physically experience the optical physics prior to purchase."),
        ("Hardware-Accelerated Split View", "Engineered using CSS clip-path dynamically bound to a range slider at 60 FPS without heavy WebGL GPU overhead."),
        ("Experiential Conversion", "Patient drags the slider across the screen, revealing real-time before-and-after optical clarity on their own smartphone.")
    ]
    for t, d in sim_arch_points:
        p = tf4_l.add_paragraph()
        p.text = f"• {t}: "
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_BOLD
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(10)

    # Right Column: 4 Complaint-Driven Scenarios
    card4_r = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, col2_l, card_top, card_w, card_h)
    card4_r.fill.solid()
    card4_r.fill.fore_color.rgb = BG_CARD
    card4_r.line.color.rgb = ZEISS_BLUE
    card4_r.line.width = Pt(2.0)

    tx4_r = s4.shapes.add_textbox(col2_l + Inches(0.28), card_top + Inches(0.22), card_w - Inches(0.56), card_h - Inches(0.4))
    tf4_r = tx4_r.text_frame
    tf4_r.word_wrap = True

    p = tf4_r.paragraphs[0]
    p.text = "4 ANAMNESIS-DRIVEN REALISTIC SCENARIOS"
    p.font.size = Pt(16.5)
    p.font.bold = True
    p.font.color.rgb = ZEISS_BLUE
    p.space_after = Pt(12)

    scenarios = [
        ("DriveSafe Night Road", "Standard: Blinding LED high-beam starburst halo obscuring a roadside pedestrian. ZEISS DriveSafe: 64% glare attenuation reveals pedestrian & lane lines."),
        ("SmartLife Progressive", "Standard: Narrow 10mm reading corridor with lateral swim distortion and head strain. ZEISS SmartLife: Edge-to-edge panoramic reading zone."),
        ("BlueProtect Digital Screen", "Standard: 400–455nm blue scatter causing hazy low contrast and brow fatigue. ZEISS BlueProtect: Pitch-black text contrast & eye strain relief."),
        ("ClearView Single Vision", "Standard: Spherical peripheral defocus and edge blur when looking sideways. ZEISS ClearView: 3× wider crystal-clear zone from center to margin.")
    ]
    for t, d in scenarios:
        p = tf4_r.add_paragraph()
        p.text = f"✓ {t}: "
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_BOLD
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(10)

    # Bottom Metric Strip
    create_metric_tile(s4, Inches(0.7), m_top, m_w, m_h, "4", "DYNAMIC SCENARIO MODES", ACCENT_AMBER)
    create_metric_tile(s4, Inches(3.73), m_top, m_w, m_h, "60 FPS", "SPLIT SLIDER RENDERING", ACCENT_GREEN)
    create_metric_tile(s4, Inches(6.8), m_top, m_w, m_h, "64%", "HEADLIGHT GLARE REDUCTION", ZEISS_BLUE)
    create_metric_tile(s4, Inches(9.83), m_top, m_w, m_h, "3×", "WIDER CLEARVIEW ZONE", ZEISS_BLUE)

    # =========================================================================
    # SLIDE 5: ZEISS RETAIL INTEROPERABILITY & PRACTICE HANDOVER
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    paint_background(s5)
    add_top_nav(s5, "ZEISS VISUCONSULT 500 Interoperability & Slip", "Ecosystem Integration", "05")

    # Left Column: VISUCONSULT 500 QR & Printable Slip
    card5_l = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, col1_l, card_top, card_w, card_h)
    card5_l.fill.solid()
    card5_l.fill.fore_color.rgb = BG_CARD
    card5_l.line.color.rgb = ZEISS_BLUE
    card5_l.line.width = Pt(2.0)

    tx5_l = s5.shapes.add_textbox(col1_l + Inches(0.28), card_top + Inches(0.22), card_w - Inches(0.56), card_h - Inches(0.4))
    tf5_l = tx5_l.text_frame
    tf5_l.word_wrap = True

    p = tf5_l.paragraphs[0]
    p.text = "ZEISS VISUCONSULT 500 DIGITAL BRIDGE"
    p.font.size = Pt(16.5)
    p.font.bold = True
    p.font.color.rgb = ZEISS_BLUE
    p.space_after = Pt(12)

    interop_points = [
        ("Pure-Python Vector SVG QR Generator", "Generates compact vector QR codes offline without external cloud dependencies, encoding patient anamnesis and screening."),
        ("Practice iPad Scanning", "Optometrist scans the QR with VISUCONSULT 500 iPad camera, instantly loading refraction parameters, corridor lengths, and coating tiers."),
        ("Sanitized Printable Optical Slip", "HTML5 print layout (@media print) generates standard 80mm thermal receipt slips or A4 PDFs with optometrist sign-off block."),
        ("Progressive Adaptation Risk (0–100)", "Quantifies non-adaptation risk based on age, cylinder, and working posture, recommending 14mm short vs 18mm standard corridor.")
    ]
    for t, d in interop_points:
        p = tf5_l.add_paragraph()
        p.text = f"• {t}: "
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_BOLD
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(10)

    # Right Column: Emerging Market Ergonomics
    card5_r = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, col2_l, card_top, card_w, card_h)
    card5_r.fill.solid()
    card5_r.fill.fore_color.rgb = BG_CARD
    card5_r.line.color.rgb = ZEISS_BLUE
    card5_r.line.width = Pt(2.0)

    tx5_r = s5.shapes.add_textbox(col2_l + Inches(0.28), card_top + Inches(0.22), card_w - Inches(0.56), card_h - Inches(0.4))
    tf5_r = tx5_r.text_frame
    tf5_r.word_wrap = True

    p = tf5_r.paragraphs[0]
    p.text = "ZEISS PORTFOLIO & EMERGING MARKET LOGIC"
    p.font.size = Pt(16.5)
    p.font.bold = True
    p.font.color.rgb = ZEISS_BLUE
    p.space_after = Pt(12)

    market_points = [
        ("Two-Wheeler Transit Safety", "Recognizes motorcycle/scooter commute vector; escalates to 1.60 Shatterproof Polycarbonate / Trivex (ANSI Z87.1 road protection)."),
        ("Sports Impact Protection", "Ball/racket sports trigger high-impact polycarbonate; water activities trigger SkyPol polarized lenses; cycling triggers PhotoFusion X."),
        ("OfficeLens Focal Ergonomics", "Maps occupational posture to Maximum Intermediate Distance (M.I.D.): Book (100cm), Desk (200cm), Room (400cm)."),
        ("Contact Lens Intelligence", "Detects contact lens fatigue and evening dry-eye, recommending backup glasses, re-wetting drops, and TBUT tear-film checks.")
    ]
    for t, d in market_points:
        p = tf5_r.add_paragraph()
        p.text = f"✓ {t}: "
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_BOLD
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(10)

    # Bottom Metric Strip
    create_metric_tile(s5, Inches(0.7), m_top, m_w, m_h, "1-Click", "VISUCONSULT 500 QR BRIDGE", ZEISS_BLUE)
    create_metric_tile(s5, Inches(3.73), m_top, m_w, m_h, "80mm / A4", "THERMAL & PRINT SLIP", ZEISS_BLUE)
    create_metric_tile(s5, Inches(6.8), m_top, m_w, m_h, "0–100", "ADAPTATION RISK SCORE", ACCENT_GREEN)
    create_metric_tile(s5, Inches(9.83), m_top, m_w, m_h, "ANSI Z87.1", "ROAD & SPORTS SAFETY", ZEISS_BLUE)

    # =========================================================================
    # SLIDE 6: TECH STACK, RED TEAM SECURITY, IMPACT & ROADMAP
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    paint_background(s6)
    add_top_nav(s6, "Full Tech Stack, Red Team Hardening & Roadmap", "Production Readiness & Verification", "06")

    # Left Column: Full Tech Stack & Security
    card6_l = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, col1_l, card_top, card_w, card_h)
    card6_l.fill.solid()
    card6_l.fill.fore_color.rgb = BG_CARD
    card6_l.line.color.rgb = ACCENT_GREEN
    card6_l.line.width = Pt(2.0)

    tx6_l = s6.shapes.add_textbox(col1_l + Inches(0.28), card_top + Inches(0.22), card_w - Inches(0.56), card_h - Inches(0.4))
    tf6_l = tx6_l.text_frame
    tf6_l.word_wrap = True

    p = tf6_l.paragraphs[0]
    p.text = "FULL TECH STACK & RED TEAM HARDENING"
    p.font.size = Pt(16.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(12)

    tech_points = [
        ("Core Stack", "Python 3.12, FastAPI 0.110+, Pydantic v2 (Rust-backed validation), Uvicorn async ASGI. Total RAM footprint < 120 MB."),
        ("Frontend & Speech", "Zero-Framework Vanilla HTML5/CSS3/ES6+ (<180 KB payload), W3C Web Speech API + gTTS server-side audio fallback."),
        ("5-Iteration Red Team Hardening", "Tested XSS injection, 8-thread concurrent race conditions, audio fuzzing, and invalid options. Patched XSS via html.escape; whitelisted screening inputs."),
        ("85 / 85 Automated Tests", "Comprehensive pytest test suite covering unit logic, API contracts, speech pipelines, and 100 stochastic Monte Carlo runs in 4.06 seconds.")
    ]
    for t, d in tech_points:
        p = tf6_l.add_paragraph()
        p.text = f"• {t}: "
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_BOLD
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(10)

    # Right Column: Live Deployment & Roadmap
    card6_r = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, col2_l, card_top, card_w, card_h)
    card6_r.fill.solid()
    card6_r.fill.fore_color.rgb = BG_CARD
    card6_r.line.color.rgb = ZEISS_BLUE
    card6_r.line.width = Pt(2.0)

    tx6_r = s6.shapes.add_textbox(col2_l + Inches(0.28), card_top + Inches(0.22), card_w - Inches(0.56), card_h - Inches(0.4))
    tf6_r = tx6_r.text_frame
    tf6_r.word_wrap = True

    p = tf6_r.paragraphs[0]
    p.text = "DEPLOYMENT, REPOSITORY & ROADMAP"
    p.font.size = Pt(16.5)
    p.font.bold = True
    p.font.color.rgb = ZEISS_BLUE
    p.space_after = Pt(12)

    roadmap_points = [
        ("Live Demonstration Access", "Equipped with 1-click Cloudflare Quick Tunnel (share_nayanee.bat) for zero-config public HTTPS testing on judges' mobile phones."),
        ("Production PWA Kiosk", "Service Worker (sw.js) + Web Manifest (manifest.json) for 1-tap installation on Android/iPad clinic reception counters."),
        ("Near-Term Roadmap (2–4 wks)", "On-device Vosk WebAssembly speech recognition for 100% offline rural camps; optometrist dim-room dark mode."),
        ("Major Roadmap (3–6 mos)", "OpenCV WebAssembly selfie-camera pupillometry (monocular PD & seg-height) with credit-card scaling; ABDM/FHIR locker sync.")
    ]
    for t, d in roadmap_points:
        p = tf6_r.add_paragraph()
        p.text = f"✓ {t}: "
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_BOLD
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(10)

    # Bottom Metric Strip
    create_metric_tile(s6, Inches(0.7), m_top, m_w, m_h, "85 / 85", "CI TEST SUITE PASSING", ACCENT_GREEN)
    create_metric_tile(s6, Inches(3.73), m_top, m_w, m_h, "4.06s", "TEST EXECUTION TIME", ZEISS_BLUE)
    create_metric_tile(s6, Inches(6.8), m_top, m_w, m_h, "5 Cycles", "RED TEAM SECURITY AUDIT", ZEISS_BLUE)
    create_metric_tile(s6, Inches(9.83), m_top, m_w, m_h, "Open Source", "GITHUB.COM/SATISH8460/NAYANEE", ZEISS_BLUE)

    # Save to disk
    for out_p in output_paths:
        try:
            prs.save(out_p)
            print(f"✨ Successfully generated light-theme presentation: {out_p}")
        except PermissionError:
            print(f"⚠️ Could not write to {out_p} (file in use).")


if __name__ == "__main__":
    build_final_6_slide_deck()
