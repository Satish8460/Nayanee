"""Benchmark suite comparing Fixed vs Adaptive Anamnesis Engines (POC-01).
"""

import time
from typing import Dict, Any
from .models import Question, LanguageCode
from .fixed_engine import FixedQuestionnaireRunner
from .adaptive_engine import AdaptiveAnamnesisEngine


def persona_presbyope_first_timer(q: Question) -> str:
    mapping = {
        "q_chief_complaint": "near_reading_blur",
        "q_acute_symptoms": "no_acute_symptoms",
        "q_near_mobile_reading": "significant_blur_holds_far",
        "q_fine_task_fatigue": "frequently",
        "q_dist_clarity": "never",
        "q_night_driving_glare": "not_applicable",
        "q_intermediate_screen": "zero_to_one",
        "q_outdoor_exposure": "one_to_three_hours_outdoors",
        "q_current_eyewear": "never_worn",
        "q_glasses_age": "less_than_one_year",
        "q_glasses_satisfaction": "very_comfortable",
    }
    return mapping.get(q.id, q.options[0])


def persona_digital_screen_worker(q: Question) -> str:
    mapping = {
        "q_chief_complaint": "distance_blur",
        "q_acute_symptoms": "no_acute_symptoms",
        "q_dist_clarity": "often",
        "q_night_driving_glare": "moderate_glare",
        "q_near_mobile_reading": "clear_at_normal_distance",
        "q_fine_task_fatigue": "occasionally",
        "q_intermediate_screen": "more_than_eight",
        "q_outdoor_exposure": "mostly_indoors",
        "q_current_eyewear": "distance_only",
        "q_glasses_age": "more_than_two_years",
        "q_glasses_satisfaction": "slightly_blurred_or_strained",
    }
    return mapping.get(q.id, q.options[0])


def persona_acute_red_flag(q: Question) -> str:
    mapping = {
        "q_chief_complaint": "sudden_vision_change",
        "q_acute_symptoms": "flashes_or_floaters",
        "q_dist_clarity": "often",
    }
    return mapping.get(q.id, q.options[0])


def persona_contradictory_patient(q: Question) -> str:
    mapping = {
        "q_chief_complaint": "distance_blur",
        "q_acute_symptoms": "no_acute_symptoms",
        "q_dist_clarity": "never",
        "q_near_mobile_reading": "cannot_read_near",
        "q_fine_task_fatigue": "never",
        "q_current_eyewear": "never_worn",
    }
    return mapping.get(q.id, q.options[0])


def run_benchmark_comparison() -> Dict[str, Any]:
    scenarios = [
        ("Presbyope First-Timer", persona_presbyope_first_timer),
        ("Digital Screen Worker", persona_digital_screen_worker),
        ("Acute Red-Flag Patient", persona_acute_red_flag),
        ("Contradictory Patient", persona_contradictory_patient),
    ]

    results = []

    for name, oracle in scenarios:
        t0 = time.perf_counter()
        fixed_runner = FixedQuestionnaireRunner(session_id=f"fixed_{name.lower().replace(' ', '_')}")
        fixed_profile = fixed_runner.run(oracle)
        t_fixed = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        adaptive_runner = AdaptiveAnamnesisEngine(session_id=f"adaptive_{name.lower().replace(' ', '_')}")
        adaptive_profile = adaptive_runner.run_simulation(oracle)
        t_adaptive = (time.perf_counter() - t0) * 1000

        reduction_pct = (
            (fixed_profile.total_questions_asked - adaptive_profile.total_questions_asked)
            / fixed_profile.total_questions_asked
            * 100.0
        )

        results.append({
            "scenario": name,
            "fixed_questions": fixed_profile.total_questions_asked,
            "adaptive_questions": adaptive_profile.total_questions_asked,
            "question_reduction_pct": round(reduction_pct, 1),
            "fixed_time_ms": round(t_fixed, 3),
            "adaptive_time_ms": round(t_adaptive, 3),
            "contradictions_detected": len(adaptive_profile.contradictions),
            "red_flags_detected": len(adaptive_profile.red_flags),
            "review_status": adaptive_profile.review_status.value,
        })

    return {"benchmark_summary": results}


if __name__ == "__main__":
    import json
    res = run_benchmark_comparison()
    print(json.dumps(res, indent=2))
