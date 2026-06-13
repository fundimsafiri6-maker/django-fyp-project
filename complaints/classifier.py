import os
os.environ.setdefault('PYTHON_FROZEN_MODULES', 'off')
import joblib
import re
import numpy as np
import pandas as pd


def get_classifier():
    """Get classifier instance (loads from ml_models dir next to this file)"""
    model_dir = os.path.join(os.path.dirname(__file__), 'ml_models')
    model = joblib.load(os.path.join(model_dir, 'best_complaint_classifier.pkl'))
    vectorizer = joblib.load(os.path.join(model_dir, 'tfidf_vectorizer.pkl'))
    return model, vectorizer


def clean_text(text):
    """Clean and preprocess text"""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _contains_rule(text_lower, keyword):
    """Match phrases by substring and single words by word boundary."""
    keyword = keyword.lower()
    if " " in keyword or "-" in keyword or "/" in keyword:
        return keyword in text_lower
    return re.search(rf"\b{re.escape(keyword)}\b", text_lower) is not None


def _first_match(text_lower, keywords):
    for keyword in keywords:
        if _contains_rule(text_lower, keyword):
            return keyword
    return None


# --- ICT Outage Pre-detection ---
ICT_OUTAGE_PATTERNS = [
    'system is down', 'system down', 'server down', 'server crashed', 'server is down',
    'portal down', 'portal is down', 'website down', 'website is down',
    'system crashed', 'portal crashed', 'system is offline', 'server is offline',
    'system unavailable', 'server unavailable',
    'email system is not working', 'email not working', 'email system down',
    'wifi not connecting', 'wifi not working', 'network down', 'network not working',
    'login failed', 'login not working', 'password not working',
    'credentials not recognized', 'cannot login', 'cant login',
    'cannot reset password', 'cant reset password',
    'online registration system keeps crashing',
    'student management system not allowing',
]

ICT_KEYWORDS = [
    'portal', 'website', 'login', 'password', 'email', 'wifi', 'wi-fi', 'internet',
    'network', 'server', 'database', 'system', 'software', 'hardware',
    'lms', 'moodle', 'canvas', 'blackboard', 'e-learning', 'elearning', 'zoom',
    'teams', 'student account', 'registration portal', 'online registration',
    # Expanded ICT terms
    'app', 'application', 'browser', 'webpage', 'page', 'site',
    'error', 'bug', 'crash', 'crashed', 'timeout', 'loading', 'slow',
    'account', 'access', 'username', 'authentication', 'verification',
    'download', 'upload', 'install', 'update', 'upgrade', 'configuration',
    'connectivity', 'bandwidth', 'offline', 'online', 'connection',
    'computer', 'laptop', 'desktop', 'tablet', 'device', 'monitor',
    'printer', 'keyboard', 'mouse', 'screen', 'equipment',
    'tech', 'technical', 'technology', 'digital',
]


# --- Other (Out-of-Department) Pre-detection ---
ACADEMIC_ICT_ANCHORS = [
    'assignment', 'course', 'module', 'class', 'lecture', 'lecturer', 'professor',
    'teacher', 'instructor', 'exam', 'test', 'quiz', 'grade', 'marks', 'gpa',
    'result', 'timetable', 'deadline', 'syllabus', 'curriculum', 'research', 'thesis',
    'project', 'supervisor', 'advisor', 'online class', 'course material', 'coursework',
    'studying', 'study', 'studies',
    # Registration & enrollment
    'register', 'registration', 'enroll', 'enrollment', 'semester', 'session',
    'intake', 'admission', 'enrol', 'enrolment',
    # Academic submissions
    'submit', 'submission', 'assignment submission', 'homework', 'paper',
    'essay', 'report', 'presentation', 'practical', 'lab report', 'lab work',
    # Classroom & learning
    'classroom', 'lecture hall', 'lesson', 'learning', 'teaching', 'tutorial',
    'group work', 'discussion', 'workshop', 'seminar', 'orientation',
    # Academic staff & dept
    'academic', 'faculty', 'department', 'program', 'programme', 'curriculum',
    'syllabus', 'college', 'school', 'institute', 'university',
    # Fees & finance
    'scholarship', 'fee', 'tuition', 'financial aid', 'student loan',
    'sponsorship', 'bursary', 'stipend',
    # ICT systems
    'portal', 'login', 'password', 'email', 'wifi', 'wi-fi', 'internet', 'network',
    'computer', 'software', 'hardware', 'database', 'server', 'system',
    'lms', 'moodle', 'canvas', 'blackboard', 'e-learning', 'elearning', 'zoom',
    'teams', 'student account', 'registration portal', 'online registration',
    # ICT issues
    'app', 'application', 'browser', 'website', 'webpage', 'page',
    'error', 'bug', 'crash', 'crashed', 'timeout', 'loading', 'slow',
    'not working', 'not loading', 'not opening', 'not accessible',
    'account', 'access', 'permission', 'user', 'username',
    'login credentials', 'password reset', 'forgot password',
    'authentication', 'verification', 'two-factor',
    # Common ICT terms
    'download', 'upload', 'install', 'update', 'upgrade',
    'configuration', 'setting', 'setup', 'connection',
    'offline', 'online', 'connectivity', 'bandwidth',
    'screen', 'monitor', 'keyboard', 'mouse', 'printer',
    'tablet', 'laptop', 'desktop', 'device', 'equipment',
]

PERSONAL_WELFARE_PHRASES = [
    'i want to go home', 'want to go home', 'go home', 'going home', 'homesick',
    'miss home', 'missing home', 'leave campus', 'leave school', 'drop out',
    'withdraw from school', 'i am lonely', 'i feel lonely', 'i am bored', 'i feel bored',
    'i am sad', 'i feel sad', 'i am depressed', 'i feel depressed', 'i am stressed',
    'i feel stressed', 'mental health', 'panic attack', 'anxiety', 'counselling',
    'counseling', 'need counselling', 'need counseling', 'personal problem', 'family problem',
    'family emergency', 'sick at home', 'i am sick', 'i feel sick', 'not feeling well',
    'i am hungry', 'very hungry', 'i am thirsty', 'very thirsty', 'sleepy', 'tired',
    'i love you', 'i love', 'love you', 'i need a wife', 'need a wife', 'i need a husband',
    'need a husband', 'want to marry', 'i want to marry', 'looking for girlfriend',
    'looking for boyfriend', 'need a relationship', 'i need a relationship',
    'i want a relationship', 'marriage proposal', 'love life',
    'i dont have money', 'i don\'t have money', 'no money', 'i am broke', 'im broke',
    'i like tembele', 'tembele', 'i want to run', 'want to run', 'i want to go',
    'i want to play', 'i want to eat', 'i want to sleep', 'i want to drink',
    'prove that you are not robot', 'prove you are not robot', 'not a robot',
]

OTHER_CATEGORIES = {
    "facilities": [
        "bathroom", "toilet", "restroom", "washroom", "sink", "sewer", "sewage",
        "water", "no water", "dirty water", "leak", "leaking", "pipe", "tap", "flood",
        "flooded", "drainage", "electricity", "power cut", "blackout", "bulb", "lighting",
        "fan", "air conditioner", "ac", "heating", "cooling", "ventilation",
        "building", "facility", "maintenance", "repair", "broken", "damaged", "crack",
        "door", "window", "desk", "chair", "table", "furniture", "seat",
        "roof", "ceiling", "floor", "stairs", "elevator", "lift",
        "cleanliness", "sanitation", "hygiene", "dustbin", "trash", "garbage",
        "bad smell", "dirty", "unclean", "paint", "wall",
        "flickering", "flicker", "lights", "lighting",
        "printer", "out of paper", "paper jam", "ink",
        "laboratory equipment", "lab equipment", "outdated equipment",
        "sports field", "gym equipment",
        "water fountain", "drinking water",
        "library fines", "lost property",
    ],
    "dining": [
        "food", "meal", "breakfast", "lunch", "dinner", "cafeteria", "canteen",
        "dining", "restaurant", "kitchen", "menu", "catering", "cook", "cooking",
        "stale food", "spoiled food", "food poisoning", "taste",
    ],
    "accommodation": [
        "hostel", "dorm", "dormitory", "residence", "accommodation", "roommate", "room mate",
        "bed", "mattress", "bunk", "hostel room", "residence hall",
        "housing", "landlord", "rent", "eviction", "room allocation",
    ],
    "security": [
        "security", "guard", "unsafe", "not safe", "safety", "theft", "stolen", "steal",
        "robbery", "robbed", "lost property", "missing item",
        "violence", "fight", "fighting", "assault", "attack", "attacked",
        "threat", "threatened", "weapon", "drug", "alcohol",
        "fire", "emergency", "accident", "injury", "danger", "dangerous",
    ],
    "transport": [
        "transport", "bus", "shuttle", "vehicle", "parking", "car park", "taxi", "boda",
        "commute", "commuting", "traffic", "pickup", "drop off", "driver", "transportation",
    ],
    "health": [
        "clinic", "hospital", "medical", "medicine", "pharmacy", "nurse", "doctor appointment",
        "health center", "health centre", "ambulance", "first aid",
        "treatment", "vaccination", "sick leave", "illness", "fever",
    ],
    "accessibility": [
        "disability", "disabled", "wheelchair", "ramp", "accessible", "accessibility",
        "special needs", "sign language", "hearing impaired", "visually impaired", "braille",
    ],
    "admin": [
        "admission", "application form", "admission letter", "transcript", "certificate",
        "diploma", "graduation clearance", "clearance", "student id", "id card", "identity card",
        "record office", "registrar office", "document", "documents",
        "approval", "permission", "policy", "procedure", "regulation",
    ],
    "finance": [
        "refund", "billing", "invoice", "receipt", "reimbursement", "overcharged", "double charged",
        "salary", "wage", "allowance", "stipend not paid", "cashier",
        "bank slip", "control number", "sponsor payment",
    ],
    "general": [
        "misc", "miscellaneous", "general", "nonsense", "random",
        "hello", "hi", "test message", "no complaint", "nothing", "not sure",
    ],
}


def _detect_ict_outage(text_lower):
    """Quick pre-check for obvious ICT system outage"""
    for pattern in ICT_OUTAGE_PATTERNS:
        if pattern in text_lower:
            return True
    return False


def _detect_other_rule_based(text_lower):
    """
    Rule-based detection for out-of-department complaints.
    Returns (is_other, reason) if clearly outside Academic/ICT scope.
    """
    has_anchor = _first_match(text_lower, ACADEMIC_ICT_ANCHORS) is not None
    has_ict = _first_match(text_lower, ICT_KEYWORDS) is not None

    for phrase in PERSONAL_WELFARE_PHRASES:
        if phrase in text_lower:
            if has_anchor or has_ict:
                continue
            return True, f'Personal/welfare: {phrase}'

    for dept, keywords in OTHER_CATEGORIES.items():
        match = _first_match(text_lower, keywords)
        if not match:
            continue
        # For any department, skip if there's academic/ict anchor context
        if has_anchor and dept not in ('general',):
            continue
        # For facilities/finance, check if it's actually an ICT issue
        if dept in ('facilities', 'finance'):
            ict_ctx = _first_match(text_lower, ICT_KEYWORDS)
            phys_ctx = _first_match(text_lower, [
                "bathroom", "toilet", "water", "leak", "flood", "electricity", "bulb",
                "building", "door", "window", "desk", "chair", "dirty",
                "refund", "invoice", "receipt", "overcharged", "cashier",
                "bank slip", "control number",
            ])
            if ict_ctx and not phys_ctx:
                continue
        # For dining/accommodation, check if it's ICT-related (e.g. hostel wifi)
        if dept in ('dining', 'accommodation') and has_ict and not has_anchor:
            ict_specific = _first_match(text_lower, [
                "wifi", "wi-fi", "internet", "network", "portal", "login",
                "system", "computer", "server", "app", "application",
                "online", "website", "email", "account",
            ])
            if ict_specific:
                continue
        return True, f'{dept}: {match}'

    question = _first_match(text_lower, ['where is', 'when is', 'how to', 'can i', 'who can', 'need information about'])
    service = _first_match(text_lower, ['admission', 'transcript', 'certificate', 'id card', 'registrar', 'clearance', 'hostel', 'transport', 'clinic', 'security'])
    if question and service:
        has_acad_ict = _first_match(text_lower, ACADEMIC_ICT_ANCHORS + ICT_KEYWORDS)
        if not has_acad_ict:
            return True, f'admin inquiry: {question} {service}'

    return False, None


# --- HOD Detection ---
STAFF_KEYWORDS = [
    "lecturer", "lecture", "professor", "prof", "doctor", "dr", "teacher",
    "instructor", "tutor", "supervisor", "advisor", "adviser", "mentor",
    "course coordinator", "module coordinator", "program coordinator", "programme coordinator",
    "dean", "hod", "head of department", "department head", "chairperson", "chair",
    "faculty", "staff", "employee", "administrator", "admin officer", "academic officer",
    "lab technician", "technician", "ict officer", "it officer", "system administrator",
    "support staff", "registrar", "exam officer", "invigilator", "marker", "examiner",
]

TITLE_KEYWORDS = [
    "dr", "doctor", "prof", "professor", "mr", "mrs", "ms", "miss", "madam", "sir",
    "lecturer", "teacher", "instructor", "tutor", "supervisor", "dean", "hod",
]

SERIOUS_KEYWORDS = [
    "harassment", "sexual harassment", "assault", "abuse", "threat", "threaten",
    "threatened", "intimidation", "bullying", "discrimination", "racism", "tribalism",
    "sexism", "favoritism", "favouritism", "bribe", "bribery", "corruption",
    "retaliation", "victimization", "victimisation", "blackmail", "coercion",
    "inappropriate", "misconduct", "unethical", "humiliated", "insulted", "abused",
    "biased", "bias", "mistreat", "mistreatment",
]

COMPLAINT_KEYWORDS = [
    "unprofessional", "rude", "arrogant", "disrespectful", "insult", "insulted",
    "shout", "shouted", "yell", "yelled", "mock", "mocked", "ignored", "neglect",
    "negligence", "biased", "bias", "unfair", "unjust", "mistreat", "mistreatment",
    "complaint", "grievance", "issue", "problem", "concern", "report", "against",
    "attitude", "behavior", "behaviour",
    "does not explain", "doesn't explain", "dont explain", "don't explain", "do not explain",
    "does not teach", "doesn't teach", "dont teach", "don't teach", "do not teach",
    "dont understand", "don't understand", "do not understand", "cannot understand",
    "can't understand", "confusing", "unclear explanation",
    "marks unfairly", "marked unfairly", "grade unfairly", "grading unfair",
    "changed my marks", "lost my marks", "refused to help", "not helpful",
    "refuses to answer", "delays feedback", "withheld results",
]

POSITIVE_KEYWORDS = [
    "helpful", "excellent", "good", "great", "professional", "supportive", "friendly",
    "kind", "appreciate", "thank", "thanks", "love", "amazing", "best", "clear",
    "explains well", "teaches well", "respectful",
]

STAFF_NAME_STOPWORDS = {
    "is", "was", "are", "were", "the", "our", "my", "a", "an", "to", "for", "of",
    "not", "but", "and", "or", "in", "on", "at", "from", "with", "without",
    "very", "really", "always", "never", "good", "bad", "rude", "late", "fair", "unfair",
    "helpful", "excellent", "professional", "supportive", "kind", "friendly",
    "has", "have", "had", "been", "being", "am", "are", "were", "was",
    "does", "do", "doesn't", "dont", "don't", "did",
    # Common pronouns & short words that are not names
    "he", "she", "it", "we", "they", "i", "you", "me", "him", "her", "us", "them",
    "his", "its", "your", "their", "this", "that", "these", "those",
    "who", "whom", "what", "which", "where", "when", "why", "how",
    "can", "could", "will", "would", "shall", "should", "may", "might", "must",
    "any", "all", "each", "every", "some", "many", "much", "more", "most",
    "here", "there", "now", "then", "today", "yesterday", "tomorrow",
    "up", "down", "over", "under", "out", "off", "into", "onto", "upon",
    "one", "two", "three", "first", "second", "last", "next", "other",
    "since", "until", "during", "before", "after", "above", "below", "between",
    "also", "just", "only", "even", "still", "already", "yet", "again",
    "about", "around", "within", "without", "through", "throughout",
    "such", "like", "than", "then", "as", "if", "so", "no", "yes", "ok",
    "please", "sorry", "thanks", "thank",
    # Common complaint title words that follow staff keywords (not names)
    "issue", "problem", "complaint", "report", "concern", "matter", "case",
    "incident", "request", "inquiry", "query", "feedback", "comment",
    "help", "support", "assistance", "guidance", "advice", "info",
    "question", "clarification", "information", "update", "status",
    "review", "appeal", "grievance", "dispute", "claim",
    "service", "quality", "standard", "policy", "procedure",
    "change", "improvement", "suggestion", "recommendation",
    "delay", "error", "mistake", "fault", "failure",
    "action", "response", "reply", "resolution", "solution",
    "meeting", "appointment", "session", "class", "lecture",
    "mark", "grade", "result", "score", "gpa",
    "registration", "enrollment", "admission", "application",
    "account", "profile", "access", "password", "login",
    "schedule", "timetable", "deadline", "submission",
    "requirement", "document", "form", "letter", "certificate",
    "fee", "payment", "finance", "scholarship", "fund",
    "room", "hostel", "accommodation", "facility",
    "transport", "bus", "shuttle", "parking",
    "food", "meal", "dining", "cafeteria", "menu",
    "network", "wifi", "internet", "portal", "system",
    # Common verbs that follow staff titles (not names)
    "says", "said", "told", "mentioned", "stated", "explained",
    "informed", "replied", "answered", "asked", "claimed", "remarked",
    "noted", "indicated", "expressed", "responded", "reported",
    "wrote", "emailed", "texted", "called", "messaged",
    "came", "went", "left", "arrived", "entered",
    "gave", "took", "made", "did", "put", "set",
    "knows", "thinks", "believes", "feels", "seems",
    "needs", "wants", "likes", "dislikes", "prefers",
    "works", "teaches", "lectures", "helps", "supports",
    "uses", "runs", "manages", "handles", "deals",
    "comes", "goes", "looks", "shows", "appears",
}


def _has_staff_name(original_text, text_lower):
    """
    Detect if text contains a staff member's name.
    Returns (found, name, score_boost, reasons)
    """
    role_pattern = rf"\b(?:{'|'.join(re.escape(k) for k in STAFF_KEYWORDS + TITLE_KEYWORDS)})\.?\s+(?:called\s+|named\s+)?([A-Z][a-z]{{3,}})\b"
    role_match = re.search(role_pattern, original_text, re.IGNORECASE)
    if role_match:
        possible = role_match.group(1).lower()
        if possible not in STAFF_NAME_STOPWORDS and possible not in STAFF_KEYWORDS and len(possible) >= 3:
            return True, role_match.group(1), 3, [f'Staff name: {role_match.group(1)}']

    name_before_role = rf"\b([A-Z][a-z]{{3,}})\s+(?:is|was|becomes|became)\s+(?:our|my|the|a|an)?\s*(?:{'|'.join(re.escape(k) for k in STAFF_KEYWORDS)})\b"
    name_match = re.search(name_before_role, original_text)
    if name_match:
        possible = name_match.group(1).lower()
        if possible not in STAFF_NAME_STOPWORDS and len(possible) >= 3:
            return True, name_match.group(1), 3, [f'Staff name: {name_match.group(1)}']

    title_name_pattern = rf"\b(?:{'|'.join(re.escape(k) for k in TITLE_KEYWORDS)})\.?\s+([A-Z][a-z]{{3,}})\b"
    title_match = re.search(title_name_pattern, original_text)
    if title_match:
        clean_name = title_match.group(1).lower()
        if clean_name not in STAFF_NAME_STOPWORDS and len(clean_name) >= 3:
            return True, title_match.group(1), 4, ['Staff title with name']

    accusation_verbs = [
        "changed", "lost", "gave", "failed", "refused", "denied",
        "threatened", "harassed", "insulted", "abused", "asked",
        "demanded", "delayed", "withheld",
    ]
    accusation_terms = SERIOUS_KEYWORDS + COMPLAINT_KEYWORDS
    named_pattern = r"\b([A-Z][a-z]{3,})\b\s+(?:" + "|".join(re.escape(v) for v in accusation_verbs) + r")\b.{0,80}"
    named_match = re.search(named_pattern, original_text)
    if named_match:
        possible_name = named_match.group(1)
        context = named_match.group(0).lower()
        pn_lower = possible_name.lower()
        if pn_lower not in STAFF_NAME_STOPWORDS and len(pn_lower) >= 4 and _first_match(context, accusation_terms):
            return True, possible_name, 5, [f'Named person with accusation: {possible_name}']

    return False, None, 0, []


def detect_hod_category(text):
    """
    Detect privacy-sensitive ICT/Academic complaints involving staff members.
    """
    text_lower = text.lower()
    original_text = str(text)
    score = 0
    reasons = []
    staff_found = False
    name_found = False
    complaint_found = False
    serious_found = False
    positive_found = False

    staff_match = _first_match(text_lower, STAFF_KEYWORDS)
    if staff_match:
        staff_found = True
        score += 2
        reasons.append(f"Staff role: {staff_match}")

    serious_match = _first_match(text_lower, SERIOUS_KEYWORDS)
    if serious_match:
        serious_found = True
        complaint_found = True
        score += 5
        reasons.append(f"Serious issue: {serious_match}")

    complaint_match = _first_match(text_lower, COMPLAINT_KEYWORDS)
    if complaint_match:
        complaint_found = True
        score += 2
        reasons.append(f"Complaint context: {complaint_match}")

    positive_match = _first_match(text_lower, POSITIVE_KEYWORDS)
    if positive_match:
        positive_found = True
        score -= 4
        reasons.append(f"Positive sentiment: {positive_match}")

    name_found, name, name_boost, name_reasons = _has_staff_name(original_text, text_lower)
    if name_found:
        score += name_boost
        reasons.extend(name_reasons)

    phrase_match = _first_match(text_lower, [
        "complaint against", "issue with", "problem with", "report against",
        "grievance against", "accuse", "accused",
        "treated me", "treats me", "shouted at me", "insulted me",
        "harassed me", "threatened me", "forced me",
        "changed my marks", "failed me unfairly",
    ])
    if phrase_match:
        complaint_found = True
        score += 3
        reasons.append(f"Complaint phrase: {phrase_match}")

    if positive_found and not complaint_found and not serious_found:
        return False, "Positive staff feedback, not a privacy complaint"

    if staff_found and serious_found:
        return True, "; ".join(reasons)
    if staff_found and name_found and (complaint_found or score >= 5):
        return True, "; ".join(reasons)
    if staff_found and complaint_found and score >= 7:
        return True, "; ".join(reasons)
    if name_found and serious_found and score >= 6:
        return True, "; ".join(reasons)
    if name_found and complaint_found and score >= 5:
        return True, "; ".join(reasons)

    return False, "Not a privacy-sensitive complaint"


def classify_complaint(complaint_text, model=None, vectorizer=None):
    """
    Classify complaint text using the trained model with rule-based enhancements.

    WORKFLOW:
    1. Rule-based: ICT outage/system keywords -> ICT
    2. Rule-based: Clear Other patterns (personal, welfare, facilities) -> Other
    3. ML model predicts (Academic/ICT/Other)
    4. If ML predicts Academic/ICT, check for HOD (privacy/accusations)
    5. If ML confidence < 0.4 and prediction is not clearly Academic/ICT, use rule-based fallback

    Optionally pass model/vectorizer to use in-memory instances instead of loading from disk.
    """
    if model is None or vectorizer is None:
        model, vectorizer = get_classifier()
    text_lower = str(complaint_text).lower()
    cleaned = clean_text(complaint_text)

    # Step 1: Rule-based ICT outage detection (catches "system is down" etc.)
    if _detect_ict_outage(text_lower):
        return {
            'category': 'ICT',
            'confidence': 0.95,
            'reason': 'Rule-based ICT detection: system outage',
            'requires_admin_review': False,
            'routing_priority': 'high',
            'department': 'ICT Department',
            'assigned_staff': 'ICT Staff',
            'action': 'Route to ICT Department'
        }

    # Step 2: Rule-based Other detection (clearly non-Academic/ICT)
    is_other, other_reason = _detect_other_rule_based(text_lower)
    if is_other:
        return {
            'category': 'Other',
            'confidence': 1.0,
            'reason': other_reason,
            'requires_admin_review': True,
            'routing_priority': 'medium',
            'department': 'Admin Queue',
            'assigned_staff': 'ADMIN',
            'action': 'Route to ADMIN for review and handling'
        }

    # Step 3: ML model prediction
    vec = vectorizer.transform([cleaned])
    ml_prediction = model.predict(vec)[0]
    ml_pred_norm = str(ml_prediction).strip().lower()

    try:
        proba = model.predict_proba(vec)[0]
        ml_confidence = max(proba)
    except Exception:
        ml_confidence = 0.85

    # Step 4: Check HOD if ML predicts Academic or ICT
    if ml_pred_norm in ('academic', 'ict'):
        is_hod, hod_reason = detect_hod_category(complaint_text)
        if is_hod:
            return {
                'category': 'HOD',
                'confidence': 1.0,
                'reason': f"HOD: {hod_reason} (ML predicted {ml_prediction})",
                'requires_admin_review': False,
                'routing_priority': 'high',
                'department': 'Head of Department',
                'assigned_staff': 'HOD',
                'action': 'Route to HOD for sensitive complaint handling',
                'ml_prediction': ml_prediction,
                'ml_confidence': ml_confidence
            }

    # Step 5: If no vocabulary features matched, ML has no signal
    if vec.nnz == 0:
        return {
            'category': 'Other',
            'confidence': 1.0,
            'reason': 'Unrecognized text: no known keywords match the complaint',
            'requires_admin_review': True,
            'routing_priority': 'medium',
            'department': 'Admin Queue',
            'assigned_staff': 'ADMIN',
            'action': 'Route to ADMIN for review and handling'
        }

    # Step 6: If ML confidence is low, check for overrides
    if ml_confidence < 0.65:
        try:
            # If text has strong Academic keywords and model is uncertain, prefer Academic
            if _first_match(text_lower, ['studying', 'study', 'assignment', 'coursework', 'lecture', 'timetable', 'syllabus', 'exam', 'grade', 'course', 'classroom', 'semester', 'tutorial']):
                return {
                    'category': 'Academic',
                    'confidence': 0.6,
                    'reason': f"Academic keyword override (ML predicted {ml_prediction} with {ml_confidence*100:.1f}%)",
                    'requires_admin_review': False,
                    'routing_priority': 'normal',
                    'department': 'Academic Department',
                    'assigned_staff': 'Academic Staff',
                    'action': 'Route to Academic Department',
                    'ml_prediction': ml_prediction,
                    'ml_confidence': ml_confidence
                }
            # If text has strong ICT keywords and model is uncertain, prefer ICT
            if _first_match(text_lower, ['portal', 'login', 'password', 'email', 'internet', 'network', 'wifi', 'server', 'database', 'system down', 'not working', 'error', 'crash', 'browser']):
                return {
                    'category': 'ICT',
                    'confidence': 0.6,
                    'reason': f"ICT keyword override (ML predicted {ml_prediction} with {ml_confidence*100:.1f}%)",
                    'requires_admin_review': False,
                    'routing_priority': 'normal',
                    'department': 'ICT Department',
                    'assigned_staff': 'ICT Staff',
                    'action': 'Route to ICT Department',
                    'ml_prediction': ml_prediction,
                    'ml_confidence': ml_confidence
                }
            # If "Other" is in top-3 and confidence is very low, route to admin
            top3 = np.argsort(proba)[-3:]
            top3_classes = [model.classes_[i].lower() for i in top3]
            if ml_confidence < 0.5 and 'other' in top3_classes:
                # Check if text has any academic/ict keywords before routing to Other
                has_any = _first_match(text_lower, ACADEMIC_ICT_ANCHORS + ICT_KEYWORDS)
                if not has_any:
                    return {
                        'category': 'Other',
                        'confidence': 1.0,
                        'reason': f"Low ML confidence ({ml_confidence*100:.1f}%) - routed to admin (ML predicted {ml_prediction})",
                        'requires_admin_review': True,
                        'routing_priority': 'medium',
                        'department': 'Admin Queue',
                        'assigned_staff': 'ADMIN',
                        'action': 'Route to ADMIN for review',
                        'ml_prediction': ml_prediction,
                        'ml_confidence': ml_confidence
                    }
        except Exception:
            pass

    # Return ML classification
    category_name = ml_prediction.capitalize() if ml_pred_norm != 'ict' else 'ICT'
    return {
        'category': category_name,
        'confidence': ml_confidence,
        'reason': f"ML classification ({ml_prediction}) with {ml_confidence*100:.1f}% confidence",
        'requires_admin_review': False,
        'routing_priority': 'normal',
        'department': f'{category_name} Department',
        'assigned_staff': f'{category_name} Staff',
        'action': f'Route to {category_name} Department'
    }
