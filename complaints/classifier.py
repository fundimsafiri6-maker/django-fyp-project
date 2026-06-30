import re


def clean_text(text):
    if not text:
        return ""
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _contains_rule(text_lower, keyword):
    keyword = keyword.lower()
    if " " in keyword or "-" in keyword or "/" in keyword:
        return keyword in text_lower
    return re.search(rf"\b{re.escape(keyword)}\b", text_lower) is not None


def _first_match(text_lower, keywords):
    for keyword in keywords:
        if _contains_rule(text_lower, keyword):
            return keyword
    return None


ICT_KEYWORDS = {
    'portal', 'portals', 'website', 'websites', 'login', 'log in', 'log-in',
    'password', 'passwords', 'email', 'emails', 'wifi', 'wi-fi', 'internet',
    'network', 'networks', 'server', 'servers', 'database', 'databases',
    'system', 'systems', 'software', 'hardware',
    'lms', 'moodle', 'canvas', 'blackboard', 'e-learning', 'elearning', 'zoom',
    'teams', 'student account', 'registration portal', 'online registration',
    'app', 'apps', 'application', 'applications', 'browser', 'browsers',
    'webpage', 'webpages', 'site', 'sites',
    'error', 'errors', 'bug', 'bugs', 'crash', 'crashed', 'crashes',
    'timeout', 'loading', 'slow',
    'account', 'accounts', 'access', 'username', 'usernames',
    'authentication', 'verification',
    'download', 'downloads', 'downloading', 'upload', 'uploads', 'uploading',
    'install', 'installing', 'installation', 'update', 'updates', 'updating',
    'upgrade', 'upgrading', 'configuration', 'config',
    'connectivity', 'bandwidth', 'offline', 'connection', 'connections',
    'computer', 'computers', 'laptop', 'laptops', 'desktop', 'desktops',
    'tablet', 'tablets', 'device', 'devices', 'monitor', 'monitors',
    'keyboard', 'keyboards', 'mouse',
    'screen', 'screens', 'equipment',
    'tech', 'technical', 'technology', 'technologies', 'digital',
        'not working', 'not loading', 'not opening', 'not responding',
    'login credentials', 'password reset', 'forgot password', 'reset password',
    'two-factor', 'two factor', '2fa',
    'sms', 'notification', 'notifications',
    'backup', 'restore', 'recovery', 'reboot', 'restart',
    'responsive', 'unresponsive', 'freeze', 'frozen', 'froze',
    'scanner', 'scanners', 'projector', 'projectors',
    'router', 'modem', 'switch', 'hub', 'firewall',
    'encryption', 'decryption', 'ssl', 'tls',
    'bandwidth', 'latency', 'ping', 'speed', 'slow internet',
    'malware', 'virus', 'antivirus', 'firewall',
    'cloud', 'storage', 'drive', 'onedrive', 'google drive',
    'virtual', 'vm', 'virtual machine',
    'data', 'dataset', 'analytics', 'dashboard',
    'automation', 'script',
}

ACADEMIC_KEYWORDS = {
    'assignment', 'assignments', 'course', 'courses', 'module', 'modules',
    'class', 'classes', 'lecture', 'lectures', 'lecturer', 'lecturers', 'professor',
    'teacher', 'instructor', 'exam', 'exams', 'examination', 'test', 'tests', 'quiz',
    'grade', 'grades', 'mark', 'marks', 'grading', 'gpa',
    'result', 'results', 'timetable', 'deadline', 'deadlines', 'syllabus',
    'curriculum', 'research', 'thesis', 'dissertation',
    'project', 'projects', 'supervisor', 'supervisors', 'advisor', 'advisors',
    'online class', 'course material', 'coursework',
    'studying', 'study', 'studies', 'student', 'students',
    'register', 'registration', 'enroll', 'enrollment', 'semester', 'semesters',
    'session', 'sessions', 'intake', 'admission', 'enrol', 'enrolment',
    'submit', 'submission', 'homework', 'paper', 'papers',
    'essay', 'essays', 'report', 'reports', 'presentation', 'presentations',
    'practical', 'practicals', 'lab report', 'lab work',
    'classroom', 'classrooms', 'lecture hall', 'lesson', 'lessons',
    'learning', 'teaching', 'tutorial', 'tutorials',
    'group work', 'discussion', 'discussions', 'workshop', 'workshops',
    'seminar', 'seminars', 'orientation',
    'academic', 'academics', 'faculty', 'department', 'departments',
    'program', 'programs', 'programme', 'programmes',
    'college', 'school', 'institute', 'university',
    'fee', 'fees', 'tuition',
    'financial aid', 'student loan', 'sponsorship', 'bursary', 'stipend',
    'invigilator', 'invigilation', 'malpractice', 'cheating', 'plagiarism',
    'curricula', 'transcript', 'transcripts', 'certificate', 'certificates',
    'diploma', 'diplomas', 'graduation', 'graduate',
    'accreditation', 'accredited', 'credit', 'credits',
    'unit', 'units', 'prerequisite', 'prerequisites',
    'elective', 'electives', 'core course', 'major', 'minor',
    'academic year', 'academic calendar', 'academic record',
    'supplementary', 'retake', 'resit', 'remedial',
    # CS/IT education subjects (often mistaken as ICT-only)
    'programming', 'coding', 'code', 'codes', 'algorithms',
    'data structures', 'data science', 'data analysis',
    'virtual learning', 'virtual classroom', 'online learning', 'e-learning',
    'tutoring', 'tutor', 'tutors', 'tutorial session',
    'textbook', 'textbooks', 'course material', 'study material',
    'computer science', 'information technology', 'information system',
    'it course', 'cs course', 'bachelor', 'degree', 'diploma program',
    'curriculum', 'accreditation', 'accredited program',
    'lab session', 'practical session', 'laboratory session',
    'field work', 'attachment', 'internship', 'industrial training',
    'teaching practice', 'school practice',
    'continuous assessment', 'cat', 'cat exam', 'cat test',
    'mid semester', 'end of semester', 'final exam',
    'course outline', 'course content', 'learning material',
    'reading list', 'reference book', 'recommended text',
    'academic advisor', 'academic counselling', 'academic counseling',
    'class representative', 'course rep', 'student leader',
    'extenuating circumstances', 'deferment', 'deferral', 'interruption',
}

PERSONAL_WELFARE_PHRASES = [
    'i want to go home', 'want to go home', 'go home', 'going home', 'homesick',
    'miss home', 'missing home', 'leave campus', 'leave school', 'drop out',
    'withdraw from school', 'i am lonely', 'i feel lonely', 'i am bored', 'i feel bored',
    'i am sad', 'i feel sad', 'i am depressed', 'i feel depressed', 'i am stressed',
    'i feel stressed',
    'mental health', 'panic attack', 'anxiety',
    'need counselling', 'need counseling', 'personal problem', 'family problem',
    'family emergency', 'sick at home', 'i am sick', 'i feel sick', 'not feeling well',
    'i am hungry', 'very hungry', 'i am thirsty', 'very thirsty', 'sleepy', 'tired',
    'i do not have money', "i don't have money", "i dont have money", 'no money', 'i am broke', 'im broke',
    'i want to eat', 'i want to sleep', 'i want to drink', 'i want to play', 'i want to run',
    'i love you', 'i love', 'love you',
    'i need a wife', 'need a wife', 'i need a husband', 'need a husband',
    'want to marry', 'i want to marry', 'looking for girlfriend', 'looking for boyfriend',
    'need a relationship', 'i need a relationship', 'i want a relationship',
    'marriage proposal', 'love life',
    'i like tembele', 'tembele', 'i like',
    'prove that you are not robot', 'prove you are not robot', 'not a robot',
    # Gratitude / non-complaints
    'thank you', 'thanks for', 'i appreciate', 'i am grateful', 'im grateful',
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
        "flickering", "flicker", "lights",
        "out of paper", "paper jam",
        "laboratory equipment", "lab equipment",
        "printer", "out of paper", "paper jam", "ink",
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
        "scholarship", "scholarships",
    ],
    "general": [
        "misc", "miscellaneous", "general", "nonsense", "random",
        "hello", "hi", "test message", "no complaint", "nothing", "not sure",
    ],
}

# --- Combined HOD keyword lists from training dataset + improvements ---
# Staff role keywords (singular, plural, multi-word titles)
HOD_STAFF_KEYWORDS = [
    "lecturer", "lecturers", "professor", "professors", "prof", "doctor", "doctors", "dr", "teacher",
    "teachers", "instructor", "instructors", "tutor", "tutors", "supervisor", "supervisors",
    "advisor", "advisors", "adviser", "advisers", "mentor", "mentors",
    "course coordinator", "module coordinator", "program coordinator", "programme coordinator",
    "dean", "deans", "hod", "head of department", "department head", "chairperson", "chair",
    "faculty", "staff", "employee", "administrator", "admin officer", "academic officer",
    "lab technician", "technician", "technicians", "ict officer", "it officer", "system administrator",
    "support staff", "staff member", "staff members", "registrar", "registrars",
    "exam officer", "invigilator", "marker", "examiner", "examiners",
    "mr", "mrs", "ms", "miss", "sir", "madam",
]

# Title keywords for name detection (e.g., "Dr. Smith", "Professor John")
HOD_TITLE_KEYWORDS = [
    "dr", "doctor", "prof", "professor", "mr", "mrs", "ms", "miss", "madam", "sir",
    "lecturer", "teacher", "instructor", "tutor", "supervisor", "dean", "hod",
]

# Serious keywords (accusations of misconduct, abuse, harassment, corruption, etc.)
HOD_SERIOUS_KEYWORDS = [
    "harassment", "harass", "harasses", "harassed", "harassing",
    "sexual harassment", "sexual misconduct",
    "assault", "assaulted", "assaulting",
    "abuse", "abuses", "abused", "abusing",
    "threat", "threaten", "threatens", "threatened", "threatening",
    "seduce", "seduced", "seducing", "ceduce", "ceduced", "ceducing",
    "intimidation", "intimidate", "intimidated",
    "bullying", "bully", "bullied",
    "discrimination", "discriminate", "discriminated", "racism", "tribalism",
    "sexism", "favoritism", "favouritism",
    "bribe", "bribery", "corrupt", "corruption",
    "retaliation", "retaliate", "retaliated",
    "victimization", "victimisation", "victimize", "victimized",
    "blackmail", "blackmailed", "coercion", "coerce", "coerced",
    "inappropriate", "misconduct", "unethical",
    "humiliated", "insulted", "abused",
    "biased", "bias", "unfair", "unfairly", "unjust", "unjustly", "mistreat", "mistreatment",
    "thief", "steal", "stole", "stolen", "theft", "fraud", "cheat", "cheated",
]

# Complaint keywords (negative behavior, poor conduct, service issues)
HOD_COMPLAINT_KEYWORDS = [
    "unprofessional", "rude", "arrogant", "disrespectful",
    "insult", "insults", "insulted", "insulting",
    "shout", "shouts", "shouted", "shouting",
    "yell", "yells", "yelled", "yelling",
    "mock", "mocks", "mocked", "mocking",
    "ignore", "ignores", "ignored", "ignoring",
    "neglect", "neglects", "neglected", "neglecting",
    "negligence", "negligent",
    "biased", "bias", "unfair", "unfairly", "unjust", "unjustly",
    "mistreat", "mistreats", "mistreated", "mistreatment",
    "complaint", "grievance", "issue", "problem", "concern", "report", "against",
    "attitude", "behavior", "behaviour",
    "strict", "harsh", "unfriendly", "inconsiderate",
    "incompetent", "careless", "unqualified", "lazy", "mean",
    "does not explain", "doesn't explain", "dont explain", "don't explain", "do not explain",
    "does not teach", "doesn't teach", "dont teach", "don't teach", "do not teach",
    "dont understand", "don't understand", "do not understand",
    "cannot understand", "can't understand", "confusing", "unclear explanation",
    "marks unfairly", "marked unfairly", "grade unfairly", "grading unfair",
    "changed my marks", "lost my marks", "refused to help", "not helpful",
    "refuses to answer", "delay", "delays", "delayed", "delaying", "delays feedback", "withheld results",
    "failed me", "unfair grading", "unfair marks",
]

HOD_POSITIVE_KEYWORDS = [
    "helpful", "excellent", "good", "great", "professional", "supportive", "friendly",
    "kind", "appreciate", "thank", "thanks", "love", "amazing", "best", "clear",
    "explains well", "teaches well", "respectful",
]

HOD_STAFF_NAME_STOPWORDS = {
    "is", "was", "are", "were", "the", "our", "my", "a", "an", "to", "for", "of",
    "not", "but", "and", "or", "in", "on", "at", "from", "with", "without",
    "very", "really", "always", "never", "good", "bad", "rude", "late", "fair", "unfair",
    "helpful", "excellent", "professional", "supportive", "kind", "friendly",
    "has", "have", "had", "been", "being", "am", "are", "were", "was",
    "does", "do", "doesn't", "dont", "don't", "did",
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
    "limited", "available", "multiple", "various", "numerous", "several",
    "notes", "halls", "recordings", "live", "doesn", "doesnt",
    "care", "lot", "part", "way", "side", "top", "back", "front", "left", "right",
    "thing", "things", "number", "group", "kind", "sort", "type", "types",
    "time", "times", "day", "days", "week", "weeks", "month", "months", "year", "years",
    "place", "area", "space", "room", "spot", "point", "line", "row", "column",
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
    Detect staff name patterns using 4 complementary regex strategies
    from the training dataset model. Returns (found, display_name, score_boost, reasons).
    """
    all_staff_terms = HOD_STAFF_KEYWORDS + HOD_TITLE_KEYWORDS
    escaped_terms = [re.escape(k) for k in all_staff_terms]
    terms_union = "|".join(escaped_terms)

    # Strategy 1: "Professor Smith", "Dr. John", "lecturer named Peter", "mr called juma"
    # Role part and name are case-insensitive (names often lowercase in informal text)
    # False positives filtered by extensive stopword list
    role_pattern = rf"\b(?:{terms_union})\.?\s+(?:called\s+|named\s+)?([A-Z][a-zA-Z]{{2,}})\b"
    role_match = re.search(role_pattern, original_text, re.IGNORECASE)
    if role_match:
        possible = role_match.group(1).lower()
        if possible not in HOD_STAFF_NAME_STOPWORDS and possible not in HOD_STAFF_KEYWORDS:
            return True, role_match.group(1), 3, [f"Staff name: {role_match.group(1)}"]

    # Strategy 2: "John is my lecturer", "Mary became our supervisor"
    name_before_role = rf"\b([A-Z][a-zA-Z]{{2,}})\s+(?:is|was|becomes|became)\s+(?:our|my|the|a|an)?\s*(?:{terms_union})\b"
    name_match = re.search(name_before_role, original_text)
    if name_match:
        return True, name_match.group(1), 3, [f"Staff name: {name_match.group(1)}"]

    # Strategy 3: Title + Name (simple title name pattern)
    title_terms = [re.escape(k) for k in HOD_TITLE_KEYWORDS]
    title_pattern = rf"\b(?:{'|'.join(title_terms)})\.?\s+([A-Z][a-zA-Z]{{2,}})\b"
    title_match = re.search(title_pattern, original_text)
    if title_match:
        clean_name = title_match.group(1).lower()
        if clean_name not in HOD_STAFF_NAME_STOPWORDS and len(clean_name) >= 3:
            return True, title_match.group(1), 4, [f"Title name: {title_match.group(1)}"]

    # Strategy 4: Name + accusation verb (e.g., "juma is corrupt", "baraka failed me")
    accusation_verbs = [
        "is", "was", "has", "have", "keeps", "always", "never", "changed", "lost",
        "gave", "failed", "refused", "denied", "threatened", "harassed", "insulted",
        "abused", "asked", "demanded", "delayed", "withheld",
    ]
    all_accusation = HOD_SERIOUS_KEYWORDS + HOD_COMPLAINT_KEYWORDS
    verb_union = "|".join(re.escape(v) for v in accusation_verbs)
    named_pattern = rf"\b([A-Z]{{2,}}|[A-Z][a-zA-Z]{{2,}})\b\s+(?:{verb_union})\b.{{0,80}}"
    named_match = re.search(named_pattern, original_text)
    if named_match:
        possible_name = named_match.group(1)
        context = named_match.group(0).lower()
        if possible_name.lower() not in HOD_STAFF_NAME_STOPWORDS and _first_match(context, all_accusation):
            return True, possible_name, 5, [f"Accused: {possible_name}"]

    return False, None, 0, []


def _detect_hod(text):
    """
    Detect privacy-sensitive complaints about staff members -> route to HOD.
    Uses keyword matching + 4-strategy name detection + cumulative thresholds.
    """
    text_lower = text.lower()
    original_text = str(text)
    score = 0
    reasons = []
    staff_found = False
    name_found = False
    serious_found = False
    complaint_found = False
    positive_found = False

    staff_match = _first_match(text_lower, HOD_STAFF_KEYWORDS)
    if staff_match:
        staff_found = True
        score += 2
        reasons.append(f"Staff role: {staff_match}")

    serious_match = _first_match(text_lower, HOD_SERIOUS_KEYWORDS)
    if serious_match:
        serious_found = True
        complaint_found = True
        score += 5
        reasons.append(f"Serious: {serious_match}")

    complaint_match = _first_match(text_lower, HOD_COMPLAINT_KEYWORDS)
    if complaint_match:
        complaint_found = True
        score += 2
        reasons.append(f"Complaint: {complaint_match}")

    positive_match = _first_match(text_lower, HOD_POSITIVE_KEYWORDS)
    if positive_match:
        positive_found = True
        score -= 4
        reasons.append(f"Positive: {positive_match}")

    # 4-strategy staff name detection (from training dataset model)
    name_found, name_display, name_boost, name_reasons = _has_staff_name(original_text, text_lower)
    if name_found:
        score += name_boost
        reasons.extend(name_reasons)

    # Complaint phrases against staff
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
        reasons.append(f"Phrase: {phrase_match}")

    # Positive feedback only -> not HOD
    if positive_found and not complaint_found and not serious_found:
        return False, "Positive feedback"

    # Thresholds (ordered strongest signal to weakest)
    # Staff role + serious accusation
    if staff_found and serious_found:
        return True, "; ".join(reasons) if reasons else "Staff + serious"
    # Staff role + named person + (complaint word or sufficient score)
    if staff_found and name_found and (complaint_found or score >= 5):
        return True, "; ".join(reasons)
    # Staff role + complaint keyword
    if staff_found and complaint_found:
        return True, "; ".join(reasons)
    # Named person + serious accusation
    if name_found and serious_found and score >= 6:
        return True, "; ".join(reasons)
    # Named person + complaint keyword
    if name_found and complaint_found and score >= 5:
        return True, "; ".join(reasons)
    # High cumulative score
    if staff_found and score >= 6:
        return True, "; ".join(reasons)
    if serious_found and (staff_found or name_found) and score >= 5:
        return True, "; ".join(reasons)
    if serious_found and score >= 8:
        return True, "; ".join(reasons)
    if complaint_found and (staff_found or name_found) and score >= 5:
        return True, "; ".join(reasons)
    if complaint_found and score >= 8:
        return True, "; ".join(reasons)

    return False, "Not HOD"


# ICT keywords that are clearly about infrastructure (not generic issue words)
ICT_SPECIFIC_KEYWORDS = {
    'portal', 'portals', 'wifi', 'wi-fi', 'internet', 'network', 'networks',
    'server', 'servers', 'database', 'databases', 'lms', 'moodle',
    'email', 'emails', 'password', 'passwords', 'login', 'log in',
    'computer', 'computers', 'laptop', 'laptops',
    'software', 'hardware', 'browser', 'browsers', 'website', 'websites',
    'app', 'apps', 'application', 'applications', 'zoom', 'teams',
    'connectivity', 'bandwidth', 'username', 'usernames', 'account', 'accounts',
    'vm', 'virtual machine', 'cloud', 'storage', 'drive',
    'router', 'modem', 'switch', 'hub', 'firewall',
    'projector', 'projectors', 'scanner', 'scanners',
    'encryption', 'decryption', 'ssl', 'tls',
    'malware', 'virus', 'antivirus',
    'backup', 'restore', 'recovery', 'reboot', 'restart',
    'sms', 'notification', 'notifications',
    'tech', 'technical', 'technology', 'technologies', 'digital',
    'student account', 'registration portal', 'online registration',
    'e-learning', 'elearning',
    'canvas', 'blackboard',
    'login credentials', 'password reset', 'forgot password', 'reset password',
    'two-factor', 'two factor', '2fa',
}


def _score_category(text_lower):
    """Score text for ICT, Academic, and Other categories. Returns (category, confidence, reason)."""
    # Step 1: ICT outage keywords -> immediate ICT
    outage_patterns = [
        'system is down', 'system down', 'server down', 'server crashed', 'server is down',
        'portal down', 'portal is down', 'website down', 'website is down',
        'system crashed', 'portal crashed', 'system is offline', 'server is offline',
        'system unavailable', 'server unavailable',
        'email not working', 'email system down',
        'wifi not connecting', 'wifi not working', 'network down', 'network not working',
        'login failed', 'login not working', 'password not working',
        'cannot login', 'cant login',
        'cannot reset password', 'cant reset password',
        'system not allowing', 'system is not allowing',
        'system not working for', 'online registration system keeps crashing',
        'credentials not recognized',
        'student management system not allowing',
        'email system is not working',
    ]
    for p in outage_patterns:
        if p in text_lower:
            return 'ICT', 0.95, f"ICT outage: {p}"

    # Step 2: Personal/welfare -> Other
    for phrase in PERSONAL_WELFARE_PHRASES:
        if phrase in text_lower:
            return 'Other', 0.95, f"Personal/welfare: {phrase}"

    # Step 3: Strong academic content phrases → immediate Academic (before keyword scoring)
    strong_academic_context = [
        'course material', 'learning material', 'study material', 'course content',
        'lecture notes', 'lecture slides', 'lecture recording',
        'teaching material', 'educational material',
    ]
    for phrase in strong_academic_context:
        if phrase in text_lower:
            return 'Academic', 0.9, f"Strong academic context: {phrase}"

    # Step 4: Score ICT vs Academic
    ict_score = 0
    acad_score = 0
    ict_specific_found = False

    for kw in ICT_KEYWORDS:
        if _contains_rule(text_lower, kw):
            ict_score += 1

    for kw in ICT_SPECIFIC_KEYWORDS:
        if _contains_rule(text_lower, kw):
            ict_specific_found = True

    for kw in ACADEMIC_KEYWORDS:
        if _contains_rule(text_lower, kw):
            acad_score += 1

    # Step 5: Decide category
    # Block Other categories override only if meaningful ICT/Academic signal exists
    # Meaningful = score >= 2 OR specific infrastructure keyword found
    meaningful_ict = ict_score >= 2 or (ict_score >= 1 and ict_specific_found)
    meaningful_acad = acad_score >= 2

    if meaningful_ict or meaningful_acad:
        if acad_score > ict_score:
            return 'Academic', min(0.5 + acad_score * 0.1, 0.95), f"Academic score {acad_score} > ICT {ict_score}"
        elif ict_score > acad_score:
            return 'ICT', min(0.5 + ict_score * 0.1, 0.95), f"ICT score {ict_score} > Academic {acad_score}"
        else:
            # Tie - check context for strong ICT vs Academic signals
            def _fuzzy_match(wordlist):
                for kw in wordlist:
                    if kw in text_lower:
                        return kw
                return None
            has_strong_ict = _fuzzy_match({
                'wifi', 'internet', 'network', 'server', 'database',
                'lms', 'moodle', 'email', 'password', 'login', 'portal',
                'hardware', 'software', 'printer', 'computer', 'laptop',
                'browser', 'website', 'app', 'zoom', 'teams',
                'error', 'bug', 'crash', 'offline', 'connectivity',
            })
            has_strong_acad = _fuzzy_match({
                'exam', 'grade', 'mark', 'lecture', 'lecturer', 'professor',
                'assignment', 'coursework', 'timetable', 'syllabus', 'curriculum',
                'thesis', 'dissertation', 'tutorial', 'seminar', 'workshop',
                'registration', 'enrollment', 'semester', 'tuition', 'scholarship',
                'transcript', 'certificate', 'graduation', 'invigilator',
                'plagiarism', 'malpractice', 'supplementary', 'retake',
            })
            if has_strong_ict and not has_strong_acad:
                return 'ICT', min(0.5 + ict_score * 0.1, 0.90), f"ICT tiebreak (strong ICT signal)"
            else:
                return 'Academic', min(0.5 + acad_score * 0.1, 0.90), f"Academic tiebreak (strong Academic signal or ambiguous)"

    # Step 6: Check ACADEMIC_ICT_ANCHORS — if text has any Academic/ICT context,
    # don't route to Other categories (except 'general') — preserves canonical model behavior
    ACADEMIC_ICT_ANCHORS = [
        'assignment', 'course', 'module', 'class', 'lecture', 'lecturer', 'professor',
        'teacher', 'instructor', 'exam', 'test', 'quiz', 'grade', 'marks', 'gpa',
        'result', 'timetable', 'deadline', 'syllabus', 'curriculum', 'research', 'thesis',
        'project', 'supervisor', 'advisor', 'online class', 'course material', 'coursework',
        'studying', 'study', 'studies',
        'portal', 'login', 'password', 'email', 'wifi', 'wi-fi', 'internet', 'network',
        'computer', 'software', 'hardware', 'database', 'server', 'system',
        'lms', 'moodle', 'canvas', 'blackboard', 'e-learning', 'elearning', 'zoom',
        'teams', 'student account', 'registration portal', 'financial aid website',
    ]
    has_anchor = _first_match(text_lower, ACADEMIC_ICT_ANCHORS) is not None

    # Step 7: Check generic Other categories
    for dept, keywords in OTHER_CATEGORIES.items():
        match = _first_match(text_lower, keywords)
        if not match:
            continue
        # Preserve canonical behavior: if text has Academic/ICT context,
        # only route to 'general' Other category, not facilities/dining/etc.
        if has_anchor and dept != 'general':
            continue
        return 'Other', 0.9, f"{dept}: {match}"

    # Step 8: Fallback — honor any partial score
    if acad_score > 0:
        return 'Academic', min(0.5 + acad_score * 0.1, 0.85), f"Academic partial score {acad_score}"
    if ict_score > 0:
        return 'ICT', min(0.5 + ict_score * 0.1, 0.85), f"ICT partial score {ict_score}"
    return 'Other', 0.6, "No ICT or Academic keywords found"


def classify_complaint(complaint_text, model=None, vectorizer=None):
    """
    Classify complaint using comprehensive rule-based system.
    Categories: ICT, Academic, HOD, Other
    Returns dict with category, confidence, reason, routing info.
    """
    text = str(complaint_text)
    text_lower = text.lower()

    # First check for HOD (staff complaints) — independent of category
    # Privacy/sensitive accusations with names must be caught regardless of keywords
    is_hod, hod_reason = _detect_hod(text)
    if is_hod:
        return {
            'category': 'HOD',
            'confidence': 0.9,
            'reason': f"HOD: {hod_reason}",
            'requires_admin_review': False,
            'routing_priority': 'high',
            'department': 'Head of Department',
            'assigned_staff': 'HOD',
            'action': 'Route to HOD for sensitive complaint handling',
        }

    # Get base category by keyword scoring
    category, confidence, reason = _score_category(text_lower)

    # Map category to response
    dept_map = {
        'ICT': ('ICT Department', 'ICT Staff', 'high'),
        'Academic': ('Academic Department', 'Academic Staff', 'normal'),
        'Other': ('Admin Queue', 'ADMIN', 'medium'),
    }
    dept_name, staff_name, priority = dept_map.get(category, ('Admin Queue', 'ADMIN', 'medium'))

    return {
        'category': category,
        'confidence': confidence,
        'reason': reason,
        'requires_admin_review': category == 'Other',
        'routing_priority': priority,
        'department': dept_name,
        'assigned_staff': staff_name,
        'action': f'Route to {dept_name}',
    }
