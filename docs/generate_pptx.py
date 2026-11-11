"""Generates a professional 3-slide widescreen (.pptx) presentation for Nayanee ZEISS Hackathon.
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE


def create_presentation(output_path: str = "docs/Nayanee_Progress_Presentation_3_Slides.pptx"):
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    COLOR_NAVY = RGBColor(0, 43, 102)        # #002B66
    COLOR_PRIMARY = RGBColor(0, 82, 204)     # #0052CC
    COLOR_TEXT_DARK = RGBColor(23, 43, 77)   # #172B4D
    COLOR_TEXT_MUTED = RGBColor(94, 108, 132)# #5E6C84
    COLOR_BG_CARD = RGBColor(244, 245, 247)  # #F4F5F7
    COLOR_CARD_BORDER = RGBColor(223, 225, 230) # #DFE1E6
    COLOR_ALERT_BG = RGBColor(255, 240, 235) # #FFF0EB
    COLOR_ALERT_TXT = RGBColor(191, 38, 0)   # #BF2600
    COLOR_SUCCESS_BG = RGBColor(235, 250, 242) # #EBFAF2
    COLOR_SUCCESS_TXT = RGBColor(0, 102, 68) # #006644
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_PILL_BG = RGBColor(222, 235, 255)  # #DEEBFF
    COLOR_PILL_TXT = RGBColor(7, 71, 166)    # #0747A6

    def add_header(slide, title_text, subtitle_text, slide_num):
        # Top banner shape
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        banner.fill.solid()
        banner.fill.fore_color.rgb = COLOR_NAVY
        banner.line.color.rgb = COLOR_NAVY

        # Logo / Icon box
        logo_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.2), Inches(0.75), Inches(0.75))
        logo_box.fill.solid()
        logo_box.fill.fore_color.rgb = COLOR_PRIMARY
        logo_box.line.color.rgb = COLOR_PRIMARY
        tf_l = logo_box.text_frame
        p_l = tf_l.paragraphs[0]
        p_l.text = "न"
        p_l.font.size = Pt(22)
        p_l.font.bold = True
        p_l.font.color.rgb = COLOR_WHITE
        p_l.alignment = PP_ALIGN.CENTER

        # Title text
        tx = slide.shapes.add_textbox(Inches(1.7), Inches(0.15), Inches(7.5), Inches(0.85))
        tf = tx.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title_text
        p1.font.size = Pt(20)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_WHITE

        p2 = tf.add_paragraph()
        p2.text = subtitle_text
        p2.font.size = Pt(11)
        p2.font.color.rgb = RGBColor(179, 212, 255)

        # Theme Badge (Right)
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.6), Inches(0.3), Inches(3.0), Inches(0.55))
        badge.fill.solid()
        badge.fill.fore_color.rgb = COLOR_PRIMARY
        badge.line.color.rgb = COLOR_WHITE
        tf_b = badge.text_frame
        p_b = tf_b.paragraphs[0]
        p_b.text = "ZEISS Theme 2 (Primary) & 1 (AFI)"
        p_b.font.size = Pt(10)
        p_b.font.bold = True
        p_b.font.color.rgb = COLOR_WHITE
        p_b.alignment = PP_ALIGN.CENTER

        # Slide Number (Bottom Right)
        footer_tx = slide.shapes.add_textbox(Inches(10.5), Inches(7.0), Inches(2.2), Inches(0.35))
        tf_f = footer_tx.text_frame
        p_f = tf_f.paragraphs[0]
        p_f.text = f"Slide {slide_num} of 3 | Nayanee"
        p_f.font.size = Pt(10)
        p_f.font.color.rgb = COLOR_TEXT_MUTED
        p_f.alignment = PP_ALIGN.RIGHT

    def add_card(slide, left, top, width, height, title, items, bg_color=COLOR_BG_CARD, border_color=COLOR_PRIMARY, title_color=COLOR_NAVY):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        tx = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), height - Inches(0.3))
        tf = tx.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = title_color
        p_t.space_after = Pt(8)

        for heading, body in items:
            p = tf.add_paragraph()
            p.text = f"• {heading}: "
            p.font.bold = True
            p.font.size = Pt(10.5)
            p.font.color.rgb = COLOR_TEXT_DARK

            run = p.add_run()
            run.text = body
            run.font.bold = False
            run.font.size = Pt(10.5)
            run.font.color.rgb = COLOR_TEXT_DARK
            p.space_after = Pt(6)

    def add_stat_box(slide, left, top, width, height, val_text, label_text):
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        box.fill.solid()
        box.fill.fore_color.rgb = COLOR_PILL_BG
        box.line.color.rgb = COLOR_PRIMARY
        box.line.width = Pt(1)

        tx = slide.shapes.add_textbox(left, top + Inches(0.05), width, height - Inches(0.1))
        tf = tx.text_frame
        p1 = tf.paragraphs[0]
        p1.text = val_text
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_PRIMARY
        p1.alignment = PP_ALIGN.CENTER

        p2 = tf.add_paragraph()
        p2.text = label_text
        p2.font.size = Pt(8.5)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_TEXT_MUTED
        p2.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 1: Problem & The No-Device Vision
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    add_header(s1, "Nayanee (ನಯನಿ) — No-Device Vision Intelligence", "Capturing Functional Vision Demands at Ordinary Counters Without Specialized Hardware", 1)

    s1_left_items = [
        ("No Dedicated Equipment", "In thousands of rural stores, there are no $10K autorefractors—just a phone or a counter."),
        ("The 25-Question Form Trap", "Static paper forms fatigue walk-in customers with irrelevant progressive adaptation questions."),
        ("Language & Literacy Divide", "Customers speak regional Indic dialects (Kannada, Hindi, etc.); English questionnaires create high friction."),
        ("The Unsafe Generative AI Trap", "Generic LLM chatbots hallucinate unsupported prescriptions, lack clinical boundary safety, and require costly cloud GPUs.")
    ]
    add_card(s1, Inches(0.8), Inches(1.4), Inches(5.6), Inches(4.3), "⚠️ The Rural & Retail Optical Dilemma", s1_left_items, COLOR_ALERT_BG, RGBColor(222, 53, 11), COLOR_ALERT_TXT)

    s1_right_items = [
        ("Smartphone-Native Anamnesis", "Captures complete functional vision needs on any phone or PC without dedicated refractive hardware."),
        ("Voice-First in 6 Indic Languages", "Natural, culturally authentic clinical conversations in Kannada, Hindi, Tamil, Telugu, Malayalam, and English."),
        ("Adaptive Entropy Questioning", "Selects the most informative next question based on information gain, pruning questions by > 25%."),
        ("Optometrist Review & Handover", "Prepares structured clinical profiles, optical lifestyle recommendations, and printable consultation slips.")
    ]
    add_card(s1, Inches(6.8), Inches(1.4), Inches(5.6), Inches(4.3), "💡 The Nayanee Solution (AFI Approach)", s1_right_items, COLOR_SUCCESS_BG, RGBColor(0, 135, 90), COLOR_SUCCESS_TXT)

    add_stat_box(s1, Inches(0.8), Inches(5.9), Inches(3.6), Inches(0.85), "$0 Hardware", "COMMODITY SMARTPHONE / PC")
    add_stat_box(s1, Inches(4.8), Inches(5.9), Inches(3.6), Inches(0.85), "6 Indic Languages", "AUTHENTIC NATIVE SPOKEN VOICE")
    add_stat_box(s1, Inches(8.8), Inches(5.9), Inches(3.6), Inches(0.85), "> 25% Pruning", "FASTER ADAPTIVE CONSULTATION")

    # ==========================================
    # SLIDE 2: Technical Breakthroughs & Novelty
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Technical Breakthroughs & Algorithmic Novelty", "Frugal Software Intelligence Replacing Expensive Physical Equipment", 2)

    s2_left_items = [
        ("Shannon Entropy Scoring", "Quantifies remaining uncertainty across 5 clinical axes: Distance, Near (Presbyopia), Screen, Lifestyle, Eyewear."),
        ("Dynamic Dependency Pruning", "Automatically suppresses non-applicable questions (e.g. progressive comfort skipped for first-time readers)."),
        ("Cross-Turn Contradiction Engine", "Catches conflicting answers in real-time (e.g. reporting distance blur but zero trouble with bus signs) and flags for optometrist review.")
    ]
    add_card(s2, Inches(0.8), Inches(1.4), Inches(5.6), Inches(4.3), "1. Information-Theoretic Adaptive Engine (POC-01)", s2_left_items, COLOR_BG_CARD, COLOR_PRIMARY, COLOR_NAVY)

    s2_right_items = [
        ("Server-Streamed Native MP3 Voice", "Streams native Indic speech (/api/v1/session/speak) via HTML5 Audio, overcoming OS speech-pack deficits across all devices."),
        ("Zero-GPU Clinical SLU Parser", "Local keyword and token-overlap intent matcher (speech_analyzer.py) analyzes spoken native responses on CPU with confidence scoring."),
        ("Deterministic Red-Flag Sentinel", "Immediate halt on acute symptoms (sudden loss of vision, severe pain, flashes), routing directly to medical ophthalmology with zero hallucination.")
    ]
    add_card(s2, Inches(6.8), Inches(1.4), Inches(5.6), Inches(4.3), "2. Multilingual Voice & Clinical SLU (POC-02 & 03)", s2_right_items, COLOR_BG_CARD, COLOR_PRIMARY, COLOR_NAVY)

    add_stat_box(s2, Inches(0.8), Inches(5.9), Inches(3.6), Inches(0.85), "< 0.1 ms", "DECISION ENGINE RESPONSE TIME")
    add_stat_box(s2, Inches(4.8), Inches(5.9), Inches(3.6), Inches(0.85), "100% Deterministic", "ZERO GENERATIVE HALLUCINATION")
    add_stat_box(s2, Inches(8.8), Inches(5.9), Inches(3.6), Inches(0.85), "38 / 38 Tests", "CI TEST SUITE PASSED")

    # ==========================================
    # SLIDE 3: Clinical Handover & Frugal Deployment
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Clinical Handover, Optometrist Support & Deployment", "Production-Ready Architecture Built for Real-World Optical Stores", 3)

    s3_left_items = [
        ("Optical Lifestyle Advisor", "Recommends pre-refraction optical considerations: blue-attenuating filters for screen workload (>8 hrs) and UV400/polarized for outdoor exposure."),
        ("Optometrist Review Portal", "Dedicated triage dashboard with domain uncertainty radar, patient demographics, and audit trails."),
        ("Printable Consultation Slip", "Instant 1-click HTML consultation slip ready for store receipt/A4 printing, complete with emergency triage alerts and optometrist sign-off block.")
    ]
    add_card(s3, Inches(0.8), Inches(1.4), Inches(5.6), Inches(4.3), "Optometrist Decision Support & EHR (POC-05)", s3_left_items, COLOR_SUCCESS_BG, RGBColor(0, 135, 90), COLOR_SUCCESS_TXT)

    s3_right_items = [
        ("Advanced Frugal Innovation (AFI)", "Runs entirely on CPU with < 80 MB RAM footprint; deployable on ordinary smartphones, store PCs, or a $35 Raspberry Pi."),
        ("PWA Offline Resilient", "Equipped with Service Worker (sw.js) and Web App Manifest (manifest.json) for standalone home-screen installation."),
        ("One-Click Launch & GitHub", "Standardized on start.bat with auto Python detection. Verified and live at github.com/Satish8460/Nayanee.")
    ]
    add_card(s3, Inches(6.8), Inches(1.4), Inches(5.6), Inches(4.3), "Frugal Hardware Architecture & Verification (POC-06)", s3_right_items, COLOR_BG_CARD, COLOR_PRIMARY, COLOR_NAVY)

    add_stat_box(s3, Inches(0.8), Inches(5.9), Inches(3.6), Inches(0.85), "< 80 MB", "LIGHTWEIGHT CPU RAM FOOTPRINT")
    add_stat_box(s3, Inches(4.8), Inches(5.9), Inches(3.6), Inches(0.85), "1-Click Launch", "STANDARDIZED WINDOWS START.BAT")
    add_stat_box(s3, Inches(8.8), Inches(5.9), Inches(3.6), Inches(0.85), "Open Source", "GITHUB.COM/SATISH8460/NAYANEE")

    prs.save(output_path)
    print(f"✅ Generated 16:9 Presentation: {output_path}")


if __name__ == "__main__":
    create_presentation()
