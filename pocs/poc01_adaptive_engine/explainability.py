"""Explainability and Traceability Module for Nayanee.
"""

from typing import List, Dict, Any
from .models import FunctionalVisionProfile, AnswerRecord


class ExplainabilityReport:
    @staticmethod
    def generate_turn_trace(turn_history: List[AnswerRecord]) -> List[Dict[str, Any]]:
        trace = []
        for turn in turn_history:
            trace.append({
                "turn": turn.turn_index,
                "question_id": turn.question_id,
                "domain": turn.domain.value,
                "selected_option": turn.selected_option,
                "selection_rationale": turn.rationale,
                "transcription_confidence": turn.confidence,
            })
        return trace

    @staticmethod
    def generate_clinical_handover_summary(profile: FunctionalVisionProfile) -> str:
        lines = [
            f"=== NAYANEE FUNCTIONAL VISION INTAKE REPORT ===",
            f"Profile ID: {profile.profile_id} | Session: {profile.session_id}",
            f"Language: {profile.customer_language.value.upper()} | Turns: {profile.total_questions_asked} | Uncertainty: {profile.uncertainty_score}",
            f"Review Status: {profile.review_status.value.upper()}",
            "",
            "1. REPORTED FUNCTIONAL SYMPTOMS:",
            f"  - Distance Vision Clarity: {profile.distance_vision_status.get('clarity_rating', 'unassessed')}",
            f"  - Night Driving Glare: {profile.distance_vision_status.get('night_glare_difficulty', 'unassessed')}",
            f"  - Near Mobile Reading: {profile.near_vision_status.get('mobile_reading_status', 'unassessed')}",
            f"  - Fine Task Fatigue (Asthenopia): {profile.near_vision_status.get('fine_task_fatigue', 'unassessed')}",
            f"  - Presbyopic Indicator: {'YES' if profile.near_vision_status.get('has_presbyopic_indicators') else 'NO'}",
            "",
            "2. OCCUPATIONAL & ENVIRONMENTAL CONTEXT:",
            f"  - Daily Screen Exposure: {profile.lifestyle_occupational_context.get('daily_screen_hours', 'unassessed')}",
            f"  - Digital Visual Fatigue Risk: {'ELEVATED' if profile.lifestyle_occupational_context.get('digital_visual_fatigue_risk') else 'NORMAL'}",
            f"  - Outdoor Sun/Dust Exposure: {profile.lifestyle_occupational_context.get('outdoor_sun_exposure', 'unassessed')}",
            "",
            "3. EYEWEAR & ADAPTATION HISTORY:",
            f"  - Current Eyewear: {profile.eyewear_history.get('current_modality', 'never_worn')}",
            f"  - Age of Current Glasses: {profile.eyewear_history.get('glasses_age', 'n/a')}",
            f"  - Comfort/Satisfaction: {profile.eyewear_history.get('satisfaction_level', 'n/a')}",
        ]

        if profile.contradictions:
            lines.append("")
            lines.append("4. DETECTED CONTRADICTIONS (CLARIFICATION REQUIRED):")
            for idx, c in enumerate(profile.contradictions, 1):
                lines.append(f"  [{idx}] {c.explanation} (Severity: {c.severity.value.upper()})")

        if profile.red_flags:
            lines.append("")
            lines.append("5. CRITICAL RED-FLAG SAFETY ESCALATIONS:")
            for idx, rf in enumerate(profile.red_flags, 1):
                lines.append(f"  🚨 [{idx}] Symptom: {rf.symptom} | Action: {rf.clinical_note}")

        lines.append("")
        lines.append("Clinical Notice: Functional anamnesis profile only. Non-diagnostic. Subject to subjective refraction.")
        return "\n".join(lines)
