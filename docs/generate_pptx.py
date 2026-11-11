"""Generates an executive-grade, visually polished 3-slide widescreen (.pptx) presentation
for Nayanee — ZEISS Hackathon Theme 2 (No-Device Vision Intelligence) & Theme 1 (AFI).
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE


def build_executive_deck(output_paths: list = None):
    if output_paths is None:
        output_paths = [
            "docs/Nayanee_Progress_Presentation_3_Slides.pptx",
            "docs/Nayanee_Executive_Presentation_3_Slides.pptx"
        ]
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    FONT_FAMILY = "Segoe UI"

    # Executive Color System (Deep Tech Navy / Electric Cyan / Pristine White)
    BG_DARK = RGBColor(6, 21, 45)          # #06152D
    BG_CARD = RGBColor(14, 38, 77)         # #0E264D
    BG_CARD_BORDER = RGBColor(30, 68, 128) # #1E4480
    ACCENT_CYAN = RGBColor(0, 210, 255)    # #00D2FF
    ACCENT_BLUE = RGBColor(0, 114, 255)    # #0072FF
    ACCENT_GREEN = RGBColor(0, 230, 118)   # #00E676
    ACCENT_RED = RGBColor(255, 82, 82)     # #FF5252
    TEXT_LIGHT = RGBColor(240, 246, 255)   # #F0F6FF
    TEXT_MUTED = RGBColor(140, 168, 204)   # #8CA8CC
    WHITE = RGBColor(255, 255, 255)

    def paint_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_top_nav(slide, title_text, category_pill, slide_num):
        # Header Box
        tx = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.5), Inches(0.9))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_sub = tf.paragraphs[0]
        p_sub.text = "NAYANEE (ನಯನಿ) • ZEISS HACKATHON PROGRESS"
        p_sub.font.size = Pt(9.5)
        p_sub.font.bold = True
        p_sub.font.color.rgb = ACCENT_CYAN
        p_sub.space_after = Pt(2)

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE

        # Pill Tag (Top Right)
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.4), Inches(0.45), Inches(3.1), Inches(0.45))
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
        num_box = slide.shapes.add_textbox(Inches(11.0), Inches(7.05), Inches(1.5), Inches(0.3))
        tf_n = num_box.text_frame
        p_n = tf_n.paragraphs[0]
        p_n.text = f"{slide_num} / 3"
        p_n.font.size = Pt(9.5)
        p_n.font.color.rgb = TEXT_MUTED
        p_n.alignment = PP_ALIGN.RIGHT

    def create_metric_tile(slide, left, top, width, height, stat_value, stat_label, accent_color=ACCENT_CYAN):
        tile = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        tile.fill.solid()
        tile.fill.fore_color.rgb = BG_CARD
        tile.line.color.rgb = BG_CARD_BORDER
        tile.line.width = Pt(1)

        tx = slide.shapes.add_textbox(left, top + Inches(0.1), width, height - Inches(0.15))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = stat_value
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = accent_color
        p1.alignment = PP_ALIGN.CENTER

        p2 = tf.add_paragraph()
        p2.text = stat_label
        p2.font.size = Pt(8.5)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_MUTED
        p2.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 1: THE PARADIGM SHIFT (No-Device Vision Intelligence)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    paint_background(s1)
    add_top_nav(s1, "No-Device Vision Intelligence for Walk-In Retail", "Theme 2 (Primary) & Theme 1 (AFI)", "01")

    # Left Column: The Problem Card
    left_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(4.3))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = BG_CARD
    left_card.line.color.rgb = ACCENT_RED
    left_card.line.width = Pt(1.5)

    tx_l = s1.shapes.add_textbox(Inches(1.05), Inches(1.7), Inches(5.1), Inches(3.9))
    tf_l = tx_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "THE RURAL & RETAIL DILEMMA"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED
    p.space_after = Pt(12)

    problems = [
        ("No Testing Equipment", "Small stores have no $10,000 autorefractors—just a phone or a front counter."),
        ("25-Question Form Fatigue", "Static paper/digital questionnaires waste time asking irrelevant questions to every customer."),
        ("Language & Literacy Barrier", "Walk-in customers speak Dravidian/Indic dialects; English forms create high friction."),
        ("The Unsafe LLM Trap", "Generic generative AI chatbots hallucinate unsupported prescriptions and lack medical safety gates.")
    ]
    for title, desc in problems:
        p = tf_l.add_paragraph()
        p.text = f"✕  {title}: "
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT

        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(8)

    # Right Column: The Nayanee Solution Card
    right_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(4.3))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = BG_CARD
    right_card.line.color.rgb = ACCENT_GREEN
    right_card.line.width = Pt(1.5)

    tx_r = s1.shapes.add_textbox(Inches(7.05), Inches(1.7), Inches(5.2), Inches(3.9))
    tf_r = tx_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "THE NAYANEE BREAKTHROUGH (AFI ETHOS)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(12)

    solutions = [
        ("Zero Hardware Dependency", "Captures complete functional vision demands on any commodity smartphone or store PC."),
        ("6 Native Indic Languages", "Communicates naturally via voice in Kannada, Hindi, Tamil, Telugu, Malayalam, and English."),
        ("Mathematical Entropy Pruning", "Information-theoretic engine cuts consultation length by > 25% by pruning irrelevant inquiries."),
        ("Deterministic Clinical Safety", "Hardcoded acute red-flag triage immediately halts on emergency symptoms with zero hallucination.")
    ]
    for title, desc in solutions:
        p = tf_r.add_paragraph()
        p.text = f"✓  {title}: "
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT

        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(8)

    # Bottom Metric Strip
    create_metric_tile(s1, Inches(0.8), Inches(6.0), Inches(2.7), Inches(0.85), "$0", "HARDWARE EQUIPMENT COST", ACCENT_GREEN)
    create_metric_tile(s1, Inches(3.7), Inches(6.0), Inches(2.7), Inches(0.85), "6", "NATIVE INDIC LANGUAGES", ACCENT_CYAN)
    create_metric_tile(s1, Inches(6.8), Inches(6.0), Inches(2.7), Inches(0.85), "> 25%", "CONSULTATION TIME REDUCED", ACCENT_CYAN)
    create_metric_tile(s1, Inches(9.7), Inches(6.0), Inches(2.8), Inches(0.85), "100%", "ZERO-GPU CPU EXECUTION", ACCENT_BLUE)

    # =========================================================================
    # SLIDE 2: UNDER THE HOOD (Technical Novelty & Architecture)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    paint_background(s2)
    add_top_nav(s2, "Under The Hood: Information Theory & Clinical Safety", "Algorithmic Novelty", "02")

    # 3-Column Pillar Architecture
    col_w = Inches(3.65)
    gap = Inches(0.4)

    # Pillar 1: Information Theory Engine
    p1_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), col_w, Inches(4.3))
    p1_card.fill.solid()
    p1_card.fill.fore_color.rgb = BG_CARD
    p1_card.line.color.rgb = ACCENT_CYAN
    p1_card.line.width = Pt(1.5)

    tx_p1 = s2.shapes.add_textbox(Inches(1.0), Inches(1.7), col_w - Inches(0.4), Inches(3.9))
    tf_p1 = tx_p1.text_frame
    tf_p1.word_wrap = True

    p = tf_p1.paragraphs[0]
    p.text = "1. ADAPTIVE ENTROPY ENGINE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(10)

    p1_points = [
        ("Shannon Entropy Scoring", "Quantifies remaining uncertainty across 5 axes: Distance, Near, Screen, Lifestyle, Eyewear."),
        ("Dynamic Pruning", "Automatically suppresses non-applicable branches (e.g. progressive comfort skipped for first-time readers)."),
        ("Contradiction Triage", "Catches conflicting answers in real-time (e.g. reporting distance blur but zero trouble with bus signs).")
    ]
    for t, d in p1_points:
        p = tf_p1.add_paragraph()
        p.text = f"• {t}: "
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(6)

    # Pillar 2: Multilingual Voice & SLU
    p2_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8) + col_w + gap, Inches(1.5), col_w, Inches(4.3))
    p2_card.fill.solid()
    p2_card.fill.fore_color.rgb = BG_CARD
    p2_card.line.color.rgb = ACCENT_BLUE
    p2_card.line.width = Pt(1.5)

    tx_p2 = s2.shapes.add_textbox(Inches(1.0) + col_w + gap, Inches(1.7), col_w - Inches(0.4), Inches(3.9))
    tf_p2 = tx_p2.text_frame
    tf_p2.word_wrap = True

    p = tf_p2.paragraphs[0]
    p.text = "2. DRAVIDIAN VOICE & ZERO-GPU SLU"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    p.space_after = Pt(10)

    p2_points = [
        ("Native MP3 Streaming", "Streams clear native Indic speech (/api/v1/session/speak) via HTML5 Audio, bypassing missing OS voice packs."),
        ("Colloquial Phrasing", "Uses culturally authentic clinical speech rather than mechanical Google Translate word-for-word text."),
        ("Zero-GPU Intent Matcher", "Local keyword & token-overlap SLU engine parses spoken native answers directly on CPU with confidence scoring.")
    ]
    for t, d in p2_points:
        p = tf_p2.add_paragraph()
        p.text = f"• {t}: "
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(6)

    # Pillar 3: Deterministic Clinical Safety
    p3_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8) + (col_w + gap) * 2, Inches(1.5), col_w, Inches(4.3))
    p3_card.fill.solid()
    p3_card.fill.fore_color.rgb = BG_CARD
    p3_card.line.color.rgb = ACCENT_GREEN
    p3_card.line.width = Pt(1.5)

    tx_p3 = s2.shapes.add_textbox(Inches(1.0) + (col_w + gap) * 2, Inches(1.7), col_w - Inches(0.4), Inches(3.9))
    tf_p3 = tx_p3.text_frame
    tf_p3.word_wrap = True

    p = tf_p3.paragraphs[0]
    p.text = "3. DETERMINISTIC CLINICAL SAFETY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(10)

    p3_points = [
        ("Acute Red-Flag Sentinel", "Probes for critical warning signs: sudden vision loss, severe eye pain, and flashes of light."),
        ("Immediate Emergency Halt", "Aborts routine questioning immediately upon acute symptoms and escalates directly to ophthalmology."),
        ("Zero Hallucination Risk", "Pure deterministic state machine; never guesses a prescription or replaces professional refraction.")
    ]
    for t, d in p3_points:
        p = tf_p3.add_paragraph()
        p.text = f"• {t}: "
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(6)

    # Bottom Metric Strip
    create_metric_tile(s2, Inches(0.8), Inches(6.0), Inches(2.7), Inches(0.85), "< 0.1 ms", "DECISION ENGINE LATENCY", ACCENT_CYAN)
    create_metric_tile(s2, Inches(3.7), Inches(6.0), Inches(2.7), Inches(0.85), "100%", "DETERMINISTIC SAFETY GATES", ACCENT_GREEN)
    create_metric_tile(s2, Inches(6.8), Inches(6.0), Inches(2.7), Inches(0.85), "Sub-500ms", "VOICE STREAMING RESPONSE", ACCENT_BLUE)
    create_metric_tile(s2, Inches(9.7), Inches(6.0), Inches(2.8), Inches(0.85), "38 / 38", "CI TEST SUITE PASSED", ACCENT_GREEN)

    # =========================================================================
    # SLIDE 3: CLINICAL HANDOVER & FRUGAL DEPLOYMENT
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    paint_background(s3)
    add_top_nav(s3, "Clinical Handover, Optometrist Review & Deployment", "Production Readiness", "03")

    # Left Column: Optometrist Decision Support
    left_c3 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(4.3))
    left_c3.fill.solid()
    left_c3.fill.fore_color.rgb = BG_CARD
    left_c3.line.color.rgb = ACCENT_CYAN
    left_c3.line.width = Pt(1.5)

    tx_c3l = s3.shapes.add_textbox(Inches(1.05), Inches(1.7), Inches(5.1), Inches(3.9))
    tf_c3l = tx_c3l.text_frame
    tf_c3l.word_wrap = True

    p = tf_c3l.paragraphs[0]
    p.text = "OPTOMETRIST DECISION SUPPORT (POC-05)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(12)

    handover_points = [
        ("Pre-Refraction Lifestyle Advisor", "Translates intake into optical considerations: blue-light filters for heavy screen hours (>8h); UV400/photochromic for sun exposure."),
        ("Dedicated Review Portal", "Practitioner triage dashboard with domain uncertainty radar, patient demographics, and audit trail."),
        ("1-Click Printable Slip", "Formatted consultation slip ready for store receipt/A4 printing, including emergency triage clearance and optometrist sign-off block."),
        ("EHR Interoperability", "Exports structured JSON profiles ready for hospital electronic health record integration.")
    ]
    for title, desc in handover_points:
        p = tf_c3l.add_paragraph()
        p.text = f"✓  {title}: "
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(8)

    # Right Column: Frugal Hardware & Production Readiness
    right_c3 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(4.3))
    right_c3.fill.solid()
    right_c3.fill.fore_color.rgb = BG_CARD
    right_c3.line.color.rgb = ACCENT_GREEN
    right_c3.line.width = Pt(1.5)

    tx_c3r = s3.shapes.add_textbox(Inches(7.05), Inches(1.7), Inches(5.2), Inches(3.9))
    tf_c3r = tx_c3r.text_frame
    tf_c3r.word_wrap = True

    p = tf_c3r.paragraphs[0]
    p.text = "FRUGAL ARCHITECTURE & READINESS (POC-06)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(12)

    readiness_points = [
        ("Micro-Instance Deployment", "Runs entirely on CPU with < 80 MB RAM footprint; deployable on ordinary smartphones, store laptops, or a $35 Raspberry Pi."),
        ("PWA Offline Resilient", "Equipped with Service Worker (sw.js) and Web App Manifest (manifest.json) for standalone home-screen installation."),
        ("1-Click Windows Launch", "Standardized on start.bat with auto Python 3.12 detection, UTF-8 mode, and browser auto-launch."),
        ("Live Open Source Codebase", "Complete, clean repository up to date on main: github.com/Satish8460/Nayanee.")
    ]
    for title, desc in readiness_points:
        p = tf_c3r.add_paragraph()
        p.text = f"✓  {title}: "
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(8)

    # Bottom Metric Strip
    create_metric_tile(s3, Inches(0.8), Inches(6.0), Inches(2.7), Inches(0.85), "< 80 MB", "LIGHTWEIGHT CPU RAM", ACCENT_CYAN)
    create_metric_tile(s3, Inches(3.7), Inches(6.0), Inches(2.7), Inches(0.85), "1-Click", "START.BAT LAUNCHER", ACCENT_GREEN)
    create_metric_tile(s3, Inches(6.8), Inches(6.0), Inches(2.7), Inches(0.85), "PWA Ready", "OFFLINE SERVICE WORKER", ACCENT_BLUE)
    create_metric_tile(s3, Inches(9.7), Inches(6.0), Inches(2.8), Inches(0.85), "Open Source", "GITHUB.COM/SATISH8460/NAYANEE", ACCENT_CYAN)

    for out_p in output_paths:
        try:
            prs.save(out_p)
            print(f"✨ Successfully generated executive presentation: {out_p}")
        except PermissionError:
            print(f"⚠️ Could not write to {out_p} (file in use).")


if __name__ == "__main__":
    build_executive_deck()
