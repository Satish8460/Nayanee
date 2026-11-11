"""Simulated Multi-Tier Speech Providers for POC-02.
"""

import random
from .provider_interface import BaseASRProvider, BaseTTSProvider, ASRResult, TTSResult, ProviderTier
from .language_registry import get_language_metadata


class SimulatedIndicASRProvider(BaseASRProvider):
    def __init__(self, simulate_network_failure: bool = False, base_latency_ms: float = 280.0):
        self.simulate_network_failure = simulate_network_failure
        self.base_latency_ms = base_latency_ms

    def transcribe(self, audio_bytes: bytes, language_code: str) -> ASRResult:
        if self.simulate_network_failure:
            raise ConnectionError("Tier 1 Cloud Indic ASR unreachable.")

        meta = get_language_metadata(language_code)
        raw_text = audio_bytes.decode("utf-8", errors="ignore") or "sample utterance"
        
        is_code_mixed = any(word.lower() in raw_text.lower() for word in meta.code_mixed_loanwords)
        detected_entities = [word for word in meta.code_mixed_loanwords if word.lower() in raw_text.lower()]
        confidence = 0.92 if not is_code_mixed else 0.86

        return ASRResult(
            raw_transcript=raw_text,
            normalized_transcript=raw_text.strip().lower(),
            language_code=language_code,
            confidence=confidence,
            provider_used=ProviderTier.TIER_1_CLOUD_INDIC,
            latency_ms=self.base_latency_ms + random.uniform(10.0, 50.0),
            is_code_mixed=is_code_mixed,
            detected_entities=detected_entities,
            requires_confirmation=confidence < 0.75,
        )


class SimulatedBrowserLocalASRProvider(BaseASRProvider):
    def __init__(self, base_latency_ms: float = 85.0):
        self.base_latency_ms = base_latency_ms

    def transcribe(self, audio_bytes: bytes, language_code: str) -> ASRResult:
        raw_text = audio_bytes.decode("utf-8", errors="ignore") or "local utterance"
        confidence = 0.74 if language_code == "en" else 0.68
        
        return ASRResult(
            raw_transcript=raw_text,
            normalized_transcript=raw_text.strip().lower(),
            language_code=language_code,
            confidence=confidence,
            provider_used=ProviderTier.TIER_2_BROWSER_LOCAL,
            latency_ms=self.base_latency_ms,
            is_code_mixed=False,
            requires_confirmation=confidence < 0.75,
        )


class SimulatedTTSProvider(BaseTTSProvider):
    def __init__(self, simulate_failure: bool = False):
        self.simulate_failure = simulate_failure

    def synthesize(self, text: str, language_code: str) -> TTSResult:
        if self.simulate_failure:
            raise RuntimeError("TTS voice synthesis failed.")

        mock_audio = f"[AUDIO_DATA_FOR_LANG_{language_code}:{text[:20]}]".encode("utf-8")
        
        return TTSResult(
            audio_format="audio/wav",
            audio_data_bytes=mock_audio,
            language_code=language_code,
            provider_used=ProviderTier.TIER_1_CLOUD_INDIC,
            latency_ms=180.0,
            fallback_applied=False,
        )
