"""Optometrist Review & Triage Portal API Routes.
"""

from typing import List, Optional, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pocs.poc01_adaptive_engine.models import (
    FunctionalVisionProfile,
    ReviewStatus,
)
from pocs.poc01_adaptive_engine.lifestyle_advisor import OpticalLifestyleAdvisor
from .session_store import store

router = APIRouter(prefix="/api/v1/profiles", tags=["Optometrist Review"])


class OptometristReviewSubmission(BaseModel):
    reviewer_name: str
    decision: ReviewStatus
    clinical_notes: str
    recommended_action: Optional[str] = None


class ProfileSummaryItem(BaseModel):
    profile_id: str
    session_id: str
    patient_name: str = "Anonymous Patient"
    patient_age: Optional[int] = None
    patient_gender: Optional[str] = None
    language: str
    created_at: str
    total_questions: int
    review_status: str
    has_red_flags: bool
    has_contradictions: bool


class ProfileDetailResponse(BaseModel):
    profile: FunctionalVisionProfile
    lifestyle_guidance: List[Dict[str, str]]


@router.post("/seed-demo", response_model=List[ProfileSummaryItem])
def seed_demo_profiles():
    store._seed_default_cases()
    return list_profiles()


@router.get("", response_model=List[ProfileSummaryItem])
def list_profiles():
    profiles = store.list_profiles()
    summaries = []
    for p in profiles:
        summaries.append(
            ProfileSummaryItem(
                profile_id=p.profile_id,
                session_id=p.session_id,
                patient_name=getattr(p, "patient_name", "Anonymous Patient"),
                patient_age=getattr(p, "patient_age", None),
                patient_gender=getattr(p, "patient_gender", None),
                language=p.customer_language.value,
                created_at=p.created_at,
                total_questions=p.total_questions_asked,
                review_status=p.review_status.value,
                has_red_flags=len(p.red_flags) > 0,
                has_contradictions=len(p.contradictions) > 0,
            )
        )
    return summaries


@router.get("/{profile_id}", response_model=ProfileDetailResponse)
def get_profile(profile_id: str):
    prof = store.get_profile(profile_id)
    if not prof:
        raise HTTPException(status_code=404, detail="Profile not found.")

    guidance = OpticalLifestyleAdvisor.generate_recommendations(prof)
    return ProfileDetailResponse(profile=prof, lifestyle_guidance=guidance)


@router.post("/{profile_id}/review", response_model=FunctionalVisionProfile)
def submit_optometrist_review(profile_id: str, review: OptometristReviewSubmission):
    prof = store.get_profile(profile_id)
    if not prof:
        raise HTTPException(status_code=404, detail="Profile not found.")

    prof.review_status = review.decision
    store.save_profile(prof)
    return prof
