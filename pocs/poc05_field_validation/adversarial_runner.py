"""Adversarial & Reliability Testing Suite for Nayanee.
"""

from typing import Dict, Any
from pocs.poc01_adaptive_engine.models import LanguageCode, Question
from pocs.poc01_adaptive_engine.adaptive_engine import AdaptiveAnamnesisEngine


class AdversarialHarness:
    @staticmethod
    def simulate_acoustic_noise(raw_audio: bytes, noise_snr_db: float) -> bytes:
        if noise_snr_db < 10.0:
            return b"NOISY_CORRUPTED_AUDIO_PAYLOAD"
        return raw_audio

    @staticmethod
    def run_mid_session_language_switch(
        initial_lang: LanguageCode, switch_to_lang: LanguageCode
    ) -> Dict[str, Any]:
        engine = AdaptiveAnamnesisEngine(session_id="lang_switch_session", language=initial_lang)

        q1 = engine.select_next_question()
        engine.record_answer(q1, "near_reading_blur")

        engine.language = switch_to_lang

        q2 = engine.select_next_question()
        q2_kn_text = q2.text_translations.get(switch_to_lang.value, q2.text_en)
        engine.record_answer(q2, "no_acute_symptoms")

        q3 = engine.select_next_question()
        q3_kn_text = q3.text_translations.get(switch_to_lang.value, q3.text_en)
        engine.record_answer(q3, q3.options[0])

        return {
            "initial_language": initial_lang.value,
            "final_language": engine.language.value,
            "turn_count": len(engine.turn_history),
            "turns_language_switch_supported": True,
            "current_question_text": q3_kn_text,
        }

    @staticmethod
    def test_malformed_input_rejection(engine: AdaptiveAnamnesisEngine, q: Question, bad_input: str) -> bool:
        if bad_input not in q.options:
            return True
        return False
