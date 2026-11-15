"""Unit tests for POC-01: Adaptive Anamnesis Decision Engine.
"""

import pytest
from pocs.poc01_adaptive_engine.models import (
    LanguageCode,
    SeverityLevel,
    ReviewStatus,
)
from pocs.poc01_adaptive_engine.questions_bank import QUESTIONS
from pocs.poc01_adaptive_engine.fixed_engine import FixedQuestionnaireRunner
from pocs.poc01_adaptive_engine.adaptive_engine import AdaptiveAnamnesisEngine
from pocs.poc01_adaptive_engine.benchmark import (
    persona_presbyope_first_timer,
    persona_digital_screen_worker,
    persona_acute_red_flag,
    persona_contradictory_patient,
)


def test_question_bank_integrity():
    assert len(QUESTIONS) >= 10
    target_langs = {"kn", "hi", "ta", "te", "ml"}
    for q in QUESTIONS:
        assert q.id.startswith("q_")
        assert len(q.options) >= 2
        for lang in target_langs:
            assert lang in q.text_translations
            assert len(q.text_translations[lang]) > 5
            assert lang in q.options_translations
            for opt in q.options:
                assert opt in q.options_translations[lang], f"Missing {lang} translation for option {opt} in {q.id}"
                assert len(q.options_translations[lang][opt]) > 0


def test_adaptive_reduces_question_count_for_presbyope():
    fixed_engine = FixedQuestionnaireRunner(session_id="test_fixed_1")
    fixed_profile = fixed_engine.run(persona_presbyope_first_timer)

    adaptive_engine = AdaptiveAnamnesisEngine(session_id="test_adaptive_1")
    adaptive_profile = adaptive_engine.run_simulation(persona_presbyope_first_timer)

    assert fixed_profile.total_questions_asked == len(QUESTIONS)
    assert adaptive_profile.total_questions_asked < fixed_profile.total_questions_asked
    reduction = (fixed_profile.total_questions_asked - adaptive_profile.total_questions_asked) / fixed_profile.total_questions_asked
    assert reduction >= 0.25

    asked_qids = [turn.question_id for turn in adaptive_engine.turn_history]
    assert "q_glasses_age" not in asked_qids
    assert "q_glasses_satisfaction" not in asked_qids


def test_acute_red_flag_immediate_halt():
    adaptive_engine = AdaptiveAnamnesisEngine(session_id="test_red_flag")
    profile = adaptive_engine.run_simulation(persona_acute_red_flag)

    assert len(profile.red_flags) >= 1
    assert profile.red_flags[0].urgency == SeverityLevel.CRITICAL
    assert profile.review_status == ReviewStatus.URGENT_MEDICAL_ESCALATION
    assert profile.total_questions_asked <= 3


def test_contradiction_detection():
    adaptive_engine = AdaptiveAnamnesisEngine(session_id="test_contra")
    profile = adaptive_engine.run_simulation(persona_contradictory_patient)

    assert len(profile.contradictions) >= 1
    contra_rules = [c.explanation for c in profile.contradictions]
    assert any("Chief complaint states distance blur" in exp or "Reported complete inability to read" in exp for exp in contra_rules)
    assert profile.review_status == ReviewStatus.CLARIFICATION_REQUESTED


def test_functional_profile_generation():
    adaptive_engine = AdaptiveAnamnesisEngine(session_id="test_profile_gen", language=LanguageCode.KANNADA)
    profile = adaptive_engine.run_simulation(persona_digital_screen_worker)

    assert profile.customer_language == LanguageCode.KANNADA
    assert profile.distance_vision_status["has_distance_complaint"] is True
    assert profile.lifestyle_occupational_context["digital_visual_fatigue_risk"] is True
    assert profile.eyewear_history["current_modality"] == "distance_only"
    assert profile.is_sufficient_for_review is True


def test_age_prior_boosts_near_domain_for_presbyope():
    engine_presbyope = AdaptiveAnamnesisEngine(session_id="test_presb_age", patient_age=48)
    engine_baseline = AdaptiveAnamnesisEngine(session_id="test_baseline_age", patient_age=None)

    q_near = next(q for q in QUESTIONS if q.id == "q_near_mobile_reading")
    gain_presbyope = engine_presbyope.calculate_information_gain(q_near)
    gain_baseline = engine_baseline.calculate_information_gain(q_near)

    assert gain_presbyope == pytest.approx(gain_baseline * 1.25)


def test_age_prior_boosts_lifestyle_domain_for_youth():
    engine_youth = AdaptiveAnamnesisEngine(session_id="test_youth_age", patient_age=22)
    engine_baseline = AdaptiveAnamnesisEngine(session_id="test_baseline_age", patient_age=None)

    q_lifestyle = next(q for q in QUESTIONS if q.id == "q_outdoor_exposure")
    gain_youth = engine_youth.calculate_information_gain(q_lifestyle)
    gain_baseline = engine_baseline.calculate_information_gain(q_lifestyle)

    assert gain_youth == pytest.approx(gain_baseline * 1.20)


def test_age_none_fallback_strictly_neutral():
    engine_none = AdaptiveAnamnesisEngine(session_id="test_none_age", patient_age=None)
    engine_default = AdaptiveAnamnesisEngine(session_id="test_default_age")

    for q in QUESTIONS:
        gain_none = engine_none.calculate_information_gain(q)
        gain_default = engine_default.calculate_information_gain(q)
        assert gain_none == pytest.approx(gain_default)


def test_chief_complaint_and_red_flag_dominate_age_prior():
    engine_youth = AdaptiveAnamnesisEngine(session_id="test_dominate", patient_age=20)
    q_acute = next(q for q in QUESTIONS if q.id == "q_acute_symptoms")
    
    # Red flag probe must always return absolute top priority 2.5
    assert engine_youth.calculate_information_gain(q_acute) == 2.5

    # If young patient explicitly picks near blur as chief complaint, near domain dominates
    q_chief = next(q for q in QUESTIONS if q.id == "q_chief_complaint")
    engine_youth.record_answer(q_chief, "near_blur")

    q_near = next(q for q in QUESTIONS if q.id == "q_near_mobile_reading")
    q_dist = next(q for q in QUESTIONS if q.id == "q_dist_clarity")

    gain_near = engine_youth.calculate_information_gain(q_near)
    gain_dist = engine_youth.calculate_information_gain(q_dist)

    # Near gain (boosted 1.3x by chief complaint) exceeds distance gain
    assert gain_near > gain_dist


def test_gender_prior_boosts_dryness_and_near_for_female_presbyope():
    engine_female_presb = AdaptiveAnamnesisEngine(session_id="test_female_presb", patient_age=46, patient_gender="female")
    engine_baseline_presb = AdaptiveAnamnesisEngine(session_id="test_base_presb", patient_age=46, patient_gender=None)

    q_dryness = next(q for q in QUESTIONS if q.id == "q_ocular_surface_dryness")
    gain_female = engine_female_presb.calculate_information_gain(q_dryness)
    gain_baseline = engine_baseline_presb.calculate_information_gain(q_dryness)

    assert gain_female == pytest.approx(gain_baseline * 1.25)


def test_gender_none_or_other_strictly_neutral():
    engine_none = AdaptiveAnamnesisEngine(session_id="test_g_none", patient_gender=None)
    engine_other = AdaptiveAnamnesisEngine(session_id="test_g_other", patient_gender="other")

    for q in QUESTIONS:
        gain_none = engine_none.calculate_information_gain(q)
        gain_other = engine_other.calculate_information_gain(q)
        assert gain_none == pytest.approx(gain_other)


