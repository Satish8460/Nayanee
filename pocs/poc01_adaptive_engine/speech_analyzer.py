"""Clinical Spoken Language Understanding (SLU) & Semantic Matcher for Nayanee.
Maps spoken Indic and English transcripts to canonical clinical options using
keyword ontologies, token overlap, and semantic intent scoring.
"""

from typing import Dict, List, Optional, Tuple
from .models import Question
from .questions_bank import get_question_by_id


# Multilingual clinical keyword lexicons for option intent matching
CLINICAL_LEXICON: Dict[str, List[str]] = {
    # Chief Complaint
    "distance_blur": [
        "distance", "blur", "far", "distant", "board", "sign", "face", "bus",
        "ದೂರ", "ದೂರದ್ದು", "ಮಸುಕು", "ಕಾಣಿಸ್ತಿಲ್ಲ", "ಮಸುಕಾಗಿದೆ",
        "दूर", "धुंधला", "साफ नहीं", "पहचान", "दूरी",
        "தூரம்", "தூரத்து", "மங்கலாக", "தெரியவில்லை",
        "దూరం", "దూరంగా", "మసక", "కనిపించడం లేదు",
        "ദൂരം", "ദൂരെയുള്ളത്", "മങ്ങൽ", "കാണുന്നില്ല"
    ],
    "near_reading_blur": [
        "near", "reading", "read", "mobile", "phone", "paper", "book", "newspaper", "close", "text", "small print",
        "ಹತ್ತಿರ", "ಓದಲು", "ಮೊಬೈಲ್", "ಪೇಪರ್", "ಅಕ್ಷರ", "ಪುಸ್ತಕ", "ಕಷ್ಟ",
        "पास", "पढ़ने", "मोबाइल", "अखबार", "किताब", "छोटे अक्षर",
        "படிக்க", "பக்கத்து", "மொபைல்", "செய்தித்தாள்", "எழுத்துக்கள்",
        "దగ్గర", "చదవడ", "మొబైల్", "పేపర్", "అక్షరాలు",
        "വായിക്കാൻ", "അടുത്തുള്ളത്", "മൊബൈൽ", "പത്രം", "അക്ഷരങ്ങൾ"
    ],
    "headaches_eyestrain": [
        "headache", "strain", "pain", "fatigue", "tired", "heavy", "forehead",
        "ತಲೆನೋವು", "ಕಣ್ಣು ನೋವು", "ಆಯಾಸ", "ಉರಿ", "ಭಾರ",
        "सिरदर्द", "दर्द", "थकान", "खिंचाव", "भारीपन",
        "தலைவலி", "கண் வலி", "சோர்வு", "கனமானது",
        "తలనొప్పి", "కంటి నొప్పి", "అలసట", "లాగుడు",
        "തലവേദന", "കണ്ണ് വേദന", "ക്ഷീണം", "തളർച്ച"
    ],
    "general_checkup": [
        "checkup", "routine", "general", "normal", "regular", "annual",
        "ಸಾಮಾನ್ಯ", "ತಪಾಸಣೆ", "ರೂಟಿನ್", "ಪರೀಕ್ಷೆ",
        "चेकअप", "नियमित", "सामान्य", "जांच",
        "பரிசோதனை", "பொதுவான", "வழக்கமான",
        "సాధారణ", "పరీక్ష", "చెకప్",
        "പരിശോധന", "സാധാരണ"
    ],
    "sudden_vision_change": [
        "sudden", "drop", "change", "rapid", "lost", "blackout",
        "ಹಠಾತ್", "ದಿಢೀರ್", "ಒಮ್ಮೆಲೆ", "ಬದಲಾಗಿದೆ",
        "अचानक", "एकाएक", "बदलाव", "गायब",
        "திடீர்", "திடீரென", "மாற்றம்",
        "హఠాత్తుగా", "అకస్మాత్తుగా", "మారింది",
        "പെട്ടെന്ന്", "മാറ്റം"
    ],

    # Acute symptoms (Red Flag)
    "no_acute_symptoms": [
        "no", "none", "nothing", "never", "normal", "fine",
        "ಇಲ್ಲ", "ಯಾವುದೂ ಇಲ್ಲ", "ತೊಂದರೆ ಇಲ್ಲ", "ಏನೂ ಇಲ್ಲ",
        "नहीं", "कोई नहीं", "कुछ नहीं", "बिल्कुल नहीं",
        "இல்லை", "ஒன்றுமில்லை", "பிரச்சனை இல்லை",
        "లేదు", "ఏమీ లేదు", "సమస్య లేదు",
        "ഇല്ല", "ഒന്നുമില്ല", "കുഴപ്പമില്ല"
    ],
    "sudden_pain_redness": [
        "pain", "redness", "red", "ache", "severe pain",
        "ನೋವು", "ಕೆಂಪಾಗಿದೆ", "ತೀವ್ರ ನೋವು",
        "दर्द", "लाल", "लाली", "तेज दर्द",
        "வலி", "சிவத்தல்", "கடுமையான வலி",
        "నొప్పి", "ఎరుపు", "తీవ్రమైన నొప్పి",
        "വേദന", "ചുവപ്പ്", "കഠിനമായ വേദന"
    ],
    "flashes_or_floaters": [
        "flashes", "floaters", "spark", "lightning", "spots", "dots",
        "ಮಿಂಚು", "ಚುಕ್ಕೆ", "ಬೆಳಕು", "ತೇಲುವ",
        "चमक", "रोशनी", "धब्बे", "बिजली",
        "மின்னல்", "புள்ளிகள்", "கீற்றுகள்",
        "మెరుపులు", "చుక్కలు", "కాంతి",
        "മിന്നൽ", "വെളിച്ചം", "പാടുകൾ"
    ],
    "sudden_vision_drop": [
        "vision drop", "blind", "cannot see", "loss",
        "ದೃಷ್ಟಿ ನಷ್ಟ", "ಕಾಣಿಸ್ತಿಲ್ಲ", "ಕಳೆದುಕೊಂಡೆ",
        "नज़र कम", "दिखना बंद", "अंधा",
        "பார்வை இழப்பு", "தெரியவில்லை",
        "చూపు తగ్గింది", "కనిపించడం లేదు",
        "കാഴ്ച നഷ്ടം", "കാണുന്നില്ല"
    ],

    # Frequency & Severity standard options
    "never": [
        "never", "no", "not at all", "zero",
        "ಖಂಡಿತ ಇಲ್ಲ", "ಇಲ್ಲ", "ಎಂದಿಗೂ ಇಲ್ಲ",
        "कभी नहीं", "बिल्कुल नहीं", "नहीं",
        "ஒருபோதும் இல்லை", "இல்லை",
        "ఎప్పుడూ లేదు", "లేదు",
        "ഒരിക്കലുമില്ല", "ഇല്ല"
    ],
    "sometimes": [
        "sometimes", "occasionally", "now and then", "mild", "a little",
        "ಕೆಲವೊಮ್ಮೆ", "ಸ್ವಲ್ಪ", "ಆಗಾಗ", "ಯಾವಾಗಲೋ",
        "कभी-कभी", "हल्का", "थोड़ा",
        "சில நேரங்களில்", "எப்போதாவது", "சிறிது",
        "అప్పుడప్పుడు", "కొద్దిగా",
        "ചിലപ്പോഴൊക്കെ", "കുറച്ച്"
    ],
    "often": [
        "often", "frequently", "many times", "regularly",
        "ಹೆಚ್ಚಾಗಿ", "ತುಂಬಾ", "ಸಾಕಷ್ಟು", "ಪದೇ ಪದೇ",
        "अक्सर", "काफी", "बार-बार",
        "அடிக்கடி", "பல முறை",
        "చాలాసార్లు", "తరచుగా",
        "പലപ്പോഴും", "കൂടുതലും"
    ],
    "always": [
        "always", "severe", "every day", "constantly", "completely",
        "ಯಾವಾಗಲೂ", "ತುಂಬಾ ಕಷ್ಟ", "ಸಂಪೂರ್ಣವಾಗಿ",
        "हमेशा", "लगातार", "बहुत ज्यादा",
        "எப்போதுமே", "மிகவும்",
        "ఎల్లప్పుడూ", "ఎప్పుడూ", "చాలా తీవ్రంగా",
        "എപ്പോഴും", "വളരെ ബുദ്ധിമുട്ട്"
    ],

    # Eyewear History
    "never_worn": [
        "never worn", "no glasses", "no specs", "first time",
        "ಕನ್ನಡಕ ಹಾಕಿಲ್ಲ", "ಇಲ್ಲ", "ಮೊದಲ ಬಾರಿ",
        "चश्मा नहीं", "कभी नहीं लगाया", "पहली बार",
        "கண்ணாடி அணிந்ததில்லை", "இல்லை",
        "కళ్ళజోడు వాడలేదు", "లేదు",
        "കണ്ണട ഉപയോഗിച്ചിട്ടില്ല", "ഇല്ല"
    ],
    "distance_only": [
        "distance only", "driving glasses", "far only",
        "ದೂರಕ್ಕೆ ಮಾತ್ರ", "ದೂರದ ಕನ್ನಡಕ",
        "सिर्फ दूर का", "दूर का चश्मा",
        "தூரத்திற்கு மட்டும்",
        "దూరానికి మాత్రమే",
        "ദൂരത്തേക്ക് മാത്രം"
    ],
    "reading_only": [
        "reading only", "reading glasses", "near only",
        "ಓದಲು ಮಾತ್ರ", "ಓದುವ ಕನ್ನಡಕ",
        "सिर्फ पढ़ने का", "पढ़ने का चश्मा",
        "படிப்பதற்கு மட்டும்",
        "చదవడానికి మాత్రమే",
        "വായനയ്ക്ക് മാത്രം"
    ],
    "bifocal_or_progressive": [
        "bifocal", "progressive", "both distance and near", "two in one", "all in one",
        "ಎರಡಕ್ಕೂ", "ಬೈಫೋಕಲ್", "ಪ್ರೋಗ್ರೆಸ್ಸಿವ್", "ದೂರ ಹತ್ತಿರ ಎರಡೂ",
        "दोनों", "बाइफोकल", "प्रोग्रेसिव", "दूर और पास दोनों",
        "இரண்டும்", "பைஃபோகல்", "ப்ரோக்ரெசிவ்",
        "రెండూ", "బైఫోకల్", "ప్రోగ్రెసివ్",
        "രണ്ടും", "ബൈഫോക്കൽ", "പ്രോഗ്രസീവ്"
    ],

    # Systemic Health
    "none": [
        "none", "no bp", "no sugar", "no diabetes", "healthy", "neither",
        "ಯಾವುದೂ ಇಲ್ಲ", "ಇಲ್ಲ", "ಶುಗರ್ ಬಿಪಿ ಇಲ್ಲ",
        "कुछ नहीं", "कोई बीमारी नहीं", "शुगर नहीं", "बीपी नहीं",
        "எதுவுமில்லை", "இல்லை",
        "ఏమీ లేవు", "లేదు",
        "ഇതൊന്നുമില്ല", "ഇല്ല"
    ],
    "diabetes_only": [
        "sugar", "diabetes", "diabetic",
        "ಶುಗರ್", "ಮಧುಮೇಹ", "ಸಕ್ಕರೆ ಕಾಯಿಲೆ",
        "शुगर", "डायबिटीज", "मधुमेह",
        "சர்க்கரை நோய்", "நீரிழிவு",
        "షుగర్", "మధుమేహం",
        "ഷുഗർ", "പ്രമേഹം"
    ],
    "hypertension_only": [
        "bp", "blood pressure", "hypertension", "high bp",
        "ಬಿಪಿ", "ರಕ್ತದೊತ್ತಡ",
        "बीपी", "ब्लड प्रेशर", "रक्तचाप",
        "பிபி", "இரத்த அழுத்தம்",
        "బీపీ", "రక్తపోటు",
        "ബിപി", "പ്രഷർ"
    ],
    "both_diabetes_and_bp": [
        "both", "sugar and bp", "diabetes and hypertension",
        "ಎರಡೂ ಇವೆ", "ಶುಗರ್ ಮತ್ತು ಬಿಪಿ",
        "दोनों हैं", "शुगर और बीपी दोनों",
        "இரண்டும் உள்ளன", "சர்க்கரை மற்றும் பிபி",
        "రెండూ ఉన్నాయి", "షుగర్ మరియు బీపీ",
        "രണ്ടും ഉണ്ട്", "ഷുഗറും ബിപിയും"
    ],
}


def normalize_text(text: str) -> str:
    """Lowercases, strips punctuation, and cleans whitespace."""
    if not text:
        return ""
    cleaned = text.lower().strip()
    for punct in [".", ",", "?", "!", "-", "_", "(", ")", "/", "'", '"']:
        cleaned = cleaned.replace(punct, " ")
    return " ".join(cleaned.split())


def score_option_match(transcript: str, option_id: str, localized_label: str) -> float:
    """Calculates semantic match confidence between user transcript and an option."""
    norm_transcript = normalize_text(transcript)
    norm_label = normalize_text(localized_label)
    norm_opt_id = normalize_text(option_id.replace("_", " "))

    if not norm_transcript:
        return 0.0

    # 1. Exact match with label or option ID
    if norm_transcript == norm_label or norm_transcript == norm_opt_id:
        return 1.0

    # 2. Substring match
    if norm_label and (norm_label in norm_transcript or norm_transcript in norm_label):
        return 0.90

    # 3. Keyword lexicon matching
    keywords = CLINICAL_LEXICON.get(option_id, [])
    match_count = 0
    words = norm_transcript.split()
    for kw in keywords:
        kw_norm = normalize_text(kw)
        if kw_norm in norm_transcript:
            match_count += 2
        for w in words:
            if w == kw_norm:
                match_count += 3

    if match_count > 0:
        return min(0.95, 0.55 + (match_count * 0.12))

    # 4. Token overlap with label
    label_tokens = set(norm_label.split())
    transcript_tokens = set(words)
    overlap = label_tokens.intersection(transcript_tokens)
    if overlap:
        return min(0.85, 0.50 + (len(overlap) / max(len(label_tokens), 1)) * 0.4)

    return 0.0


def analyze_transcript_for_question(
    question_id: str,
    transcript: str,
    language_code: str = "en"
) -> Tuple[str, float, str]:
    """Analyzes user transcript against question options and returns best matched option."""
    q = get_question_by_id(question_id)
    opts_map = q.options_translations.get(language_code, {})

    best_opt = q.options[0]
    best_score = 0.0
    best_label = opts_map.get(best_opt, best_opt.replace("_", " ").title())

    for opt in q.options:
        label = opts_map.get(opt, opt.replace("_", " ").title())
        score = score_option_match(transcript, opt, label)
        if score > best_score:
            best_score = score
            best_opt = opt
            best_label = label

    # If no keywords matched above threshold, return moderate confidence on first option
    if best_score < 0.2:
        best_score = 0.35

    return best_opt, round(best_score, 2), best_label
