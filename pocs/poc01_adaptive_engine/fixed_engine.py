"""Baseline Fixed Questionnaire Engine (POC-01 Control Benchmark).
"""

from typing import List, Dict, Callable
from .models import Question, AnswerRecord, FunctionalVisionProfile, LanguageCode
from .questions_bank import QUESTIONS
from .profile_generator import build_functional_profile


class FixedQuestionnaireRunner:
    def __init__(self, session_id: str, language: LanguageCode = LanguageCode.ENGLISH):
        self.session_id = session_id
        self.language = language
        self.answers: Dict[str, AnswerRecord] = {}
        self.turn_history: List[AnswerRecord] = []

    def run(self, respondent_oracle: Callable[[Question], str]) -> FunctionalVisionProfile:
        for turn_idx, question in enumerate(QUESTIONS):
            answer_choice = respondent_oracle(question)
            record = AnswerRecord(
                question_id=question.id,
                category=question.category,
                domain=question.domain,
                selected_option=answer_choice,
                confidence=1.0,
                turn_index=turn_idx + 1,
                rationale="Fixed sequential questionnaire order.",
            )
            self.answers[question.id] = record
            self.turn_history.append(record)

        profile = build_functional_profile(
            session_id=self.session_id,
            language=self.language,
            answers=self.answers,
            turn_history=self.turn_history,
            engine_type="fixed_baseline",
        )
        return profile
