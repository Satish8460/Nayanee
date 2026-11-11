"""Speech Provider Abstraction Interfaces for POC-02.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class ProviderTier(str, Enum):
    TIER_1_CLOUD_INDIC = "tier_1_cloud_indic"
    TIER_2_BROWSER_LOCAL = "tier_2_browser_local"
    TIER_3_TEXT_FALLBACK = "tier_3_text_fallback"


class ASRResult(BaseModel):
    raw_transcript: str
    normalized_transcript: str
    language_code: str
    confidence: float = Field(ge=0.0, le=1.0)
    provider_used: ProviderTier
    latency_ms: float
    is_code_mixed: bool = False
    detected_entities: List[str] = Field(default_factory=list)
    requires_confirmation: bool = False


class TTSResult(BaseModel):
    audio_format: str
    audio_data_bytes: Optional[bytes] = None
    language_code: str
    provider_used: ProviderTier
    latency_ms: float
    fallback_applied: bool = False


class BaseASRProvider(ABC):
    @abstractmethod
    def transcribe(self, audio_bytes: bytes, language_code: str) -> ASRResult:
        pass


class BaseTTSProvider(ABC):
    @abstractmethod
    def synthesize(self, text: str, language_code: str) -> TTSResult:
        pass
