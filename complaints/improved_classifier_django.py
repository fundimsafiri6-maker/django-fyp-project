"""
Improved Complaint Classifier with Out-of-Department Detection and Admin Routing

This module provides ML-based complaint classification with automatic detection
of out-of-department complaints and admin routing for system cleanup.
"""

import joblib
import os
import re
import numpy as np
import pandas as pd
from datetime import datetime


class OutOfDepartmentDetector:
    """
    Detects complaints that do not fit ICT or Academic departments.
    These complaints should be routed to ADMIN for human review/handling.
    """

    def __init__(self, confidence_threshold=0.65):
        self.confidence_threshold = confidence_threshold
        self.academic_ict_anchors = [
            'assignment', 'course', 'module', 'class', 'lecture', 'lecturer', 'professor',
            'teacher', 'instructor', 'exam', 'test', 'quiz', 'grade', 'marks', 'gpa',
            'result', 'timetable', 'deadline', 'syllabus', 'curriculum', 'research', 'thesis',
            'project', 'supervisor', 'advisor', 'online class', 'course material', 'coursework',
            'portal', 'login', 'password', 'email', 'wifi', 'wi-fi', 'internet', 'network',
            'computer', 'software', 'hardware', 'database', 'server', 'system', 'printer',
            'lms', 'moodle', 'canvas', 'blackboard', 'e-learning', 'elearning', 'zoom',
            'teams',             'student account', 'registration portal', 'financial aid website',
            'classroom', 'unclear', 'unclear deadline', 'deadline unclear', 'unclear assignment',
            'assignment unclear', 'unclear instructions', 'instructions unclear'
        ]
        self.personal_welfare = [
            'i want to go home', 'want to go home', 'go home', 'going home', 'homesick',
            'miss home', 'missing home', 'leave campus', 'leave school', 'drop out',
            'withdraw from school', 'lonely', 'bored', 'sad', 'depressed', 'mental health',
            'panic attack', 'anxiety', 'counselling', 'counseling', 'personal problem',
            'family problem', 'family emergency', 'not feeling well', 'hungry', 'thirsty',
            'sleepy', 'tired', 'run away', 'runaway', 'escape', 'want to leave', 'leaving',
            'quit', 'quitting', 'give up', 'stressed', 'stress', 'overwhelmed', 'burnout',
            'exhausted', 'worried', 'worry', 'scared', 'afraid', 'fear', 'nervous',
            'unhappy', 'miserable', 'hopeless', 'helpless', 'alone', 'isolated', 'loneliness',
            'cry', 'crying', 'tears', 'upset', 'angry', 'frustrated', 'annoyed', 'irritated',
            'disappointed', 'heartbroken', 'broken heart', 'grief', 'mourning', 'loss'
        ]
        self.out_of_dept_keywords = {
            'facilities': [
                'bathroom', 'toilet', 'restroom', 'washroom', 'sink', 'sewer', 'sewage',
                'water', 'dirty water', 'leak', 'leaking', 'pipe', 'tap', 'flood', 'flooded',
                'drainage', 'electricity', 'power cut', 'blackout', 'bulb', 'lighting',
                'fan', 'air conditioner', 'ac', 'heating', 'cooling', 'ventilation',
                'temperature', 'too hot', 'too cold', 'cold', 'hot',
                'building', 'facility', 'maintenance', 'repair', 'broken', 'damaged',
                'crack', 'door', 'window', 'desk', 'chair', 'table', 'furniture', 'seat',
                'roof', 'ceiling', 'floor', 'stairs', 'elevator', 'lift', 'cleanliness',
                'sanitation', 'hygiene', 'dustbin', 'trash', 'garbage', 'bad smell', 'dirty'
            ],
            'dining': [
                'food', 'meal', 'breakfast', 'lunch', 'dinner', 'cafeteria', 'canteen',
                'dining', 'restaurant', 'kitchen', 'menu', 'catering', 'stale food',
                'spoiled food', 'food poisoning', 'expensive food', 'eat', 'eating',
                'hungry', 'thirsty', 'drink', 'snack', 'cook', 'cooking', 'makange'
            ],
            'accommodation': [
                'hostel', 'dorm', 'dormitory', 'residence', 'accommodation', 'roommate',
                'room mate', 'bed', 'mattress', 'bunk', 'hostel room', 'residence hall',
                'housing', 'landlord', 'rent', 'eviction', 'room allocation'
            ],
            'security': [
                'security', 'guard', 'unsafe', 'not safe', 'safety', 'theft', 'stolen',
                'robbery', 'robbed', 'lost property', 'missing item', 'violence', 'fight',
                'assault', 'attack', 'threat', 'threatened', 'weapon', 'drug', 'alcohol',
                'fire', 'emergency', 'accident', 'injury', 'danger', 'dangerous'
            ],
            'transport': [
                'transport', 'bus', 'shuttle', 'vehicle', 'parking', 'car park', 'taxi',
                'boda', 'commute', 'traffic', 'pickup', 'drop off', 'driver', 'transportation'
            ],
            'health': [
                'clinic', 'hospital', 'medical', 'medicine', 'pharmacy', 'nurse',
                'doctor appointment', 'health center', 'health centre', 'ambulance',
                'first aid', 'treatment', 'vaccination', 'sick leave', 'illness', 'fever'
            ],
            'accessibility': [
                'disability', 'disabled', 'wheelchair', 'ramp', 'accessible', 'accessibility',
                'special needs', 'reasonable accommodation', 'accommodation request',
                'sign language', 'hearing impaired', 'visually impaired', 'braille'
            ],
            'admin': [
                'admission', 'application form', 'admission letter', 'transcript', 'certificate',
                'diploma', 'graduation clearance', 'clearance', 'student id', 'id card',
                'identity card', 'record office', 'registrar office', 'document', 'documents',
                'approval', 'permission', 'policy', 'procedure', 'regulation', 'appeal form',
                'office closed', 'administration'
            ],
            'finance': [
                'refund', 'billing', 'invoice', 'receipt', 'reimbursement', 'overcharged',
                'double charged', 'salary', 'wage', 'allowance', 'stipend not paid',
                'cashier', 'bank slip', 'control number', 'sponsor payment'
            ],
            'general': ['other', 'misc', 'miscellaneous', 'general', 'nonsense', 'random',
                'poverty', 'poor', 'rich', 'wealth', 'life', 'living', 'situation',
                'condition', 'matter', 'thing', 'something', 'anything', 'everything',
                'nothing', 'not good', 'not bad', 'terrible', 'horrible', 'awful',
                'worst', 'best', 'better', 'worse', 'struggling', 'suffering', 'pain',
                'problem', 'issue', 'concern', 'love', 'i love', 'thank you', 'thanks',
                'run', 'want to run', 'i want to run', 'go', 'want to go', 'i want to go',
                'play', 'want to play', 'i want to play', 'eat', 'want to eat', 'i want to eat',
                'sleep', 'want to sleep', 'i want to sleep', 'drink', 'want to drink', 'i want to drink',
                'wife', 'need a wife', 'i need a wife', 'husband', 'need a husband', 'i need a husband',
                'marriage', 'marry', 'want to marry', 'spouse', 'girlfriend', 'boyfriend',
                'dating', 'relationship', 'partner', 'romantic', 'love life'
            ],
            'greetings': [
                'hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening',
                'how are you', 'how are you doing', 'whats up', "what's up", 'greetings',
                'good day', 'nice to meet you', 'pleased to meet you'
            ]
        }

    def _contains(self, text_lower, keyword):
        keyword = keyword.lower()
        if ' ' in keyword or '-' in keyword or '/' in keyword:
            return keyword in text_lower
        return re.search(rf'\b{re.escape(keyword)}\b', text_lower) is not None

    def _first_match(self, text_lower, keywords):
        for keyword in keywords:
            if self._contains(text_lower, keyword):
                return keyword
        return None

    def is_out_of_department(self, text):
        text_lower = str(text).lower()
        has_anchor = self._first_match(text_lower, self.academic_ict_anchors) is not None
        personal = self._first_match(text_lower, self.personal_welfare)
        if personal and not has_anchor:
            return True, f'personal/welfare: {personal}'

        for dept, keywords in self.out_of_dept_keywords.items():
            match = self._first_match(text_lower, keywords)
            if not match:
                continue
            if dept in {'facilities', 'finance'}:
                ict_context = self._first_match(text_lower, [
                    'portal', 'website', 'login', 'password', 'email', 'system', 'software',
                    'database', 'server', 'network', 'wifi', 'internet', 'student account'
                ])
                physical_context = self._first_match(text_lower, [
                    'bathroom', 'toilet', 'water', 'leak', 'flood', 'electricity', 'bulb',
                    'building', 'door', 'window', 'desk', 'chair', 'dirty', 'refund',
                    'invoice', 'receipt', 'overcharged', 'cashier', 'bank slip', 'control number'
                ])
                if ict_context and not physical_context:
                    continue
            return True, f'{dept}: {match}'

        question = self._first_match(text_lower, ['where is', 'when is', 'how to', 'can i', 'who can', 'need information about'])
        service = self._first_match(text_lower, [
            'admission', 'transcript', 'certificate', 'id card', 'registrar', 'office',
            'clearance', 'refund', 'invoice', 'hostel', 'transport', 'clinic', 'security'
        ])
        if question and service:
            return True, f'admin/service inquiry: {question} {service}'

        return False, None

    def should_mark_as_other(self, prediction, confidence, original_text):
        is_ood, dept = self.is_out_of_department(original_text)
        if is_ood:
            return True, f'Out-of-department ({dept})'
        word_count = len(str(original_text).split())
        if word_count < 3 and str(original_text).strip().lower() in {'hi', 'hello', 'test', 'help'}:
            return True, 'Vague/incomplete non-complaint'
        return False, 'Valid Academic/ICT classification'


class HODDetector:
    """
    Detects privacy-sensitive complaints involving named or identifiable staff.
    Positive feedback about staff is not routed to HOD.
    """

    def __init__(self):
        self.staff_indicators = [
            'lecturer', 'lecture', 'professor', 'prof', 'doctor', 'dr', 'teacher',
            'instructor', 'tutor', 'supervisor', 'advisor', 'adviser', 'mentor',
            'course coordinator', 'module coordinator', 'program coordinator', 'programme coordinator',
            'dean', 'hod', 'head of department', 'department head', 'chairperson', 'chair',
            'faculty', 'staff', 'employee', 'administrator', 'admin officer', 'academic officer',
            'lab technician', 'technician', 'ict officer', 'it officer', 'system administrator',
            'support staff', 'registrar', 'exam officer', 'invigilator', 'marker', 'examiner',
            'mr', 'mrs', 'ms', 'miss', 'madam', 'sir'
        ]
        self.serious_keywords = [
            'harassment', 'sexual harassment', 'assault', 'abuse', 'threat', 'threaten',
            'threatened', 'intimidation', 'bullying', 'discrimination', 'racism', 'tribalism',
            'sexism', 'favoritism', 'favouritism', 'bribe', 'bribery', 'corruption',
            'retaliation', 'victimization', 'victimisation', 'blackmail', 'coercion',
            'inappropriate', 'misconduct', 'unethical', 'humiliated', 'insulted', 'abused',
            'biased', 'bias', 'unfair', 'unjust', 'mistreat', 'mistreatment'
        ]
        self.privacy_keywords = [
            'unprofessional', 'rude', 'arrogant', 'disrespectful', 'insult', 'shout',
            'mocked', 'ignored', 'neglect', 'biased', 'unfair', 'complaint', 'grievance',
            'issue with', 'problem with', 'concern about', 'report against', 'against',
            'attitude', 'behavior', 'behaviour', 'does not explain', "doesn't explain",
            "don't explain", 'do not explain', 'does not teach', "doesn't teach", "don't teach",
            'do not teach', "don't understand", 'dont understand', 'do not understand',
            'cannot understand', "can't understand", 'marks unfairly', 'grading unfair',
            'changed my marks', 'failed me unfairly', 'withheld results', 'delays feedback'
        ]
        self.positive_keywords = [
            'helpful', 'excellent', 'good', 'great', 'professional', 'supportive', 'friendly',
            'kind', 'appreciate', 'thank', 'thanks', 'love', 'amazing', 'best', 'clear',
            'explains well', 'teaches well', 'respectful'
        ]
        self.name_stopwords = {
            'is', 'was', 'are', 'were', 'the', 'our', 'my', 'a', 'an', 'to', 'for', 'of',
            'not', 'but', 'and', 'or', 'in', 'on', 'at', 'from', 'with', 'without', 'very',
            'really', 'always', 'never', 'good', 'bad', 'rude', 'late', 'fair', 'unfair',
            'helpful', 'excellent', 'professional', 'supportive', 'kind', 'friendly'
        }

    def _contains(self, text_lower, keyword):
        keyword = keyword.lower()
        if ' ' in keyword or '-' in keyword or '/' in keyword:
            return keyword in text_lower
        return re.search(rf'\b{re.escape(keyword)}\b', text_lower) is not None

    def _first_match(self, text_lower, keywords):
        for keyword in keywords:
            if self._contains(text_lower, keyword):
                return keyword
        return None

    def is_privacy_sensitive(self, text):
        text_lower = str(text).lower()
        original_text = str(text)
        score = 0
        reasons = []
        staff_found = False
        name_found = False
        complaint_found = False
        serious_found = False

        staff = self._first_match(text_lower, self.staff_indicators)
        if staff:
            staff_found = True
            score += 2
            reasons.append(f'staff role: {staff}')

        serious = self._first_match(text_lower, self.serious_keywords)
        if serious:
            serious_found = True
            complaint_found = True
            score += 5
            reasons.append(f'serious issue: {serious}')

        complaint = self._first_match(text_lower, self.privacy_keywords)
        if complaint:
            complaint_found = True
            score += 2
            reasons.append(f'complaint context: {complaint}')

        positive = self._first_match(text_lower, self.positive_keywords)
        if positive:
            score -= 4
            reasons.append(f'positive sentiment: {positive}')

        role_pattern = rf"\b(?:{'|'.join(re.escape(k) for k in self.staff_indicators)})\.?\s+(?:called\s+|named\s+)?([a-zA-Z]{{2,}})\b"
        role_match = re.search(role_pattern, original_text, re.IGNORECASE)
        if role_match:
            possible = re.sub(r'[^A-Za-z]', '', role_match.group(1)).lower()
            if possible and possible not in self.name_stopwords and possible not in self.staff_indicators:
                name_found = True
                score += 3
                reasons.append(f'staff name: {role_match.group(1)}')

        name_before_role = rf"\b([A-Z][a-z]{{2,}})\s+(?:is|was|becomes|became)\s+(?:our|my|the|a|an)?\s*(?:{'|'.join(re.escape(k) for k in self.staff_indicators)})\b"
        name_match = re.search(name_before_role, original_text)
        if name_match:
            name_found = True
            score += 3
            reasons.append(f'staff name: {name_match.group(1)}')

        accusation_verbs = [
            'is', 'was', 'has', 'have', 'keeps', 'always', 'never', 'changed', 'lost',
            'gave', 'failed', 'refused', 'denied', 'threatened', 'harassed', 'insulted',
            'abused', 'asked', 'demanded', 'delayed', 'withheld'
        ]
        accusation_terms = self.serious_keywords + self.privacy_keywords
        named_pattern = r"\b([A-Z]{2,}|[A-Z][a-z]{2,})\b\s+(?:" + "|".join(re.escape(v) for v in accusation_verbs) + r")\b.{0,80}"
        named_match = re.search(named_pattern, original_text)
        if named_match:
            possible_name = named_match.group(1)
            context = named_match.group(0).lower()
            if possible_name.lower() not in self.name_stopwords and self._first_match(context, accusation_terms):
                name_found = True
                complaint_found = True
                score += 5
                reasons.append(f'named person with accusation: {possible_name}')

        if positive and not complaint_found and not serious_found:
            return False, 'Positive staff feedback, not a privacy complaint'
        if staff_found and serious_found:
            return True, '; '.join(reasons)
        if staff_found and name_found and (complaint_found or score >= 5):
            return True, '; '.join(reasons)
        if staff_found and complaint_found and score >= 4:
            return True, '; '.join(reasons)
        if name_found and serious_found and score >= 6:
            return True, '; '.join(reasons)
        if name_found and complaint_found and score >= 5:
            return True, '; '.join(reasons)
        return False, 'Not a privacy-sensitive complaint'


class AdminRoutingSystem:
    """
    Routes out-of-department complaints ('other' category) and privacy-sensitive 
    complaints ('HOD' category) to appropriate queues.
    """

    ACTION_MAPPING = {
        'facilities': {
            'action': 'ROUTE_TO_FACILITIES',
            'department': 'Facilities Management',
            'auto_delete': False,
            'review_level': 'standard'
        },
        'finance': {
            'action': 'ROUTE_TO_FINANCE',
            'department': 'Finance Department',
            'auto_delete': False,
            'review_level': 'standard'
        },
        'admin': {
            'action': 'MARK_FOR_REVIEW',
            'department': 'Admin Panel',
            'auto_delete': False,
            'review_level': 'high'
        },
        'general': {
            'action': 'MARK_FOR_DELETION',
            'department': 'System Cleanup',
            'auto_delete': True,
            'review_level': 'high'
        },
        'hod': {
            'action': 'ROUTE_TO_HOD',
            'department': 'Head of Department',
            'auto_delete': False,
            'review_level': 'high'
        }
    }
    
    def __init__(self, ood_detector):
        self.ood_detector = ood_detector
        self.admin_queue = []

    def get_admin_action(self, classification_result):
        """
        Determine admin action based on classification.
        Returns admin routing instructions for out-of-department and HOD complaints.
        """
        category = classification_result['category']

        if category == 'hod':
            action_config = self.ACTION_MAPPING['hod']
            return {
                'action': action_config['action'],
                'department': action_config['department'],
                'requires_admin': True,
                'auto_delete': action_config['auto_delete'],
                'review_level': action_config['review_level'],
                'reason': classification_result['reason'],
                'original_category': category,
                'confidence': classification_result.get('confidence', 1.0)
            }

        if category != 'other':
            return {'action': 'PROCESS_NORMALLY', 'requires_admin': False}

        reason = classification_result['reason']
        department = 'general'
        
        for dept in self.ACTION_MAPPING.keys():
            if dept in reason.lower():
                department = dept
                break
        
        action_config = self.ACTION_MAPPING[department]
        
        return {
            'action': action_config['action'],
            'department': action_config['department'],
            'requires_admin': True,
            'auto_delete': action_config['auto_delete'],
            'review_level': action_config['review_level'],
            'reason': reason,
            'original_category': classification_result['original_category'],
            'confidence': classification_result['original_confidence']
        }
    
    def add_to_admin_queue(self, complaint_id, complaint_text, admin_action):
        """Add complaint to admin queue for review"""
        queue_entry = {
            'id': complaint_id,
            'text': complaint_text,
            'action': admin_action['action'],
            'department': admin_action['department'],
            'auto_delete': admin_action['auto_delete'],
            'review_level': admin_action['review_level'],
            'reason': admin_action['reason'],
            'timestamp': datetime.now(),
            'status': 'pending_review'
        }
        self.admin_queue.append(queue_entry)
        return queue_entry


class ImprovedComplaintClassifier:
    """
    Enhanced classifier combining ML predictions with out-of-department detection 
    and HOD (privacy-sensitive) detection.
    Routes non-departmental complaints as 'other' to admin and privacy-sensitive 
    complaints as 'HOD' to Head of Department.
    """

    _instance = None

    def __init__(self, model_path=None):
        """
        Initialize classifier with pre-trained models.

        Args:
            model_path: Path to ML models directory (optional for Django settings)
        """
        if model_path is None:
            possible_paths = [
                'ml_models/',
                './ml_models/',
                '../ml_models/',
                '/app/ml_models/',
            ]

            for path in possible_paths:
                if os.path.exists(os.path.join(path, 'improved_classifier.pkl')):
                    model_path = path
                    break

        if model_path is None:
            raise ValueError("Could not find ml_models directory. Specify model_path explicitly.")

        self.improved_clf = joblib.load(os.path.join(model_path, 'improved_classifier.pkl'))
        self.admin_router = joblib.load(os.path.join(model_path, 'admin_router.pkl'))

        self.ood_detector = OutOfDepartmentDetector()
        self.hod_detector = HODDetector()
    
    @classmethod
    def get_instance(cls, model_path=None):
        """Singleton pattern for Django"""
        if cls._instance is None:
            cls._instance = ImprovedComplaintClassifier(model_path)
        return cls._instance
    
    def classify_and_route(self, complaint_text):
        """
        Classify complaint and determine if it should go to admin queue or HOD.

        CORRECT WORKFLOW:
        1. FIRST: Check Other rules (without overlapping ICT/Academic keywords)
        2. SECOND: ML model predicts Academic or ICT (based on dataset training)
        3. THIRD: If ML predicts Academic/ICT, check for HOD (privacy/accusations)

        Args:
            complaint_text: Original complaint text from user

        Returns:
            {
                'category': str ('ict', 'academic', 'other', or 'hod'),
                'priority': str ('high', 'medium', 'low'),
                'confidence': float (0-1),
                'requires_admin_review': bool,
                'reason': str,
                'admin_action': dict (admin routing details if 'other' or 'hod'),
                'timestamp': datetime
            }
        """
        try:
            # Step 1: FIRST check if complaint is clearly "Other" (out-of-department)
            local_is_other, local_other_reason = self.ood_detector.is_out_of_department(complaint_text)
            if local_is_other:
                return {
                    'category': 'other',
                    'priority': 'medium',
                    'confidence': 1.0,
                    'requires_admin_review': True,
                    'reason': f'Rule-based Other/Admin: {local_other_reason}',
                    'admin_action': 'MARK_FOR_REVIEW',
                    'admin_department': 'ADMIN',
                    'auto_delete': False,
                    'review_level': 'standard',
                    'assigned_staff': 'ADMIN',
                    'timestamp': datetime.now()
                }
            
            # Step 2: ML prediction for Academic or ICT
            result = self.improved_clf.classify_with_admin_routing(complaint_text)
            ml_category = result['category'].lower()
            ml_confidence = float(result.get('confidence', 0.85))
            
            # Step 3: Check for HOD (privacy-sensitive) for academic/ict complaints
            is_hod, hod_reason = self.hod_detector.is_privacy_sensitive(complaint_text)
            if is_hod:
                return {
                    'category': 'hod',
                    'priority': 'high',
                    'confidence': 1.0,
                    'requires_admin_review': False,
                    'reason': hod_reason,
                    'admin_action': 'ROUTE_TO_HOD',
                    'admin_department': 'HOD',
                    'auto_delete': False,
                    'review_level': 'high',
                    'original_category': ml_category,
                    'assigned_staff': 'HOD',
                    'timestamp': datetime.now()
                }
            
            # Return ML classification (academic or ict)
            category_name = ml_category if ml_category in {'academic', 'ict'} else 'other'
            return {
                'category': category_name,
                'priority': result['priority'].lower(),
                'confidence': ml_confidence,
                'requires_admin_review': False,
                'reason': result['reason'],
                'admin_action': 'PROCESS_NORMALLY',
                'admin_department': ml_category.capitalize() if ml_category in {'academic', 'ict'} else 'ADMIN',
                'auto_delete': False,
                'review_level': 'standard',
                'original_category': ml_category,
                'assigned_staff': f"{ml_category.capitalize()} Staff" if ml_category in {'academic', 'ict'} else 'ADMIN',
                'timestamp': datetime.now()
            }
        except Exception as e:
            return {
                'category': 'other',
                'priority': 'low',
                'confidence': 0.0,
                'requires_admin_review': True,
                'reason': f'Classification error: {str(e)}',
                'admin_action': 'MARK_FOR_REVIEW',
                'admin_department': 'System',
                'auto_delete': False,
                'review_level': 'high',
                'original_category': None,
                'timestamp': datetime.now()
            }


# Django Integration Helper
def get_classifier():
    """Get singleton instance of classifier for Django views"""
    return ImprovedComplaintClassifier.get_instance()


def classify_complaint(complaint_text):
    """Quick classify function for Django views"""
    classifier = get_classifier()
    return classifier.classify_and_route(complaint_text)
