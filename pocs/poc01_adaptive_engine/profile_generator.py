"""Profile Generator for Nayanee Anamnesis Engines.
"""

from typing import Dict, List, Optional
from .models import (
    FunctionalVisionProfile,
    AnswerRecord,
    ContradictionFlag,
    RedFlagAlert,
    LanguageCode,
    ReviewStatus,
)


def build_functional_profile(
    session_id: str,
    language: LanguageCode,
    answers: Dict[str, AnswerRecord],
    turn_history: List[AnswerRecord],
    contradictions: Optional[List[ContradictionFlag]] = None,
    red_flags: Optional[List[RedFlagAlert]] = None,
    uncertainty_score: float = 0.0,
    engine_type: str = "adaptive",
    patient_name: str = "Anonymous Patient",
    patient_age: Optional[int] = None,
    patient_gender: Optional[str] = None,
    patient_phone: Optional[str] = None,
) -> FunctionalVisionProfile:
    contradictions = contradictions or []
    red_flags = red_flags or []

    dist_clarity = answers.get("q_dist_clarity")
    night_glare = answers.get("q_night_driving_glare")
    distance_status = {
        "clarity_rating": dist_clarity.selected_option if dist_clarity else "unassessed",
        "night_glare_difficulty": night_glare.selected_option if night_glare else "unassessed",
        "has_distance_complaint": any(
            a.selected_option in ["often", "always", "distance_blur", "severe_glare_avoids_driving"]
            for a in answers.values()
        ),
    }

    near_reading = answers.get("q_near_mobile_reading")
    fine_fatigue = answers.get("q_fine_task_fatigue")
    near_status = {
        "mobile_reading_status": near_reading.selected_option if near_reading else "unassessed",
        "fine_task_fatigue": fine_fatigue.selected_option if fine_fatigue else "unassessed",
        "has_presbyopic_indicators": (
            near_reading.selected_option in ["significant_blur_holds_far", "cannot_read_near"]
            if near_reading else False
        ),
    }

    screen_time = answers.get("q_intermediate_screen")
    outdoor_exp = answers.get("q_outdoor_exposure")
    lifestyle_status = {
        "daily_screen_hours": screen_time.selected_option if screen_time else "unassessed",
        "outdoor_sun_exposure": outdoor_exp.selected_option if outdoor_exp else "unassessed",
        "digital_visual_fatigue_risk": screen_time.selected_option in ["five_to_eight", "more_than_eight"] if screen_time else False,
    }

    eyewear_cur = answers.get("q_current_eyewear")
    eyewear_age = answers.get("q_glasses_age")
    eyewear_sat = answers.get("q_glasses_satisfaction")
    eyewear_status = {
        "current_modality": eyewear_cur.selected_option if eyewear_cur else "never_worn",
        "glasses_age": eyewear_age.selected_option if eyewear_age else "n/a",
        "satisfaction_level": eyewear_sat.selected_option if eyewear_sat else "n/a",
    }

    if red_flags:
        status = ReviewStatus.URGENT_MEDICAL_ESCALATION
    elif contradictions:
        status = ReviewStatus.CLARIFICATION_REQUESTED
    else:
        status = ReviewStatus.PENDING_OPTOMETRIST_REVIEW

    is_sufficient = len(turn_history) >= 5 and "q_chief_complaint" in answers

    return FunctionalVisionProfile(
        session_id=session_id,
        patient_name=patient_name,
        patient_age=patient_age,
        patient_gender=patient_gender,
        patient_phone=patient_phone,
        customer_language=language,
        total_questions_asked=len(turn_history),
        distance_vision_status=distance_status,
        intermediate_vision_status={"screen_workload": lifestyle_status["daily_screen_hours"]},
        near_vision_status=near_status,
        lifestyle_occupational_context=lifestyle_status,
        eyewear_history=eyewear_status,
        contradictions=contradictions,
        red_flags=red_flags,
        uncertainty_score=round(uncertainty_score, 3),
        is_sufficient_for_review=is_sufficient,
        review_status=status,
        engine_type=engine_type,
    )
