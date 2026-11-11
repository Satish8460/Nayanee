"""Language Registry and Lexicon for Nayanee.
"""

from typing import Dict, List
from pydantic import BaseModel


class LanguageMetadata(BaseModel):
    code: str
    autonym: str
    english_name: str
    script: str
    sample_confirmation_prompt: str
    common_optical_keywords: List[str]
    code_mixed_loanwords: List[str]


LANGUAGE_REGISTRY: Dict[str, LanguageMetadata] = {
    "kn": LanguageMetadata(
        code="kn",
        autonym="ಕನ್ನಡ",
        english_name="Kannada",
        script="Kannada",
        sample_confirmation_prompt="ನೀವು ಹೇಳಿದ್ದು: '{transcript}'. ಇದು ಸರಿಯೇ?",
        common_optical_keywords=["ದೃಷ್ಟಿ", "ಕಣ್ಣು", "ಮಸುಕು", "ಕನ್ನಡಕ", "ಓದುವುದು", "ದೂರ", "ತಲೆನೋವು"],
        code_mixed_loanwords=["glasses", "screen", "mobile", "reading", "night driving", "glare", "laptop"],
    ),
    "hi": LanguageMetadata(
        code="hi",
        autonym="हिन्दी",
        english_name="Hindi",
        script="Devanagari",
        sample_confirmation_prompt="आपने कहा: '{transcript}'। क्या यह सही है?",
        common_optical_keywords=["दृष्टि", "आँखें", "धुंधला", "चश्मा", "पढ़ना", "दूर", "सिरदर्द"],
        code_mixed_loanwords=["glasses", "chashma", "screen", "mobile", "reading", "night driving", "glare"],
    ),
    "ta": LanguageMetadata(
        code="ta",
        autonym="தமிழ்",
        english_name="Tamil",
        script="Tamil",
        sample_confirmation_prompt="நீங்கள் கூறியது: '{transcript}'. இது சரியானதா?",
        common_optical_keywords=["பார்வை", "கண்", "மங்கலான", "கண்ணாடி", "வாசிப்பு", "தூரம்", "தலைவலி"],
        code_mixed_loanwords=["glasses", "kannadi", "screen", "mobile", "reading", "night driving", "glare"],
    ),
    "te": LanguageMetadata(
        code="te",
        autonym="తెలుగు",
        english_name="Telugu",
        script="Telugu",
        sample_confirmation_prompt="మీరు చెప్పినది: '{transcript}'. ఇది సరైనదేనా?",
        common_optical_keywords=["దృష్టి", "కళ్ళు", "మసక", "కళ్ళజోడు", "చదవడం", "దూరం", "తలనొప్పి"],
        code_mixed_loanwords=["glasses", "screen", "mobile", "reading", "night driving", "glare"],
    ),
    "ml": LanguageMetadata(
        code="ml",
        autonym="മലയാളം",
        english_name="Malayalam",
        script="Malayalam",
        sample_confirmation_prompt="നിങ്ങൾ പറഞ്ഞത്: '{transcript}'. ഇത് ശരിയാണോ?",
        common_optical_keywords=["കാഴ്ച", "കണ്ണ്", "മങ്ങൽ", "കണ്ണട", "വായന", "ദൂരം", "തലവേദന"],
        code_mixed_loanwords=["glasses", "screen", "mobile", "reading", "night driving", "glare"],
    ),
    "en": LanguageMetadata(
        code="en",
        autonym="English",
        english_name="English",
        script="Latin",
        sample_confirmation_prompt="You said: '{transcript}'. Is this correct?",
        common_optical_keywords=["vision", "eyes", "blur", "glasses", "reading", "distance", "headache"],
        code_mixed_loanwords=[],
    ),
}


def get_language_metadata(code: str) -> LanguageMetadata:
    if code not in LANGUAGE_REGISTRY:
        raise ValueError(f"Language '{code}' is not supported in the 6-language registry.")
    return LANGUAGE_REGISTRY[code]
