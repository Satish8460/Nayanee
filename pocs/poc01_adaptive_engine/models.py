"""Data models for POC-01 Adaptive Anamnesis Engine.
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
import uuid
from datetime import datetime, timezone


class LanguageCode(str, Enum):
    KANNADA = "kn"
    HINDI = "hi"
    TAMIL = "ta"
    TELUGU = "te"
    MALAYALAM = "ml"
    ENGLISH = "en"


class QuestionCategory(str, Enum):
    CHIEF_COMPLAINT = "chief_complaint"
    DISTANCE_VISION = "distance_vision"
    INTERMEDIATE_VISION = "intermediate_vision"
    NEAR_VISION = "near_vision"
    LIFESTYLE_OCCUPATION = "lifestyle_occupation"
    EYEWEAR_HISTORY = "eyewear_history"
    RED_FLAG_SAFETY = "red_flag_safety"
    CLARIFICATION = "clarification"


class FunctionalDomain(str, Enum):
    DISTANCE = "distance"
    INTERMEDIATE = "intermediate"
    NEAR = "near"
    LIFESTYLE = "lifestyle"
    EYEWEAR = "eyewear"
    RED_FLAG = "red_flag"


class SeverityLevel(str, Enum):
    NONE = "none"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class ReviewStatus(str, Enum):
    DRAFT = "draft"
    PENDING_OPTOMETRIST_REVIEW = "pending_optometrist_review"
    REVIEWED_APPROVED = "reviewed_approved"
    CLARIFICATION_REQUESTED = "clarification_requested"
    URGENT_MEDICAL_ESCALATION = "urgent_medical_escalation"


class Question(BaseModel):
    id: str
    category: QuestionCategory
    domain: FunctionalDomain
    text_en: str
    text_translations: Dict[str, str] = Field(default_factory=dict)
    options: List[str]
    options_translations: Dict[str, Dict[str, str]] = Field(default_factory=dict)
    prerequisites: Dict[str, Any] = Field(default_factory=dict)
    base_information_weight: float = 0.5
    is_red_flag_probe: bool = False


class AnswerRecord(BaseModel):
    question_id: str
    category: QuestionCategory
    domain: FunctionalDomain
    selected_option: str
    confidence: float = 1.0
    turn_index: int
    rationale: Optional[str] = None


class ContradictionFlag(BaseModel):
    question_id_a: str
    answer_a: str
    question_id_b: str
    answer_b: str
    explanation: str
    severity: SeverityLevel = SeverityLevel.MODERATE


class RedFlagAlert(BaseModel):
    symptom: str
    trigger_question_id: str
    trigger_answer: str
    urgency: SeverityLevel = SeverityLevel.CRITICAL
    clinical_note: str


class FunctionalVisionProfile(BaseModel):
    profile_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    patient_name: str = "Anonymous Patient"
    patient_age: Optional[int] = None
    patient_gender: Optional[str] = None
    patient_phone: Optional[str] = None
    customer_language: LanguageCode
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    total_questions_asked: int
    
    distance_vision_status: Dict[str, Any] = Field(default_factory=dict)
    intermediate_vision_status: Dict[str, Any] = Field(default_factory=dict)
    near_vision_status: Dict[str, Any] = Field(default_factory=dict)
    lifestyle_occupational_context: Dict[str, Any] = Field(default_factory=dict)
    eyewear_history: Dict[str, Any] = Field(default_factory=dict)
    
    contradictions: List[ContradictionFlag] = Field(default_factory=list)
    red_flags: List[RedFlagAlert] = Field(default_factory=list)
    uncertainty_score: float = 0.0
    is_sufficient_for_review: bool = False
    review_status: ReviewStatus = ReviewStatus.PENDING_OPTOMETRIST_REVIEW
    engine_type: str = "adaptive"
