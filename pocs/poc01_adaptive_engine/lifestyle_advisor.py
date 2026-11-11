"""Ergonomic Lifestyle & Optical Guidance Engine for Nayanee.
"""

from typing import List, Dict
from .models import FunctionalVisionProfile


class OpticalLifestyleAdvisor:
    @staticmethod
    def generate_recommendations(profile: FunctionalVisionProfile) -> List[Dict[str, str]]:
        recommendations = []

        screen_hours = profile.lifestyle_occupational_context.get("daily_screen_hours")
        if screen_hours in ["five_to_eight", "more_than_eight"]:
            recommendations.append({
                "category": "Digital Ergonomics",
                "finding": f"High daily screen exposure ({screen_hours.replace('_', ' ')} hours).",
                "consideration": "Consider selective blue-attenuating lens coating and intermediate anti-fatigue / digital occupational lens design.",
            })

        glare = profile.distance_vision_status.get("night_glare_difficulty")
        if glare in ["moderate_glare", "severe_glare_avoids_driving"]:
            recommendations.append({
                "category": "Driving Safety",
                "finding": f"Reported {glare.replace('_', ' ')}.",
                "consideration": "Recommend premium multi-layer anti-reflective (AR) coating with high transmittance; evaluate contrast sensitivity and astigmatic correction.",
            })

        near_reading = profile.near_vision_status.get("mobile_reading_status")
        if near_reading in ["significant_blur_holds_far", "cannot_read_near"]:
            recommendations.append({
                "category": "Near Vision Support",
                "finding": "Classic presbyopic symptoms (holds reading material far or cannot read near).",
                "consideration": "Assess reading addition (+Add) via trial frame; discuss progressive addition lenses (PAL) vs. dedicated reading glasses based on intermediate needs.",
            })

        outdoor = profile.lifestyle_occupational_context.get("outdoor_sun_exposure")
        if outdoor in ["majority_outdoors_heavy_sun", "one_to_three_hours_outdoors"]:
            recommendations.append({
                "category": "Environmental Protection",
                "finding": "Substantial outdoor sunlight/dust exposure.",
                "consideration": "Recommend 100% UV400 protective lenses; consider photochromic (variable tint) or polarized sunglasses for glare attenuation.",
            })

        eyewear_age = profile.eyewear_history.get("glasses_age")
        if eyewear_age == "more_than_two_years":
            recommendations.append({
                "category": "Eyewear Wear & Tear",
                "finding": "Current glasses in use for >2 years.",
                "consideration": "Check existing lenses for micro-scratches, optical center alignment, and frame vertex distance shifts.",
            })

        return recommendations
