"""ZEISS Lens & Coating Recommendation Engine for Nayanee.
Deterministic, multi-factor optical decision engine matching walk-in functional
vision profiles to ZEISS ophthalmic lens and coating portfolios.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from pocs.poc01_adaptive_engine.models import FunctionalVisionProfile


@dataclass
class ZeissLensRecommendation:
    primary_lens: str
    lens_family: str
    recommended_coating: str
    recommended_index: str
    corridor_or_boost: Optional[str]
    patient_explanation: str
    optician_dispensing_notes: str
    lifestyle_triggers: List[str] = field(default_factory=list)


class ZeissLensRecommender:
    """Deterministic expert matching matrix for the ZEISS ophthalmic portfolio."""

    @classmethod
    def recommend(
        cls,
        profile: FunctionalVisionProfile,
        onscreen_test_results: Optional[Dict[str, Any]] = None,
    ) -> ZeissLensRecommendation:
        triggers: List[str] = []
        age = profile.patient_age or 35

        # 1. Extract functional indicators
        near_status = profile.near_vision_status.get("mobile_reading_status", "")
        screen_hours = profile.lifestyle_occupational_context.get("daily_screen_hours", "")
        glare_difficulty = profile.distance_vision_status.get("night_glare_difficulty", "")
        outdoor_sun = profile.lifestyle_occupational_context.get("outdoor_sun_exposure", "")
        dist_clarity = profile.distance_vision_status.get("distance_clarity_status", "")

        is_presbyope = (
            age >= 42
            or near_status in ["significant_blur_holds_far", "cannot_read_near"]
        )
        is_heavy_screen = screen_hours in ["five_to_eight", "more_than_eight"]
        is_night_glare = glare_difficulty in ["moderate_glare", "severe_glare_avoids_driving"]
        is_outdoor_heavy = outdoor_sun in ["majority_outdoors_heavy_sun", "one_to_three_hours_outdoors"]

        # Track triggers
        if is_presbyope:
            triggers.append(f"Presbyopic reading blur at age {age}")
        if is_heavy_screen:
            triggers.append(f"Heavy digital screen workload ({screen_hours.replace('_', ' ')} hrs/day)")
        if is_night_glare:
            triggers.append(f"Night driving glare and reduced mesopic contrast")
        if is_outdoor_heavy:
            triggers.append(f"Active outdoor UV and bright sunlight exposure")

        # 2. Determine Primary Lens & Family
        if is_presbyope:
            lens_family = "ZEISS Progressive Portfolio"
            if is_heavy_screen:
                primary_lens = "ZEISS SmartLife Progressive (Near Priority)"
                corridor = "Near/Intermediate Corridor Priority (Customized for digital multitasking)"
                patient_exp = (
                    "Designed for adults experiencing natural reading difficulty. Provides smooth, "
                    "seamless focus from phone screens to across the room without lines."
                )
            else:
                primary_lens = "ZEISS Progressive Light 3D"
                corridor = "Balanced Universal Progression Corridor"
                patient_exp = (
                    "Effortless transition across all distances (near, intermediate, far) "
                    "with wide, clear reading zones for first-time progressive wearers."
                )
            dispensing_notes = (
                "Verify pupil center height and monocular fitting heights in chosen frame. "
                "Ensure minimum fitting height >= 14mm."
            )

        elif is_heavy_screen and age < 42:
            lens_family = "ZEISS Digital Lens Portfolio"
            primary_lens = "ZEISS Digital Lenses"
            boost_power = "+0.75D" if age >= 32 else "+0.50D"
            corridor = f"Accommodative Relief Boost ({boost_power})"
            patient_exp = (
                "Specifically engineered for smartphone and computer users. Eases eye strain "
                "and end-of-day fatigue by providing a gentle focus boost in the lower lens area."
            )
            dispensing_notes = (
                f"Prescribe targeted accommodative relief ({boost_power}). Verify optical center at pupil."
            )

        elif is_night_glare and not is_presbyope:
            lens_family = "ZEISS DriveSafe Portfolio"
            primary_lens = "ZEISS DriveSafe Single Vision"
            corridor = "Luminance Design Optimized Optics"
            patient_exp = (
                "Engineered for clear vision in challenging light, dusk, and night driving. "
                "Significantly minimizes blinding glare from incoming modern LED/xenon headlights."
            )
            dispensing_notes = (
                "Luminance Design pupil-optimized optics. Advise customer on high-contrast twilight clarity."
            )

        else:
            lens_family = "ZEISS ClearView Single Vision Portfolio"
            primary_lens = "ZEISS Single Vision ClearView"
            corridor = "Freeform Point-by-Point Optimized"
            patient_exp = (
                "Delivers up to 3x larger zones of crystal-clear vision compared to standard "
                "stock lenses, with a modern ultra-flat and thin profile."
            )
            dispensing_notes = (
                "Stock freeform single vision. Fit standard optical center."
            )

        # 3. Determine Recommended Coating
        if is_night_glare:
            coating = "ZEISS DuraVision DriveSafe"
        elif is_heavy_screen:
            coating = "ZEISS DuraVision BlueProtect (400–455nm Selective Filter)"
        elif is_outdoor_heavy:
            coating = "ZEISS PhotoFusion X (Fast Variable Tint) + DuraVision Platinum"
        else:
            coating = "ZEISS DuraVision Platinum UV (Ultra-Hard Scratch Resistance + Anti-Static)"

        # 4. Determine Recommended Index
        if is_presbyope and is_heavy_screen:
            rec_index = "1.60 High Index (Thin & Lightweight)"
        elif is_outdoor_heavy:
            rec_index = "1.60 Impact-Resistant (Extra Durability)"
        else:
            rec_index = "1.56 / 1.60 Clarity Index"

        # 5. Factor in On-Screen Test Results if available
        if onscreen_test_results:
            astig_finding = onscreen_test_results.get("astigmatic_dial", {})
            if astig_finding.get("astigmatism_suspected"):
                dispensing_notes += (
                    f" [ASTIGMATIC ALERT: Dial test flagged {astig_finding.get('dominant_meridian')} "
                    f"meridian. Perform full Jackson Cross-Cylinder check.]"
                )

            duochrome = onscreen_test_results.get("duochrome", {})
            if duochrome.get("tendency"):
                dispensing_notes += f" [DUOCHROME PRE-REFRACTION: {duochrome.get('tendency')}]."

        return ZeissLensRecommendation(
            primary_lens=primary_lens,
            lens_family=lens_family,
            recommended_coating=coating,
            recommended_index=rec_index,
            corridor_or_boost=corridor,
            patient_explanation=patient_exp,
            optician_dispensing_notes=dispensing_notes,
            lifestyle_triggers=triggers,
        )
