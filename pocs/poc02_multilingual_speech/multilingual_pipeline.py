"""Multilingual Conversational Speech Pipeline Orchestrator.
"""

from typing import Optional, Tuple
from .provider_interface import BaseASRProvider, BaseTTSProvider, ASRResult, TTSResult, ProviderTier
from .language_registry import get_language_metadata, LANGUAGE_REGISTRY


class MultilingualSpeechPipeline:
    def __init__(
        self,
        primary_asr: BaseASRProvider,
        secondary_asr: BaseASRProvider,
        tts_provider: BaseTTSProvider,
        confidence_threshold: float = 0.75,
    ):
        self.primary_asr = primary_asr
        self.secondary_asr = secondary_asr
        self.tts_provider = tts_provider
        self.confidence_threshold = confidence_threshold

    def process_incoming_audio(
        self, audio_bytes: bytes, language_code: str
    ) -> Tuple[ASRResult, Optional[str]]:
        if language_code not in LANGUAGE_REGISTRY:
            raise ValueError(f"Language {language_code} not supported.")

        meta = get_language_metadata(language_code)

        try:
            asr_res = self.primary_asr.transcribe(audio_bytes, language_code)
        except Exception:
            asr_res = self.secondary_asr.transcribe(audio_bytes, language_code)

        confirmation_prompt = None
        if asr_res.confidence < self.confidence_threshold:
            asr_res.requires_confirmation = True
            confirmation_prompt = meta.sample_confirmation_prompt.format(
                transcript=asr_res.raw_transcript
            )

        return asr_res, confirmation_prompt

    def synthesize_question(self, text: str, language_code: str) -> TTSResult:
        try:
            return self.tts_provider.synthesize(text, language_code)
        except Exception:
            return TTSResult(
                audio_format="text_fallback",
                audio_data_bytes=None,
                language_code=language_code,
                provider_used=ProviderTier.TIER_3_TEXT_FALLBACK,
                latency_ms=1.0,
                fallback_applied=True,
            )
