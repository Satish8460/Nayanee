"""Deterministic On-Screen Visual Functional Tests for Nayanee.
Provides calibrated, browser-friendly evaluators for 3 standard optical tests:
1. Red-Green Duochrome Test (Spherical accommodation balance)
2. Astigmatic Clock Dial (Directional blur / cylinder meridian detection)
3. Amsler Grid (Macular distortion & emergency retinal defect sentinel)
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ScreeningResult:
    test_name: str
    status: str  # "normal", "abnormal", "needs_clinical_attention", "urgent_referral"
    finding: str
    clinical_notes_for_optometrist: str
    is_emergency_flag: bool = False


class OnScreenScreeningEngine:
    """Evaluates customer responses to calibrated on-screen optical tests."""

    @staticmethod
    def evaluate_duochrome(user_selection: str) -> ScreeningResult:
        """User selections: 'red_clearer', 'green_clearer', 'equally_sharp'."""
        sel = user_selection.lower().strip()
        if sel == "red_clearer":
            return ScreeningResult(
                test_name="Red-Green Duochrome Balance",
                status="needs_clinical_attention",
                finding="Optotypes on the RED half appear darker/sharper.",
                clinical_notes_for_optometrist=(
                    "Suggests relative myopic shift or insufficient minus power / uncorrected myopic refraction. "
                    "Start trial refraction by adding -0.25D step until balance is achieved."
                ),
            )
        elif sel == "green_clearer":
            return ScreeningResult(
                test_name="Red-Green Duochrome Balance",
                status="needs_clinical_attention",
                finding="Optotypes on the GREEN half appear darker/sharper.",
                clinical_notes_for_optometrist=(
                    "Suggests relative hyperopic state or accommodative spasm / over-minused refraction. "
                    "In younger patients, check for accommodative fatigue; in older adults, add plus power."
                ),
            )
        else:
            return ScreeningResult(
                test_name="Red-Green Duochrome Balance",
                status="normal",
                finding="Optotypes on RED and GREEN halves appear equally sharp.",
                clinical_notes_for_optometrist="Chromatically balanced at the retina. No spherical accommodation bias.",
            )

    @staticmethod
    def evaluate_astigmatic_dial(selected_meridian: str) -> ScreeningResult:
        """Selected meridian: 'all_lines_equal', '12_to_6' (vertical), '9_to_3' (horizontal),
        '10_to_4' (oblique), '2_to_8' (oblique).
        """
        sel = selected_meridian.lower().strip()
        if sel in ["all_lines_equal", "none", "equal"]:
            return ScreeningResult(
                test_name="Astigmatic Clock Dial",
                status="normal",
                finding="All radiating clock dial lines appear equally dark and distinct.",
                clinical_notes_for_optometrist="No dominant astigmatic meridian observed. Symmetrical ocular power distribution.",
            )
        else:
            meridian_map = {
                "12_to_6": ("Vertical 90°", "Axis suspected near 180° (Rule of 30: 6 o'clock x 30 = 180°)"),
                "9_to_3": ("Horizontal 180°", "Axis suspected near 90° (Rule of 30: 3 o'clock x 30 = 90°)"),
                "10_to_4": ("Oblique ~120°", "Axis suspected near 30° (Oblique astigmatism)"),
                "2_to_8": ("Oblique ~60°", "Axis suspected near 150° (Oblique astigmatism)"),
            }
            name, axis_hint = meridian_map.get(
                sel, (sel.replace("_", " "), "Potential astigmatic meridian")
            )
            return ScreeningResult(
                test_name="Astigmatic Clock Dial",
                status="abnormal",
                finding=f"Lines along the {name} meridian appear noticeably darker/bolder.",
                clinical_notes_for_optometrist=(
                    f"Astigmatism suspected. {axis_hint}. "
                    "Prioritize Jackson Cross-Cylinder refinement in trial frame."
                ),
            )

    @staticmethod
    def evaluate_amsler_grid(finding: str) -> ScreeningResult:
        """Finding: 'all_lines_straight', 'wavy_distorted_lines', 'dark_patch_missing_spots'."""
        f = finding.lower().strip()
        if f in ["wavy_distorted_lines", "metamorphopsia"]:
            return ScreeningResult(
                test_name="Amsler Grid Macular Screening",
                status="urgent_referral",
                finding="Metamorphopsia reported: Wavy or distorted grid lines near center fixation.",
                clinical_notes_for_optometrist=(
                    "CRITICAL MACULAR ALERT: Wavy lines indicate potential central retinal / macular disturbance "
                    "(e.g., macular edema, choroidal neovascularization, or epiretinal membrane). "
                    "Refer immediately to tertiary ophthalmologist for dilated fundus examination and OCT."
                ),
                is_emergency_flag=True,
            )
        elif f in ["dark_patch_missing_spots", "scotoma"]:
            return ScreeningResult(
                test_name="Amsler Grid Macular Screening",
                status="urgent_referral",
                finding="Central / paracentral scotoma reported: Missing grid areas or dark patches.",
                clinical_notes_for_optometrist=(
                    "CRITICAL RETINAL ALERT: Absolute or relative scotoma observed on Amsler grid. "
                    "Immediate referral to ophthalmologist / vitreoretinal specialist required."
                ),
                is_emergency_flag=True,
            )
        else:
            return ScreeningResult(
                test_name="Amsler Grid Macular Screening",
                status="normal",
                finding="All grid squares intact; all horizontal and vertical lines straight and continuous.",
                clinical_notes_for_optometrist="Central 10 degrees of visual field intact without visible metamorphopsia.",
            )
