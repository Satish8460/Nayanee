"""Thread-safe In-Memory Session and Profile Store for Nayanee.
"""

import threading
from typing import Dict, Optional, List
from pocs.poc01_adaptive_engine.models import (
    FunctionalVisionProfile,
    LanguageCode,
    ReviewStatus,
    ContradictionFlag,
    RedFlagAlert,
    SeverityLevel,
)
from pocs.poc01_adaptive_engine.adaptive_engine import AdaptiveAnamnesisEngine


class SessionStore:
    def __init__(self):
        self._lock = threading.Lock()
        self._active_engines: Dict[str, AdaptiveAnamnesisEngine] = {}
        self._finalized_profiles: Dict[str, FunctionalVisionProfile] = {}
        self._seed_default_cases()

    def save_engine(self, session_id: str, engine: AdaptiveAnamnesisEngine) -> None:
        with self._lock:
            self._active_engines[session_id] = engine

    def get_engine(self, session_id: str) -> Optional[AdaptiveAnamnesisEngine]:
        with self._lock:
            return self._active_engines.get(session_id)

    def save_profile(self, profile: FunctionalVisionProfile) -> None:
        with self._lock:
            self._finalized_profiles[profile.profile_id] = profile

    def get_profile(self, profile_id: str) -> Optional[FunctionalVisionProfile]:
        with self._lock:
            return self._finalized_profiles.get(profile_id)

    def get_profile_by_session(self, session_id: str) -> Optional[FunctionalVisionProfile]:
        with self._lock:
            for prof in self._finalized_profiles.values():
                if prof.session_id == session_id:
                    return prof
            return None

    def list_profiles(self) -> List[FunctionalVisionProfile]:
        with self._lock:
            return list(self._finalized_profiles.values())

    def clear(self) -> None:
        with self._lock:
            self._active_engines.clear()
            self._finalized_profiles.clear()

    def _seed_default_cases(self) -> None:
        p1 = FunctionalVisionProfile(
            profile_id="demo-kn-parvathamma",
            session_id="sess-demo-01",
            patient_name="Parvathamma B.",
            patient_age=62,
            patient_gender="Female",
            customer_language=LanguageCode.KANNADA,
            total_questions_asked=8,
            distance_vision_status={"clarity_rating": "never", "night_glare_difficulty": "not_applicable", "has_distance_complaint": False},
            intermediate_vision_status={"screen_workload": "zero_to_one"},
            near_vision_status={"mobile_reading_status": "significant_blur_holds_far", "fine_task_fatigue": "frequently", "has_presbyopic_indicators": True},
            lifestyle_occupational_context={"daily_screen_hours": "zero_to_one", "outdoor_sun_exposure": "one_to_three_hours_outdoors", "digital_visual_fatigue_risk": False},
            eyewear_history={"current_modality": "never_worn", "glasses_age": "n/a", "satisfaction_level": "n/a"},
            review_status=ReviewStatus.PENDING_OPTOMETRIST_REVIEW,
            uncertainty_score=0.15,
            is_sufficient_for_review=True,
        )
        self._finalized_profiles[p1.profile_id] = p1

        p2 = FunctionalVisionProfile(
            profile_id="demo-hi-rajesh-screen",
            session_id="sess-demo-02",
            patient_name="Rajesh Kumar",
            patient_age=34,
            patient_gender="Male",
            customer_language=LanguageCode.HINDI,
            total_questions_asked=9,
            distance_vision_status={"clarity_rating": "often", "night_glare_difficulty": "moderate_glare", "has_distance_complaint": True},
            intermediate_vision_status={"screen_workload": "more_than_eight"},
            near_vision_status={"mobile_reading_status": "clear_at_normal_distance", "fine_task_fatigue": "occasionally", "has_presbyopic_indicators": False},
            lifestyle_occupational_context={"daily_screen_hours": "more_than_eight", "outdoor_sun_exposure": "mostly_indoors", "digital_visual_fatigue_risk": True},
            eyewear_history={"current_modality": "distance_only", "glasses_age": "more_than_two_years", "satisfaction_level": "slightly_blurred_or_strained"},
            review_status=ReviewStatus.PENDING_OPTOMETRIST_REVIEW,
            uncertainty_score=0.12,
            is_sufficient_for_review=True,
        )
        self._finalized_profiles[p2.profile_id] = p2

        p3 = FunctionalVisionProfile(
            profile_id="demo-ta-muthuvel-contra",
            session_id="sess-demo-03",
            patient_name="Muthuvel S.",
            patient_age=48,
            patient_gender="Male",
            customer_language=LanguageCode.TAMIL,
            total_questions_asked=8,
            distance_vision_status={"clarity_rating": "never", "night_glare_difficulty": "not_applicable", "has_distance_complaint": True},
            intermediate_vision_status={"screen_workload": "two_to_four"},
            near_vision_status={"mobile_reading_status": "cannot_read_near", "fine_task_fatigue": "never", "has_presbyopic_indicators": True},
            lifestyle_occupational_context={"daily_screen_hours": "two_to_four", "outdoor_sun_exposure": "mostly_indoors", "digital_visual_fatigue_risk": False},
            eyewear_history={"current_modality": "never_worn", "glasses_age": "n/a", "satisfaction_level": "n/a"},
            contradictions=[
                ContradictionFlag(
                    question_id_a="q_dist_clarity",
                    answer_a="never",
                    question_id_b="q_chief_complaint",
                    answer_b="distance_blur",
                    explanation="Chief complaint states distance blur, but reported never having trouble reading distant signs or recognizing faces.",
                    severity=SeverityLevel.HIGH,
                )
            ],
            review_status=ReviewStatus.CLARIFICATION_REQUESTED,
            uncertainty_score=0.22,
            is_sufficient_for_review=True,
        )
        self._finalized_profiles[p3.profile_id] = p3

        p4 = FunctionalVisionProfile(
            profile_id="demo-te-srinivas-redflag",
            session_id="sess-demo-04",
            patient_name="Srinivas Rao",
            patient_age=56,
            patient_gender="Male",
            customer_language=LanguageCode.TELUGU,
            total_questions_asked=2,
            distance_vision_status={"clarity_rating": "unassessed", "night_glare_difficulty": "unassessed", "has_distance_complaint": False},
            near_vision_status={"mobile_reading_status": "unassessed", "fine_task_fatigue": "unassessed", "has_presbyopic_indicators": False},
            lifestyle_occupational_context={"daily_screen_hours": "unassessed", "outdoor_sun_exposure": "unassessed", "digital_visual_fatigue_risk": False},
            eyewear_history={"current_modality": "never_worn", "glasses_age": "n/a", "satisfaction_level": "n/a"},
            red_flags=[
                RedFlagAlert(
                    symptom="flashes_or_floaters",
                    trigger_question_id="q_acute_symptoms",
                    trigger_answer="flashes_or_floaters",
                    urgency=SeverityLevel.CRITICAL,
                    clinical_note="Urgent retinal tear/detachment suspicion. Immediate ophthalmologist evaluation required before any optical dispensing.",
                )
            ],
            review_status=ReviewStatus.URGENT_MEDICAL_ESCALATION,
            uncertainty_score=0.85,
            is_sufficient_for_review=False,
        )
        self._finalized_profiles[p4.profile_id] = p4


store = SessionStore()
