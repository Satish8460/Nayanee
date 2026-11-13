"""Comprehensive Unit & Determinism Tests for POC-07:
ZEISS Lens Recommender & Interactive On-Screen Screening Tests.
"""

import pytest
from pocs.poc01_adaptive_engine.models import (
    FunctionalVisionProfile,
    LanguageCode,
    ReviewStatus,
)
from pocs.poc07_zeiss_matcher_and_screening.zeiss_lens_recommender import (
    ZeissLensRecommender,
    ZeissLensRecommendation,
)
from pocs.poc07_zeiss_matcher_and_screening.onscreen_screening import (
    OnScreenScreeningEngine,
    ScreeningResult,
)


def create_base_profile(age=30, screen="one_to_four", near="normal", glare="no_glare", sun="none_or_rarely"):
    return FunctionalVisionProfile(
        profile_id="test_prof",
        session_id="test_sess",
        customer_language=LanguageCode.ENGLISH,
        total_questions_asked=4,
        patient_name="Test Patient",
        patient_age=age,
        patient_gender="Other",
        lifestyle_occupational_context={
            "daily_screen_hours": screen,
            "outdoor_sun_exposure": sun,
        },
        near_vision_status={"mobile_reading_status": near},
        distance_vision_status={
            "distance_clarity_status": "clear_distance",
            "night_glare_difficulty": glare,
        },
        eyewear_history={"glasses_wearer": "first_time"},
    )


def test_digital_lens_for_young_screen_worker():
    prof = create_base_profile(age=28, screen="more_than_eight")
    rec = ZeissLensRecommender.recommend(prof)

    assert rec.primary_lens == "ZEISS Digital Lenses"
    assert rec.lens_family == "ZEISS Digital Lens Portfolio"
    assert "DuraVision BlueProtect" in rec.recommended_coating
    assert "+0.50D" in rec.corridor_or_boost
    assert len(rec.lifestyle_triggers) >= 1


def test_progressive_smartlife_for_presbyope_heavy_screen():
    prof = create_base_profile(age=48, screen="five_to_eight", near="significant_blur_holds_far")
    rec = ZeissLensRecommender.recommend(prof)

    assert "SmartLife Progressive" in rec.primary_lens
    assert rec.lens_family == "ZEISS Progressive Portfolio"
    assert "Near Priority" in rec.primary_lens
    assert "1.60 High Index" in rec.recommended_index


def test_drivesafe_for_night_glare_driver():
    prof = create_base_profile(age=32, glare="severe_glare_avoids_driving")
    rec = ZeissLensRecommender.recommend(prof)

    assert "DriveSafe" in rec.primary_lens
    assert rec.lens_family == "ZEISS DriveSafe Portfolio"
    assert "DuraVision DriveSafe" in rec.recommended_coating


def test_clearview_default_for_standard_patient():
    prof = create_base_profile(age=25, screen="one_to_four", near="normal", glare="no_glare")
    rec = ZeissLensRecommender.recommend(prof)

    assert rec.primary_lens == "ZEISS Single Vision ClearView"
    assert rec.lens_family == "ZEISS ClearView Single Vision Portfolio"
    assert "DuraVision Platinum UV" in rec.recommended_coating


def test_photofusion_for_heavy_sunlight():
    prof = create_base_profile(age=35, sun="majority_outdoors_heavy_sun")
    rec = ZeissLensRecommender.recommend(prof)

    assert "PhotoFusion X" in rec.recommended_coating
    assert "1.60 Impact-Resistant" in rec.recommended_index


def test_duochrome_test_evaluations():
    r_red = OnScreenScreeningEngine.evaluate_duochrome("red_clearer")
    assert r_red.status == "needs_clinical_attention"
    assert "myopic" in r_red.clinical_notes_for_optometrist.lower()

    r_green = OnScreenScreeningEngine.evaluate_duochrome("green_clearer")
    assert r_green.status == "needs_clinical_attention"
    assert "hyperopic" in r_green.clinical_notes_for_optometrist.lower()

    r_equal = OnScreenScreeningEngine.evaluate_duochrome("equally_sharp")
    assert r_equal.status == "normal"


def test_astigmatic_dial_evaluations():
    dial_normal = OnScreenScreeningEngine.evaluate_astigmatic_dial("all_lines_equal")
    assert dial_normal.status == "normal"

    dial_vertical = OnScreenScreeningEngine.evaluate_astigmatic_dial("12_to_6")
    assert dial_vertical.status == "abnormal"
    assert "Vertical" in dial_vertical.finding
    assert "Jackson Cross-Cylinder" in dial_vertical.clinical_notes_for_optometrist


def test_amsler_grid_emergency_sentinel():
    grid_normal = OnScreenScreeningEngine.evaluate_amsler_grid("all_lines_straight")
    assert grid_normal.status == "normal"
    assert grid_normal.is_emergency_flag is False

    grid_wavy = OnScreenScreeningEngine.evaluate_amsler_grid("wavy_distorted_lines")
    assert grid_wavy.status == "urgent_referral"
    assert grid_wavy.is_emergency_flag is True
    assert "MACULAR" in grid_wavy.clinical_notes_for_optometrist

    grid_scotoma = OnScreenScreeningEngine.evaluate_amsler_grid("dark_patch_missing_spots")
    assert grid_scotoma.status == "urgent_referral"
    assert grid_scotoma.is_emergency_flag is True


def test_deterministic_stability_100_runs():
    """Verify that running the engine 100 times consecutively yields 100% identical outputs."""
    prof = create_base_profile(age=45, screen="five_to_eight", near="significant_blur_holds_far", glare="moderate_glare")
    first_res = ZeissLensRecommender.recommend(prof)

    for _ in range(100):
        subsequent = ZeissLensRecommender.recommend(prof)
        assert subsequent.primary_lens == first_res.primary_lens
        assert subsequent.recommended_coating == first_res.recommended_coating
        assert subsequent.corridor_or_boost == first_res.corridor_or_boost
        assert subsequent.optician_dispensing_notes == first_res.optician_dispensing_notes
