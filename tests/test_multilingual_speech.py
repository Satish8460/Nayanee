"""Unit tests for POC-02: Multilingual Speech Pipeline.
"""

from pocs.poc02_multilingual_speech.provider_interface import ProviderTier
from pocs.poc02_multilingual_speech.language_registry import LANGUAGE_REGISTRY, get_language_metadata
from pocs.poc02_multilingual_speech.mock_providers import (
    SimulatedIndicASRProvider,
    SimulatedBrowserLocalASRProvider,
    SimulatedTTSProvider,
)
from pocs.poc02_multilingual_speech.multilingual_pipeline import MultilingualSpeechPipeline


ALL_6_LANGUAGES = ["kn", "hi", "ta", "te", "ml", "en"]


def test_six_languages_registry_complete():
    for lang in ALL_6_LANGUAGES:
        assert lang in LANGUAGE_REGISTRY
        meta = get_language_metadata(lang)
        assert len(meta.autonym) > 0
        assert "{transcript}" in meta.sample_confirmation_prompt
        assert len(meta.common_optical_keywords) >= 5


def test_primary_speech_pipeline_transcription():
    primary_asr = SimulatedIndicASRProvider()
    secondary_asr = SimulatedBrowserLocalASRProvider()
    tts = SimulatedTTSProvider()
    pipeline = MultilingualSpeechPipeline(primary_asr, secondary_asr, tts)

    kn_audio = "ನನಗೆ ಮೊಬೈಲ್ ಓದಲು ಕಷ್ಟ ಆಗುತ್ತಿದೆ".encode("utf-8")
    res, confirm = pipeline.process_incoming_audio(kn_audio, "kn")
    assert res.language_code == "kn"
    assert res.provider_used == ProviderTier.TIER_1_CLOUD_INDIC
    assert res.confidence >= 0.85
    assert confirm is None

    hi_audio = "मुझे दूर का साइनबोर्ड नहीं दिखता".encode("utf-8")
    res, confirm = pipeline.process_incoming_audio(hi_audio, "hi")
    assert res.language_code == "hi"
    assert res.provider_used == ProviderTier.TIER_1_CLOUD_INDIC
    assert res.confidence >= 0.85


def test_code_mixing_detection():
    primary_asr = SimulatedIndicASRProvider()
    secondary_asr = SimulatedBrowserLocalASRProvider()
    tts = SimulatedTTSProvider()
    pipeline = MultilingualSpeechPipeline(primary_asr, secondary_asr, tts)

    audio = "ನಾನು mobile ಮತ್ತು reading ಮಾಡುವಾಗ headache ಬರುತ್ತದೆ".encode("utf-8")
    res, _ = pipeline.process_incoming_audio(audio, "kn")
    assert res.is_code_mixed is True
    assert "mobile" in res.detected_entities or "reading" in res.detected_entities


def test_tier1_failure_falls_back_to_tier2():
    failing_primary = SimulatedIndicASRProvider(simulate_network_failure=True)
    secondary_asr = SimulatedBrowserLocalASRProvider()
    tts = SimulatedTTSProvider()
    pipeline = MultilingualSpeechPipeline(failing_primary, secondary_asr, tts)

    audio = "கண்ணாடி போட்டு படிக்கும் போது மங்கலாக உள்ளது".encode("utf-8")
    res, confirm = pipeline.process_incoming_audio(audio, "ta")

    assert res.provider_used == ProviderTier.TIER_2_BROWSER_LOCAL
    assert res.confidence < 0.75
    assert res.requires_confirmation is True
    assert confirm is not None
    assert "நீங்கள் கூறியது:" in confirm


def test_tts_synthesis_and_fallback():
    primary_asr = SimulatedIndicASRProvider()
    secondary_asr = SimulatedBrowserLocalASRProvider()
    
    tts_ok = SimulatedTTSProvider(simulate_failure=False)
    pipeline_ok = MultilingualSpeechPipeline(primary_asr, secondary_asr, tts_ok)
    tts_res = pipeline_ok.synthesize_question("నమస్కారం", "te")
    assert tts_res.provider_used == ProviderTier.TIER_1_CLOUD_INDIC
    assert tts_res.fallback_applied is False
    assert tts_res.audio_data_bytes is not None

    tts_failing = SimulatedTTSProvider(simulate_failure=True)
    pipeline_fallback = MultilingualSpeechPipeline(primary_asr, secondary_asr, tts_failing)
    tts_res_fb = pipeline_fallback.synthesize_question("നമസ്കാരം", "ml")
    assert tts_res_fb.provider_used == ProviderTier.TIER_3_TEXT_FALLBACK
    assert tts_res_fb.fallback_applied is True
    assert tts_res_fb.audio_format == "text_fallback"
