"""Generates an executive-grade, visually polished 6-slide widescreen (.pptx) presentation
for Nayanee — ZEISS Hackathon Final Submission.
Team: Group Coders | Satish SM, Tejaswini C B | BMSIT
Themes: Theme 2 (No-Device Vision Intelligence) & Theme 1 (AFI)

ENHANCED PROPORTIONAL LAYOUT WITH PROMINENT FIGURES & COMPLETE TECHNICAL DEPTH:
- All figures explicitly labeled: Fig 1 to Fig 8 with clear clinical captions
- Enhanced 2x2 grid on Slide 3 so Duochrome, Astigmatic Dial, Amsler Grid, and Voice Waveform are large and prominent (3.1 in wide each, never diminished)
- Slide 2 features full-height Fig 2 (4.3 in wide) with complete Bayesian math & priors
- All important technical & clinical terms preserved verbatim
"""

import os
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE


def build_final_6_slide_deck(output_paths: list = None):
    if output_paths is None:
        output_paths = [
            "docs/Nayanee_Final_Presentation_Coders_6_Slides_v3.pptx",
            "docs/Nayanee_Final_Presentation_Coders_6_Slides_v2.pptx",
            "docs/Nayanee_Final_Presentation_Coders_6_Slides.pptx",
            "docs/Nayanee_Final_Presentation_Coders_6_Slides_Light.pptx",
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
        tx = slide.shapes.add_textbox(Inches(0.7), Inches(0.32), Inches(8.8), Inches(1.15))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_sub = tf.paragraphs[0]
        if presenter_sub:
            p_sub.text = presenter_sub
        else:
            p_sub.text = "NAYANEE (ನಯनी) • ZEISS HACKATHON FINAL SUBMISSION  |  GROUP CODERS (BMSIT)"
        p_sub.font.size = Pt(12.0)
        p_sub.font.bold = True
        p_sub.font.color.rgb = TEXT_TITLE_SUB
        p_sub.space_after = Pt(2)

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(27)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_HEAD

        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.2), Inches(0.38), Inches(3.45), Inches(0.52))
        pill.fill.solid()
        pill.fill.fore_color.rgb = PILL_BG
        pill.line.color.rgb = PILL_BORDER
        pill.line.width = Pt(1.5)
        tf_p = pill.text_frame
        p_p = tf_p.paragraphs[0]
        p_p.text = category_pill
        p_p.font.size = Pt(12.0)
        p_p.font.bold = True
        p_p.font.color.rgb = ZEISS_BLUE
        p_p.alignment = PP_ALIGN.CENTER

        num_box = slide.shapes.add_textbox(Inches(10.8), Inches(7.05), Inches(1.8), Inches(0.35))
        tf_n = num_box.text_frame
        p_n = tf_n.paragraphs[0]
        p_n.text = f"{slide_num} / {total_slides}"
        p_n.font.size = Pt(11.5)
        p_n.font.bold = True
        p_n.font.color.rgb = TEXT_MUTED
        p_n.alignment = PP_ALIGN.RIGHT

    def create_metric_tile(slide, left, top, width, height, stat_value, stat_label, accent_color=ZEISS_BLUE, link_url=None):
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
        p1.font.size = Pt(24 if len(stat_value) > 7 else 26)
        p1.font.bold = True
        p1.font.color.rgb = accent_color
        p1.alignment = PP_ALIGN.CENTER
        if link_url and len(p1.runs) > 0:
            p1.runs[0].hyperlink.address = link_url

        p2 = tf.add_paragraph()
        p2.text = stat_label
        p2.font.size = Pt(9.5 if len(stat_label) > 22 else 10.0)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_MUTED
        p2.alignment = PP_ALIGN.CENTER
        if link_url and len(p2.runs) > 0:
            p2.runs[0].hyperlink.address = link_url

    def add_framed_screenshot(slide, image_path, card_l, card_t, card_w, card_h, fig_title, border_color=ZEISS_BLUE, extra_note=None, sub_badge=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, card_l, card_t, card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        top_bar_h = Inches(0.32)
        tx_b = slide.shapes.add_textbox(card_l + Inches(0.08), card_t + Inches(0.06), card_w - Inches(0.16), top_bar_h)
        tf_b = tx_b.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
        p_b = tf_b.paragraphs[0]
        p_b.text = fig_title
        p_b.font.size = Pt(9.5)
        p_b.font.bold = True
        p_b.font.color.rgb = border_color
        p_b.alignment = PP_ALIGN.CENTER

        if sub_badge:
            p_sub = tf_b.add_paragraph()
            p_sub.text = sub_badge
            p_sub.font.size = Pt(8.0)
            p_sub.font.bold = True
            p_sub.font.color.rgb = TEXT_MUTED
            p_sub.alignment = PP_ALIGN.CENTER
            top_bar_h = Inches(0.46)

        with Image.open(image_path) as img:
            img_w, img_h = img.size

        note_space = Inches(0.38) if extra_note else Inches(0.0)
        top_offset = card_t + top_bar_h + Inches(0.06)
        max_w = card_w - Inches(0.2)
        max_h = card_h - top_bar_h - Inches(0.14) - note_space

        scale = min(max_w / img_w, max_h / img_h)
        target_w = int(img_w * scale)
        target_h = int(img_h * scale)

        pos_l = card_l + int((card_w - target_w) / 2)
        pos_t = top_offset + int((max_h - target_h) / 2)

        slide.shapes.add_picture(image_path, pos_l, pos_t, target_w, target_h)

        if extra_note:
            tx_n = slide.shapes.add_textbox(card_l + Inches(0.08), card_t + card_h - Inches(0.36), card_w - Inches(0.16), Inches(0.3))
            tf_n = tx_n.text_frame
            tf_n.word_wrap = True
            tf_n.margin_left = tf_n.margin_right = tf_n.margin_top = tf_n.margin_bottom = 0
            p_n = tf_n.paragraphs[0]
            p_n.text = extra_note
            p_n.font.size = Pt(8.5)
            p_n.font.bold = True
            p_n.font.color.rgb = TEXT_MUTED
            p_n.alignment = PP_ALIGN.CENTER

    card_top = Inches(1.52)
    card_h = Inches(4.35)
    m_top = Inches(5.95)
    m_w = Inches(2.8)
    m_h = Inches(0.95)

    # =========================================================================
    # SLIDE 1: EXECUTIVE VISION — THE RURAL & RETAIL OPTICAL DILEMMA
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    paint_background(s1)
    add_top_nav(s1, "No-Device Vision Intelligence for Walk-In Retail", "Theme 2 (Primary) & Theme 1 (AFI)", "01",
                presenter_sub="NAYANEE (ನಯनी)  •  GROUP CODERS: SATISH SM, TEJASWINI C B (BMSIT)  |  https://github.com/Satish8460/Nayanee")

    col1_w = Inches(6.4)
    left_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.7), card_top, col1_w, card_h)
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = BG_CARD
    left_card.line.color.rgb = ACCENT_RED
    left_card.line.width = Pt(2.0)

    tx_l = s1.shapes.add_textbox(Inches(0.95), card_top + Inches(0.2), col1_w - Inches(0.5), card_h - Inches(0.35))
    tf_l = tx_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "THE RURAL & RETAIL OPTICAL DILEMMA"
    p.font.size = Pt(16.0)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED
    p.space_after = Pt(10)

    problems = [
        ("Zero Hardware Equipment", "Small clinics & optical shops cannot afford $15,000 autorefractors—just a phone or front counter."),
        ("24-Question Survey Fatigue", "Static lifestyle surveys (e.g. ZEISS Vision Profile) suffer >40% drop-off due to tedious multi-slider forms."),
        ("Language & Literacy Barrier", "Over 85% of Indian walk-in patients speak regional Indic languages; English intake forms alienate them."),
        ("Commercial Red-Flag Blindness", "Commercial questionnaires focus only on selling lenses, ignoring acute retinal tears or glaucoma emergencies.")
    ]
    for title, desc in problems:
        p = tf_l.add_paragraph()
        p.text = f"✕  {title}: "
        p.font.size = Pt(13.0)
        p.font.bold = True
        p.font.color.rgb = TEXT_BOLD

        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(8)

    # Right Column: Fig 1 (Language Selection & Intake Kiosk)
    add_framed_screenshot(
        s1,
        "docs/assets/screenshots/01_language_intake.png",
        Inches(7.3),
        card_top,
        Inches(5.333),
        card_h,
        "Fig 1: Multi-Lingual Intake Kiosk (6 Indic Languages + Demographics)",
        border_color=ZEISS_BLUE,
        extra_note="Touch-First Kiosk: Kannada, Hindi, Tamil, Telugu, Malayalam & English"
    )

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

    col2_w = Inches(7.3)
    card2_l = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.7), card_top, col2_w, card_h)
    card2_l.fill.solid()
    card2_l.fill.fore_color.rgb = BG_CARD
    card2_l.line.color.rgb = ZEISS_BLUE
    card2_l.line.width = Pt(2.0)

    tx2_l = s2.shapes.add_textbox(Inches(0.95), card_top + Inches(0.2), col2_w - Inches(0.5), card_h - Inches(0.35))
    tf2_l = tx2_l.text_frame
    tf2_l.word_wrap = True

    p = tf2_l.paragraphs[0]
    p.text = "ACTIVE INFERENCE & BILINGUAL VOICE INPUT"
    p.font.size = Pt(16.0)
    p.font.bold = True
    p.font.color.rgb = ZEISS_BLUE
    p.space_after = Pt(10)

    math_points = [
        ("Domain Uncertainty Vector", "Tracks remaining entropy U(D) in [0.0, 1.0] across 6 clinical axes: Distance, Near, Screen, Lifestyle, Eyewear, Red-Flag."),
        ("InfoGain Ranking Equation", "Dynamically scores candidate questions at every turn: InfoGain(q) = W_base(q) × U(D_q) × B_chief × B_age × B_gender."),
        ("Physiological Age & Gender Priors", "Age ≥40 boosts Near domain (1.25×); Female ≥40 boosts dry-eye risk (1.25×) and shorter forearm reach (33cm)."),
        ("Tree Pruning & Contradiction Matrix", "Selecting 'never_worn' prunes 3 questions; catches conflicting answers (e.g. near blur vs zero strain)."),
        ("67% Question Reduction", "Averages 7.2 questions (under 90s) vs 24 questions (7–10m) in ZEISS Vision Profile without clinical depth loss.")
    ]
    for t, d in math_points:
        p = tf2_l.add_paragraph()
        p.text = f"• {t}: "
        p.font.size = Pt(12.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_BOLD
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(8)

    # Right Column: Fig 2 (Large, prominent Active Anamnesis Turn 1 in Kannada)
    add_framed_screenshot(
        s2,
        "docs/assets/screenshots/02_active_anamnesis.jpg",
        Inches(8.2),
        card_top,
        Inches(4.433),
        card_h,
        "Fig 2: Active Anamnesis Turn 1 (Kannada UI + English Subtitle)",
        border_color=ZEISS_BLUE,
        extra_note="Spoken Audio Playback 🔊 + Touch-Response Chief Complaint Tiles"
    )

    create_metric_tile(s2, Inches(0.7), m_top, m_w, m_h, "7.2", "AVG QUESTIONS ASKED", ZEISS_BLUE)
    create_metric_tile(s2, Inches(3.73), m_top, m_w, m_h, "< 2 ms", "INFERENCE TURN LATENCY", ACCENT_GREEN)
    create_metric_tile(s2, Inches(6.8), m_top, m_w, m_h, "67%", "REDUCTION VS 24-QN FORMS", ZEISS_BLUE)
    create_metric_tile(s2, Inches(9.83), m_top, m_w, m_h, "100%", "DETERMINISTIC SAFETY", ZEISS_BLUE)

    # =========================================================================
    # SLIDE 3: ZERO-HARDWARE CLINICAL SCREENING SUITE (2x2 PROMINENT GRID!)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    paint_background(s3)
    add_top_nav(s3, "Zero-Hardware Refractive & Macular Screening Suite", "Device-Free Triaging", "03")

    col3_w = Inches(5.4)
    card3_l = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.7), card_top, col3_w, card_h)
    card3_l.fill.solid()
    card3_l.fill.fore_color.rgb = BG_CARD
    card3_l.line.color.rgb = ACCENT_GREEN
    card3_l.line.width = Pt(2.0)

    tx3_l = s3.shapes.add_textbox(Inches(0.92), card_top + Inches(0.18), col3_w - Inches(0.44), card_h - Inches(0.32))
    tf3_l = tx3_l.text_frame
    tf3_l.word_wrap = True

    p = tf3_l.paragraphs[0]
    p.text = "3 ON-SCREEN TESTS & TURN-2 SENTINEL"
    p.font.size = Pt(15.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(8)

    tests_points = [
        ("Red-Green Duochrome Test", "Evaluates longitudinal chromatic aberration (650nm Red vs 535nm Green). Red clearer indicates myopia; Green clearer indicates hyperopia/over-minusing."),
        ("Astigmatic Clock Dial", "Visualizes the Conoid of Sturm at 30° radial meridians on Retina/OLED displays, identifying dominant cylinder axis for JCC refinement."),
        ("Amsler Grid Macular Guard", "Evaluates central 10° of visual field. Detects metamorphopsia (wavy lines) or scotomas (blind spots), flagging macular edema or AMD."),
        ("Turn-2 Invariant Circuit Breaker", "Every patient is probed for acute red flags on Turn 2. Flashes, floaters, or severe pain immediately halt intake with urgent hospital triage."),
        ("Zero Hallucination Guarantee", "Deterministic state machine; generates an emergency ophthalmology pass and never dispenses glasses when pathology is suspected.")
    ]
    for t, d in tests_points:
        p = tf3_l.add_paragraph()
        p.text = f"• {t}: "
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_BOLD
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(6)

    # Right Side: 2x2 Prominent Grid (Width: 3.1 in each, Height: 2.1 in each)
    grid_w = Inches(3.1)
    grid_h = Inches(2.1)
    gap_x = Inches(0.2)
    gap_y = Inches(0.15)
    r_col1 = Inches(6.35)
    r_col2 = r_col1 + grid_w + gap_x
    r_row1 = card_top
    r_row2 = card_top + grid_h + gap_y

    # Fig 3: Red-Green Duochrome Test
    add_framed_screenshot(
        s3,
        "docs/assets/screenshots/06_duochrome_test.png",
        r_col1,
        r_row1,
        grid_w,
        grid_h,
        "Fig 3: Duochrome (Spherical Balance)",
        border_color=ACCENT_GREEN,
        sub_badge="Red (650nm) vs Green (535nm)",
        extra_note="Evaluates Myopia / Hyperopia Accommodation"
    )

    # Fig 4: Astigmatic Clock Dial
    add_framed_screenshot(
        s3,
        "docs/assets/screenshots/07_astigmatic_dial.png",
        r_col2,
        r_row1,
        grid_w,
        grid_h,
        "Fig 4: Astigmatic Clock Dial Fan",
        border_color=ZEISS_BLUE,
        sub_badge="30° Radial Cylindrical Meridians",
        extra_note="Identifies Principal Astigmatic Axis"
    )

    # Fig 5: Amsler Grid Macular Guard
    add_framed_screenshot(
        s3,
        "docs/assets/screenshots/08_amsler_grid.png",
        r_col1,
        r_row2,
        grid_w,
        grid_h,
        "Fig 5: Amsler Grid Macular Guard",
        border_color=ACCENT_RED,
        sub_badge="Central 10° Foveal Field Check",
        extra_note="Detects Metamorphopsia & Macular Edema"
    )

    # Fig 6: Live Spoken Voice Waveform Recording & Acute Red-Flag Triage
    add_framed_screenshot(
        s3,
        "docs/assets/screenshots/03_voice_recording_triage.png",
        r_col2,
        r_row2,
        grid_w,
        grid_h,
        "Fig 6: Spoken Red-Flag Emergency Triage",
        border_color=ACCENT_RED,
        sub_badge="Voice Waveform + Instant Speech SLU",
        extra_note="Immediate Emergency Halt on Acute Symptoms"
    )

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

    col4_w = Inches(7.4)
    card4_l = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.7), card_top, col4_w, card_h)
    card4_l.fill.solid()
    card4_l.fill.fore_color.rgb = BG_CARD
    card4_l.line.color.rgb = ACCENT_AMBER
    card4_l.line.width = Pt(2.0)

    tx4_l = s4.shapes.add_textbox(Inches(0.95), card_top + Inches(0.2), col4_w - Inches(0.5), card_h - Inches(0.35))
    tf4_l = tx4_l.text_frame
    tf4_l.word_wrap = True

    p = tf4_l.paragraphs[0]
    p.text = "SOLVING 'THE INVISIBLE PRODUCT DILEMMA'"
    p.font.size = Pt(16.0)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER
    p.space_after = Pt(10)

    sim_arch_points = [
        ("The Retail Bottleneck", "Ophthalmic lenses are transparent pieces of plastic. A ₹1,200 generic stock lens and a ₹8,000 ZEISS lens look identical to a walk-in patient."),
        ("Hardware-Accelerated Split Slider", "Engineered using CSS clip-path dynamically bound to a range slider at 60 FPS without heavy WebGL GPU overhead."),
        ("DriveSafe Night Road", "Standard: Blinding LED high-beam starburst halo obscuring a roadside pedestrian. ZEISS DriveSafe: 64% glare attenuation reveals pedestrian & lane lines."),
        ("SmartLife Progressive", "Standard: Narrow 10mm reading corridor with lateral swim distortion and head strain. ZEISS SmartLife: Edge-to-edge panoramic reading zone."),
        ("BlueProtect & ClearView", "Digital blue scatter relief (BlueProtect); 3× wider peripheral clear zone vs standard spherical stock lens edge blur (ClearView).")
    ]
    for t, d in sim_arch_points:
        p = tf4_l.add_paragraph()
        p.text = f"• {t}: "
        p.font.size = Pt(12.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_BOLD
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(8)

    # Right Column: Fig 7 (Live ZEISS Match & Split Perception Simulator)
    add_framed_screenshot(
        s4,
        "docs/assets/screenshots/04_visual_simulator_profile.png",
        Inches(8.3),
        card_top,
        Inches(4.333),
        card_h,
        "Fig 7: Real-Time ZEISS Match & Split Perception Simulator",
        border_color=ZEISS_BLUE,
        extra_note="Progressive Adaptation Risk: 20/100 (LOW) • Interactive Split Slider"
    )

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

    col5_w = Inches(7.4)
    card5_l = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.7), card_top, col5_w, card_h)
    card5_l.fill.solid()
    card5_l.fill.fore_color.rgb = BG_CARD
    card5_l.line.color.rgb = ZEISS_BLUE
    card5_l.line.width = Pt(2.0)

    tx5_l = s5.shapes.add_textbox(Inches(0.95), card_top + Inches(0.2), col5_w - Inches(0.5), card_h - Inches(0.35))
    tf5_l = tx5_l.text_frame
    tf5_l.word_wrap = True

    p = tf5_l.paragraphs[0]
    p.text = "ZEISS VISUCONSULT 500 DIGITAL BRIDGE"
    p.font.size = Pt(16.0)
    p.font.bold = True
    p.font.color.rgb = ZEISS_BLUE
    p.space_after = Pt(10)

    interop_points = [
        ("Pure-Python Vector SVG QR Generator", "Generates compact vector QR codes offline without external cloud dependencies, encoding patient anamnesis and screening."),
        ("Practice iPad Scanning", "Optometrist scans the QR with VISUCONSULT 500 iPad camera, instantly loading refraction parameters, corridor lengths, and coating tiers."),
        ("Sanitized Printable Optical Slip", "HTML5 print layout (@media print) generates standard 80mm thermal receipt slips or A4 PDFs with optometrist sign-off block."),
        ("Two-Wheeler Transit Safety", "Recognizes motorcycle/scooter commute vector; escalates to 1.60 Shatterproof Polycarbonate / Trivex (ANSI Z87.1 road protection)."),
        ("OfficeLens Focal Ergonomics", "Maps occupational posture to Maximum Intermediate Distance (M.I.D.): Book (100cm), Desk (200cm), Room (400cm).")
    ]
    for t, d in interop_points:
        p = tf5_l.add_paragraph()
        p.text = f"• {t}: "
        p.font.size = Pt(12.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_BOLD
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(8)

    # Right Column: Fig 8 (Authentic Printable Consultation Slip)
    add_framed_screenshot(
        s5,
        "docs/assets/screenshots/05_printable_consultation_slip.jpg",
        Inches(8.3),
        card_top,
        Inches(4.333),
        card_h,
        "Fig 8: Standardized VISUCONSULT 500 Optical Slip",
        border_color=ZEISS_BLUE,
        extra_note="Includes Anamnesis, ZEISS Match, SVG QR & Optometrist Sign-off"
    )

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

    col6_w = Inches(5.8)
    card6_l = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.7), card_top, col6_w, card_h)
    card6_l.fill.solid()
    card6_l.fill.fore_color.rgb = BG_CARD
    card6_l.line.color.rgb = ACCENT_GREEN
    card6_l.line.width = Pt(2.0)

    tx6_l = s6.shapes.add_textbox(Inches(0.95), card_top + Inches(0.2), col6_w - Inches(0.5), card_h - Inches(0.35))
    tf6_l = tx6_l.text_frame
    tf6_l.word_wrap = True

    p = tf6_l.paragraphs[0]
    p.text = "FULL TECH STACK & RED TEAM HARDENING"
    p.font.size = Pt(16.0)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(10)

    tech_points = [
        ("Core Backend Stack", "Python 3.12, FastAPI 0.110+, Pydantic v2 (Rust-backed validation), Uvicorn async ASGI. Total RAM footprint < 120 MB."),
        ("Frontend & Speech", "Zero-Framework Vanilla HTML5/CSS3/ES6+ (<180 KB payload), W3C Web Speech API + gTTS server-side audio fallback."),
        ("5-Iteration Red Team Hardening", "Tested XSS injection, 8-thread concurrent race conditions, audio fuzzing, and invalid options. Patched XSS via html.escape; whitelisted screening inputs."),
        ("85 / 85 Automated Tests", "Comprehensive pytest test suite covering unit logic, API contracts, speech pipelines, and 100 stochastic Monte Carlo runs in 4.06 seconds.")
    ]
    for t, d in tech_points:
        p = tf6_l.add_paragraph()
        p.text = f"• {t}: "
        p.font.size = Pt(13.0)
        p.font.bold = True
        p.font.color.rgb = TEXT_BOLD
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(8)

    card6_r = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), card_top, col6_w, card_h)
    card6_r.fill.solid()
    card6_r.fill.fore_color.rgb = BG_CARD
    card6_r.line.color.rgb = ZEISS_BLUE
    card6_r.line.width = Pt(2.0)

    tx6_r = s6.shapes.add_textbox(Inches(7.05), card_top + Inches(0.2), col6_w - Inches(0.5), card_h - Inches(0.35))
    tf6_r = tx6_r.text_frame
    tf6_r.word_wrap = True

    p = tf6_r.paragraphs[0]
    p.text = "DEPLOYMENT, REPOSITORY & ROADMAP"
    p.font.size = Pt(16.0)
    p.font.bold = True
    p.font.color.rgb = ZEISS_BLUE
    p.space_after = Pt(10)

    roadmap_points = [
        ("Live Demonstration Access", "Equipped with 1-click Cloudflare Quick Tunnel (share_nayanee.bat) for zero-config public HTTPS testing on judges' mobile phones."),
        ("Production PWA Kiosk", "Service Worker (sw.js) + Web Manifest (manifest.json) for 1-tap installation on Android/iPad clinic reception counters."),
        ("Near-Term Roadmap (2–4 wks)", "On-device Vosk WebAssembly speech recognition for 100% offline rural camps; optometrist dim-room dark mode."),
        ("Major Roadmap (3–6 mos)", "OpenCV WebAssembly selfie-camera pupillometry (monocular PD & seg-height) with credit-card scaling; ABDM/FHIR locker sync."),
        ("GitHub Repository", "Complete, documented, production-ready codebase with CI automation: https://github.com/Satish8460/Nayanee")
    ]
    for t, d in roadmap_points:
        p = tf6_r.add_paragraph()
        p.text = f"✓ {t}: "
        p.font.size = Pt(12.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_BOLD
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = ZEISS_BLUE if "http" in d else TEXT_BODY
        if "http" in d:
            run.font.bold = True
            run.hyperlink.address = "https://github.com/Satish8460/Nayanee"
        p.space_after = Pt(7)

    create_metric_tile(s6, Inches(0.7), m_top, m_w, m_h, "85 / 85", "CI TEST SUITE PASSING", ACCENT_GREEN)
    create_metric_tile(s6, Inches(3.73), m_top, m_w, m_h, "4.06s", "TEST EXECUTION TIME", ZEISS_BLUE)
    create_metric_tile(s6, Inches(6.8), m_top, m_w, m_h, "5 Cycles", "RED TEAM SECURITY AUDIT", ZEISS_BLUE)
    create_metric_tile(s6, Inches(9.83), m_top, m_w, m_h, "GitHub", "SATISH8460 / NAYANEE", ZEISS_BLUE, link_url="https://github.com/Satish8460/Nayanee")

    for out_p in output_paths:
        try:
            prs.save(out_p)
            print(f"✨ Successfully generated presentation with prominent figures: {out_p}")
        except PermissionError:
            print(f"⚠️ Could not write to {out_p} (file in use).")


if __name__ == "__main__":
    build_final_6_slide_deck()
