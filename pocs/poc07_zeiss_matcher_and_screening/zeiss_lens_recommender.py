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
    progressive_adaptation_risk: Dict[str, Any] = field(default_factory=dict)


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
        dryness_status = profile.near_vision_status.get("ocular_surface_dryness", "")
        screen_hours = profile.lifestyle_occupational_context.get("daily_screen_hours", "")
        glare_difficulty = profile.distance_vision_status.get("night_glare_difficulty", "")
        outdoor_sun = profile.lifestyle_occupational_context.get("outdoor_sun_exposure", "")
        dist_clarity = profile.distance_vision_status.get("distance_clarity_status", "")
        ergo_plane = profile.ergonomic_task_profile.get("primary_focal_plane", "")
        commute_mode = profile.transit_environmental_vector.get("commute_mode", "")
        gender = (profile.patient_gender or "").lower().strip()

        is_presbyope = (
            age >= 42
            or near_status in ["significant_blur_holds_far", "cannot_read_near"]
        )
        is_heavy_screen = screen_hours in ["five_to_eight", "more_than_eight"]
        is_night_glare = glare_difficulty in ["moderate_glare", "severe_glare_avoids_driving"]
        is_outdoor_heavy = outdoor_sun in ["majority_outdoors_heavy_sun", "one_to_three_hours_outdoors"]
        is_two_wheeler = commute_mode == "two_wheeler_bike"

        # Track triggers
        if is_presbyope:
            triggers.append(f"Presbyopic reading blur at age {age}")
        if is_heavy_screen:
            triggers.append(f"Heavy digital screen workload ({screen_hours.replace('_', ' ')} hrs/day)")
        if is_night_glare:
            triggers.append(f"Night driving glare and reduced mesopic contrast")
        if is_outdoor_heavy:
            triggers.append(f"Active outdoor UV and bright sunlight exposure")
        if is_two_wheeler:
            triggers.append("Daily two-wheeler commuter exposed to open wind, dust, and oncoming LED headlights")

        # 2. Determine Primary Lens & Family & Corridor
        if is_presbyope:
            lens_family = "ZEISS Progressive Portfolio"
            if is_heavy_screen:
                primary_lens = "ZEISS SmartLife Progressive (Near Priority)"
                if ergo_plane == "handheld_mobile_close" or gender == "female":
                    corridor = "Short Corridor 14mm (Rapid Mobile & Female Arm Reach 33cm)"
                    triggers.append("Closer reading posture (< 35cm) tailored with 14mm corridor")
                else:
                    corridor = "Near/Intermediate Corridor Priority (Customized for digital multitasking)"
                patient_exp = (
                    "Designed for adults experiencing natural reading difficulty. Provides smooth, "
                    "seamless focus from phone screens to across the room without lines."
                )
            else:
                primary_lens = "ZEISS Progressive Light 3D"
                if ergo_plane == "desktop_monitor_desk":
                    corridor = "Extended Intermediate Corridor 17mm (Desktop & Screen Depth)"
                    triggers.append("Desktop/counter-dominant working distance (60-75cm)")
                elif gender == "female":
                    corridor = "Short Corridor 14mm (Anthropometric Female Arm Reach 33cm)"
                    triggers.append("Female anthropometric shorter arm reach (32-35cm)")
                else:
                    corridor = "Balanced Universal Progression Corridor (15mm)"
                patient_exp = (
                    "Effortless transition across all distances (near, intermediate, far) "
                    "with wide, clear reading zones for first-time progressive wearers."
                )
            dispensing_notes = (
                "Verify pupil center height and monocular fitting heights in chosen frame. "
                "Ensure minimum fitting height matches corridor."
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
        if is_two_wheeler and is_night_glare:
            coating = "ZEISS DuraVision DriveSafe + Platinum (Dust & High-Beam Glare Shield)"
        elif is_night_glare:
            coating = "ZEISS DuraVision DriveSafe"
        elif is_heavy_screen:
            coating = "ZEISS DuraVision BlueProtect (400–455nm Selective Filter)"
        elif is_outdoor_heavy:
            coating = "ZEISS PhotoFusion X (Fast Variable Tint) + DuraVision Platinum"
        else:
            coating = "ZEISS DuraVision Platinum UV (Ultra-Hard Scratch Resistance + Anti-Static)"

        # 4. Determine Recommended Index & Material
        if is_two_wheeler:
            rec_index = "1.60 High-Impact Polycarbonate / Trivex (Road Safety)"
            dispensing_notes += (
                " [TWO-WHEELER ROAD SAFETY: Mandatory shatter-resistant 1.60 high-impact material "
                "and dust-repellent oleophobic coating for bike/scooter riding.]"
            )
        elif gender == "female" and (is_presbyope or is_heavy_screen):
            rec_index = "1.60 High Index (Cosmetic Edge Thinning for Feminine Frames)"
        elif is_presbyope and is_heavy_screen:
            rec_index = "1.60 High Index (Thin & Lightweight)"
        elif is_outdoor_heavy:
            rec_index = "1.60 Impact-Resistant (Extra Durability)"
        else:
            rec_index = "1.56 / 1.60 Clarity Index"

        # Factor in Ocular Surface Dryness
        if dryness_status == "fluctuating_blur_burning":
            triggers.append("Ocular surface burning and fluctuating tear-film blur")
            dispensing_notes += (
                " [TEAR-FILM DRY EYE WARNING: Patient reports fluctuating blur and ocular burning. "
                "Evaluate Tear Break-Up Time (TBUT) before finalizing reading add to prevent premature over-plus dispensing.]"
            )
            if "Platinum" not in coating:
                coating = "ZEISS DuraVision Platinum UV (Ultra-Slick Oleophobic + Blue-Light Protection)"

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
                if gender == "male" and duochrome.get("status") == "needs_clinical_attention":
                    dispensing_notes += (
                        " [MALE COLOUR VIGILANCE: Red-green Duochrome imbalance noted. "
                        "Check for X-linked congenital deuteranomaly/protanomaly (~8% prevalence) during trial lens refraction.]"
                    )

        # 6. Progressive Adaptation & Non-Tolerance Risk Calculation
        adaptation_score = 0
        risk_factors = []
        if is_presbyope:
            current_modality = profile.eyewear_history.get("current_modality", "never_worn")
            if current_modality in ["never_worn", "distance_only", "readers_only"]:
                adaptation_score += 30
                risk_factors.append("First-time progressive wearer transitioning from single-vision/readers")
            if ergo_plane == "handheld_mobile_close":
                adaptation_score += 25
                risk_factors.append("Close handheld reading posture (< 35cm) demands steep downward version")
            if onscreen_test_results:
                astig_finding = onscreen_test_results.get("astigmatic_dial", {})
                if astig_finding.get("astigmatism_suspected"):
                    adaptation_score += 25
                    risk_factors.append("Uncorrected cylinder astigmatism creates peripheral corridor swim")
            if age >= 52:
                adaptation_score += 20
                risk_factors.append(f"High reading addition demand at age {age}")

            if adaptation_score >= 65:
                risk_level = "HIGH"
                dispensing_notes += (
                    f" [PROGRESSIVE ADAPTATION ALERT: High non-tolerance risk (Score {adaptation_score}/100). "
                    f"Recommend ZEISS SmartLife Individual soft corridor + in-store head-turn dynamic counseling.]"
                )
            elif adaptation_score >= 35:
                risk_level = "MODERATE"
                dispensing_notes += (
                    f" [PROGRESSIVE ADAPTATION NOTE: Moderate non-tolerance risk (Score {adaptation_score}/100). "
                    f"Advise 3-day gradual gaze adaptation protocol.]"
                )
            else:
                risk_level = "LOW"

            progressive_adaptation = {
                "score": adaptation_score,
                "risk_level": risk_level,
                "risk_factors": risk_factors,
                "recommended_corridor_type": "ZEISS SmartLife Individual (Soft Corridor)" if risk_level == "HIGH" else "ZEISS SmartLife Plus (Balanced)",
            }
        else:
            progressive_adaptation = {
                "score": 0,
                "risk_level": "NOT_APPLICABLE",
                "risk_factors": [],
                "recommended_corridor_type": "N/A (Single Vision / Digital)",
            }

        return ZeissLensRecommendation(
            primary_lens=primary_lens,
            lens_family=lens_family,
            recommended_coating=coating,
            recommended_index=rec_index,
            corridor_or_boost=corridor,
            patient_explanation=patient_exp,
            optician_dispensing_notes=dispensing_notes,
            lifestyle_triggers=triggers,
            progressive_adaptation_risk=progressive_adaptation,
        )
