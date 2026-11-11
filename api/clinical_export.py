"""Clinical Export Service for Nayanee.
"""

from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import HTMLResponse
from pocs.poc01_adaptive_engine.explainability import ExplainabilityReport
from pocs.poc01_adaptive_engine.lifestyle_advisor import OpticalLifestyleAdvisor
from .session_store import store

router = APIRouter(prefix="/api/v1/export", tags=["Clinical Export"])


@router.get("/profile/{profile_id}/summary-text")
def export_profile_summary_text(profile_id: str):
    prof = store.get_profile(profile_id)
    if not prof:
        raise HTTPException(status_code=404, detail="Profile not found.")

    text_report = ExplainabilityReport.generate_clinical_handover_summary(prof)
    return Response(content=text_report, media_type="text/plain; charset=utf-8")


@router.get("/profile/{profile_id}/audit-trail")
def export_profile_audit_trail(profile_id: str):
    prof = store.get_profile(profile_id)
    if not prof:
        raise HTTPException(status_code=404, detail="Profile not found.")

    engine = store.get_engine(prof.session_id)
    if not engine:
        return {"audit_trail": [], "note": "Engine session expired or finalized."}

    trace = ExplainabilityReport.generate_turn_trace(engine.turn_history)
    return {
        "profile_id": profile_id,
        "session_id": prof.session_id,
        "turns_count": len(trace),
        "audit_trace": trace,
    }


@router.get("/profile/{profile_id}/printable-slip", response_class=HTMLResponse)
def export_printable_slip(profile_id: str):
    prof = store.get_profile(profile_id)
    if not prof:
        raise HTTPException(status_code=404, detail="Profile not found.")

    guidance = OpticalLifestyleAdvisor.generate_recommendations(prof)

    is_urgent = len(prof.red_flags) > 0
    status_color = "#de350b" if is_urgent else "#0052cc"
    status_label = "URGENT MEDICAL TRIAGE" if is_urgent else prof.review_status.value.replace("_", " ").upper()

    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Nayanee Intake Slip — {profile_id[:8]}</title>
  <style>
    @media print {{
      body {{ margin: 0; padding: 10mm; font-size: 11pt; }}
      .no-print {{ display: none; }}
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
      max-width: 650px;
      margin: 20px auto;
      padding: 24px;
      border: 1px solid #ccc;
      color: #172b4d;
      line-height: 1.4;
    }}
    .header {{
      display: flex;
      justify-content: space-between;
      border-bottom: 2px solid #002b66;
      padding-bottom: 10px;
      margin-bottom: 16px;
    }}
    .brand {{ font-size: 1.4rem; font-weight: bold; color: #002b66; }}
    .badge {{
      display: inline-block;
      padding: 4px 10px;
      border-radius: 4px;
      font-size: 0.85rem;
      font-weight: bold;
      color: white;
      background: {status_color};
    }}
    .section {{ margin-bottom: 14px; }}
    .section-title {{ font-size: 0.95rem; font-weight: bold; border-bottom: 1px solid #dfe1e6; padding-bottom: 3px; margin-bottom: 6px; text-transform: uppercase; color: #5e6c84; }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.9rem; }}
    .box {{ background: #f4f5f7; padding: 8px 12px; border-radius: 4px; }}
    .alert-box {{ background: #ffebe6; border-left: 4px solid #de350b; padding: 8px 12px; margin-bottom: 10px; font-size: 0.9rem; color: #bf2600; font-weight: bold; }}
    .opto-action {{ border: 1.5px dashed #0052cc; padding: 12px; border-radius: 6px; margin-top: 18px; }}
    .btn-print {{ background: #0052cc; color: white; padding: 8px 18px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }}
  </style>
</head>
<body>
  <div class="no-print" style="margin-bottom: 16px; text-align: right;">
    <button class="btn-print" onclick="window.print()">🖨️ Print Consultation Slip</button>
  </div>

  <div class="header">
    <div>
      <div class="brand">NAYANEE (ನಯनी)</div>
      <div style="font-size: 0.8rem; color: #5e6c84;">Adaptive Vision Intelligence &bull; Optical Consultation Slip</div>
    </div>
    <div style="text-align: right;">
      <span class="badge">{status_label}</span><br>
      <small style="color: #5e6c84;">ID: {profile_id[:16]}</small>
    </div>
  </div>

  {'<div class="alert-box">🚨 MANDATORY EMERGENCY TRIAGE: Critical symptom reported. Refer for medical ophthalmology evaluation prior to refraction.</div>' if is_urgent else ''}

  <div class="section">
    <div class="section-title">Patient Intake Details</div>
    <div class="grid">
      <div class="box"><strong>Patient Name:</strong> {getattr(prof, 'patient_name', 'Anonymous Patient')}</div>
      <div class="box"><strong>Age / Gender:</strong> {getattr(prof, 'patient_age', 'N/A') or 'N/A'} yrs / {getattr(prof, 'patient_gender', 'N/A') or 'N/A'}</div>
      <div class="box"><strong>Interaction Language:</strong> {prof.customer_language.value.upper()}</div>
      <div class="box"><strong>Consultation Date:</strong> {prof.created_at[:10]}</div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Functional Vision Profile</div>
    <div class="grid">
      <div class="box">
        <strong>Near Demands:</strong><br>
        • Mobile Reading: {prof.near_vision_status.get('mobile_reading_status', 'unassessed')}<br>
        • Presbyopic Sign: {'YES' if prof.near_vision_status.get('has_presbyopic_indicators') else 'NO'}
      </div>
      <div class="box">
        <strong>Distance & Driving:</strong><br>
        • Clarity Rating: {prof.distance_vision_status.get('clarity_rating', 'unassessed')}<br>
        • Night Glare: {prof.distance_vision_status.get('night_glare_difficulty', 'unassessed')}
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Ergonomic Lifestyle Context</div>
    <div class="grid">
      <div class="box">
        <strong>Screen Hours:</strong> {prof.lifestyle_occupational_context.get('daily_screen_hours', 'unassessed')}<br>
        <strong>Digital Strain Risk:</strong> {'ELEVATED' if prof.lifestyle_occupational_context.get('digital_visual_fatigue_risk') else 'NORMAL'}
      </div>
      <div class="box">
        <strong>Outdoor Sun Exposure:</strong> {prof.lifestyle_occupational_context.get('outdoor_sun_exposure', 'unassessed')}<br>
        <strong>Current Eyewear:</strong> {prof.eyewear_history.get('current_modality', 'never_worn')}
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Pre-Refraction Optical Guidance (Lens Considerations)</div>
    <div style="font-size: 0.85rem; background: #ebf2fa; padding: 10px; border-radius: 4px;">
      {''.join(f"<div><strong>• [{g['category']}]</strong> {g['consideration']}</div>" for g in guidance) if guidance else '<div>Standard subjective refraction indicated.</div>'}
    </div>
  </div>

  <div class="opto-action">
    <div style="font-weight: bold; margin-bottom: 6px; color: #002b66;">Optometrist Refraction & Clinical Notes</div>
    <div style="height: 60px; border-bottom: 1px dotted #ccc;"></div>
    <div style="display: flex; justify-content: space-between; margin-top: 10px; font-size: 0.8rem; color: #5e6c84;">
      <span>Optometrist Signature: _______________________</span>
      <span>Date: _______________</span>
    </div>
  </div>

  <div style="text-align: center; margin-top: 20px; font-size: 0.75rem; color: #8993a4;">
    Notice: Functional vision profile generated via adaptive anamnesis. Non-diagnostic. Subject to professional subjective refraction.
  </div>
</body>
</html>
"""
    return HTMLResponse(content=html_content)
