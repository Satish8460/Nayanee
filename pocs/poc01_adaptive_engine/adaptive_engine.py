"""Adaptive Anamnesis Decision Engine.
"""

from typing import List, Dict, Optional, Callable
from .models import (
    Question,
    QuestionCategory,
    FunctionalDomain,
    AnswerRecord,
    ContradictionFlag,
    RedFlagAlert,
    FunctionalVisionProfile,
    LanguageCode,
    SeverityLevel,
    ReviewStatus,
)
from .questions_bank import QUESTIONS, get_question_by_id
from .profile_generator import build_functional_profile


CONTRADICTION_RULES = [
    {
        "q_a": "q_near_mobile_reading",
        "val_a": "cannot_read_near",
        "q_b": "q_fine_task_fatigue",
        "val_b": "never",
        "explanation": "Reported complete inability to read near text, yet claims never experiencing strain or fatigue with near tasks.",
        "severity": SeverityLevel.MODERATE,
    },
    {
        "q_a": "q_dist_clarity",
        "val_a": "never",
        "q_b": "q_chief_complaint",
        "val_b": "distance_blur",
        "explanation": "Chief complaint states distance blur, but reported never having trouble reading distant bus signs or recognizing faces.",
        "severity": SeverityLevel.HIGH,
    },
    {
        "q_a": "q_current_eyewear",
        "val_a": "never_worn",
        "q_b": "q_glasses_age",
        "val_b": "more_than_two_years",
        "explanation": "Reported never wearing glasses, but answered having glasses for more than two years.",
        "severity": SeverityLevel.HIGH,
    },
]


class AdaptiveAnamnesisEngine:
    def __init__(
        self,
        session_id: str,
        language: LanguageCode = LanguageCode.ENGLISH,
        target_confidence_threshold: float = 0.85,
        max_questions: int = 8,
        patient_name: str = "Anonymous Patient",
        patient_age: Optional[int] = None,
        patient_gender: Optional[str] = None,
        patient_phone: Optional[str] = None,
    ):
        self.session_id = session_id
        self.language = language
        self.target_confidence = target_confidence_threshold
        self.max_questions = max_questions
        self.patient_name = patient_name
        self.patient_age = patient_age
        self.patient_gender = patient_gender
        self.patient_phone = patient_phone

        self.answers: Dict[str, AnswerRecord] = {}
        self.turn_history: List[AnswerRecord] = []
        self.contradictions: List[ContradictionFlag] = []
        self.red_flags: List[RedFlagAlert] = []

        self.domain_uncertainty: Dict[FunctionalDomain, float] = {
            FunctionalDomain.DISTANCE: 1.0,
            FunctionalDomain.NEAR: 1.0,
            FunctionalDomain.INTERMEDIATE: 1.0,
            FunctionalDomain.LIFESTYLE: 1.0,
            FunctionalDomain.EYEWEAR: 1.0,
            FunctionalDomain.RED_FLAG: 1.0,
        }

    def is_prerequisite_satisfied(self, question: Question) -> bool:
        if not question.prerequisites:
            return True
        for prereq_qid, allowed_values in question.prerequisites.items():
            if prereq_qid not in self.answers:
                return False
            actual_val = self.answers[prereq_qid].selected_option
            if actual_val not in allowed_values:
                return False
        return True

    def calculate_information_gain(self, question: Question) -> float:
        domain_unc = self.domain_uncertainty.get(question.domain, 0.5)
        chief_complaint = self.answers.get("q_chief_complaint")
        chief_boost = 1.0
        if chief_complaint:
            choice = chief_complaint.selected_option
            if "distance" in choice and question.domain == FunctionalDomain.DISTANCE:
                chief_boost = 1.3
            elif "near" in choice and question.domain == FunctionalDomain.NEAR:
                chief_boost = 1.3

        if question.is_red_flag_probe and "q_acute_symptoms" not in self.answers:
            return 2.5

        return question.base_information_weight * domain_unc * chief_boost

    def check_contradictions(self, new_record: AnswerRecord) -> None:
        for rule in CONTRADICTION_RULES:
            if rule["q_a"] == new_record.question_id:
                if new_record.selected_option == rule["val_a"]:
                    other_rec = self.answers.get(rule["q_b"])
                    if other_rec and other_rec.selected_option == rule["val_b"]:
                        self.contradictions.append(
                            ContradictionFlag(
                                question_id_a=rule["q_a"],
                                answer_a=new_record.selected_option,
                                question_id_b=rule["q_b"],
                                answer_b=other_rec.selected_option,
                                explanation=rule["explanation"],
                                severity=rule["severity"],
                            )
                        )
            elif rule["q_b"] == new_record.question_id:
                if new_record.selected_option == rule["val_b"]:
                    other_rec = self.answers.get(rule["q_a"])
                    if other_rec and other_rec.selected_option == rule["val_a"]:
                        self.contradictions.append(
                            ContradictionFlag(
                                question_id_a=rule["q_a"],
                                answer_a=other_rec.selected_option,
                                question_id_b=rule["q_b"],
                                answer_b=new_record.selected_option,
                                explanation=rule["explanation"],
                                severity=rule["severity"],
                            )
                        )

    def select_next_question(self) -> Optional[Question]:
        if "q_chief_complaint" not in self.answers:
            return get_question_by_id("q_chief_complaint")

        if "q_acute_symptoms" not in self.answers:
            return get_question_by_id("q_acute_symptoms")

        if self.red_flags:
            return None

        if len(self.turn_history) >= self.max_questions:
            return None

        average_uncertainty = sum(self.domain_uncertainty.values()) / len(self.domain_uncertainty)
        if average_uncertainty <= (1.0 - self.target_confidence):
            return None

        candidate_questions = [
            q for q in QUESTIONS
            if q.id not in self.answers and self.is_prerequisite_satisfied(q)
        ]

        if not candidate_questions:
            return None

        scored_candidates = [
            (q, self.calculate_information_gain(q))
            for q in candidate_questions
        ]
        scored_candidates.sort(key=lambda item: item[1], reverse=True)

        return scored_candidates[0][0]

    def record_answer(self, question: Question, answer_choice: str, confidence: float = 1.0) -> AnswerRecord:
        rationale = f"Selected because domain '{question.domain.value}' had remaining uncertainty {self.domain_uncertainty[question.domain]:.2f}."
        
        record = AnswerRecord(
            question_id=question.id,
            category=question.category,
            domain=question.domain,
            selected_option=answer_choice,
            confidence=confidence,
            turn_index=len(self.turn_history) + 1,
            rationale=rationale,
        )

        self.answers[question.id] = record
        self.turn_history.append(record)

        if question.id == "q_acute_symptoms" and answer_choice != "no_acute_symptoms":
            self.red_flags.append(
                RedFlagAlert(
                    symptom=answer_choice,
                    trigger_question_id=question.id,
                    trigger_answer=answer_choice,
                    urgency=SeverityLevel.CRITICAL,
                    clinical_note="Immediate optometrist or ophthalmologist referral required. Do not dispense without medical clearance.",
                )
            )

        self.check_contradictions(record)

        current_unc = self.domain_uncertainty[question.domain]
        decay = 0.55 * question.base_information_weight
        self.domain_uncertainty[question.domain] = max(0.0, current_unc - decay)

        return record

    def run_simulation(self, respondent_oracle: Callable[[Question], str]) -> FunctionalVisionProfile:
        while True:
            next_q = self.select_next_question()
            if not next_q:
                break
            answer = respondent_oracle(next_q)
            self.record_answer(next_q, answer)

        average_uncertainty = sum(self.domain_uncertainty.values()) / len(self.domain_uncertainty)
        
        profile = build_functional_profile(
            session_id=self.session_id,
            language=self.language,
            answers=self.answers,
            turn_history=self.turn_history,
            contradictions=self.contradictions,
            red_flags=self.red_flags,
            uncertainty_score=average_uncertainty,
            engine_type="adaptive",
            patient_name=self.patient_name,
            patient_age=self.patient_age,
            patient_gender=self.patient_gender,
            patient_phone=self.patient_phone,
        )
        return profile
