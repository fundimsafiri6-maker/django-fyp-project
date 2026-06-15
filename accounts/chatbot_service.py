import os
import logging

logger = logging.getLogger(__name__)

try:
    from google.genai import Client
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    logger.warning("google.genai not installed. Chatbot will use fallback mode.")


GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-2.0-flash')

SYSTEM_PROMPT = """You are an AI assistant for the University of Dodoma (UDOM), College of Informatics and Virtual Education (CIVE) complaint management system. Your role is to help students and staff with questions about:

COMMON ICT ISSUES AT UDOM CIVE:
- Network connectivity problems (WiFi, LAN, campus network)
- Student portal login issues (portal.udom.ac.tz)
- SR2 system problems (registration, results, fees)
- Email account issues (student email, staff email)
- System errors, browser issues, slow connectivity
- Computer lab equipment, software access
- Online learning platform (Moodle, Google Classroom)
- Password reset and account recovery

COMMON ACADEMIC ISSUES AT UDOM CIVE:
- Course registration and enrollment
- Exam schedules, results, and transcripts
- Assignment submission deadlines and platforms
- Academic advising and department contacts
- Lecture schedules and classroom changes
- Fee payment and financial matters
- Internship and practical attachment
- Project supervision and research

GENERAL COMPLAINT SYSTEM QUESTIONS:
- How to submit a complaint
- How to track complaint status
- How complaint routing works (AI classification)
- Response times and escalation process
- Confidentiality and privacy
- Contact information for departments

Always provide helpful, accurate information about UDOM CIVE procedures. If you don't know something specific, direct users to the appropriate department contact. Be concise but thorough. Use markdown formatting for clarity.

Keep responses focused on UDOM CIVE and Tanzanian higher education context."""


def get_chat_response(user_message, conversation_history=None):
    if not GENAI_AVAILABLE or not GEMINI_API_KEY:
        return generate_fallback_response(user_message)

    try:
        client = Client(api_key=GEMINI_API_KEY)

        contents = []
        if conversation_history:
            for msg in conversation_history:
                role = msg.get("role", "user")
                parts = msg.get("parts", [])
                text = ""
                for part in parts:
                    if isinstance(part, dict) and "text" in part:
                        text = part["text"]
                    elif isinstance(part, str):
                        text = part
                if text:
                    contents.append(types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=text)]
                    ))

        contents.append(types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_message)]
        ))

        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.7,
            max_output_tokens=800,
            top_p=0.9,
            top_k=40,
        )

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=contents,
            config=config,
        )

        return {
            'answer': response.text,
            'sources': [],
            'from_gemini': True,
        }

    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return generate_fallback_response(user_message)


def generate_fallback_response(query):
    query_lower = query.lower()

    if 'password' in query_lower or 'reset' in query_lower or 'login' in query_lower:
        return {
            'answer': "**Password & Login Assistance (UDOM CIVE)**\n\n"
                      "1. **Student Portal**: Visit https://portal.udom.ac.tz and click 'Forgot Password'\n"
                      "2. **SR2 Password**: Contact the ICT Help Desk for SR2 password reset\n"
                      "3. **Email Account**: Email issues can be directed to ithelpdesk@udom.ac.tz\n"
                      "4. **Walk-in Support**: Visit the CIVE ICT Lab during office hours\n\n"
                      "For immediate help, contact the CIVE IT Support Office.",
            'sources': [],
            'from_gemini': False,
        }
    elif 'network' in query_lower or 'wifi' in query_lower or 'internet' in query_lower or 'connect' in query_lower:
        return {
            'answer': "**Network & Connectivity Issues (UDOM CIVE)**\n\n"
                      "Common solutions:\n"
                      "1. **WiFi not connecting**: Forget the network and reconnect\n"
                      "2. **Slow internet**: Report to ICT department with location and time\n"
                      "3. **Campus network**: Ensure you're using the correct SSID (UDOM-Staff or UDOM-Student)\n"
                      "4. **Proxy settings**: Some areas require proxy configuration\n\n"
                      "Report persistent issues via the complaint system under 'ICT' category.",
            'sources': [],
            'from_gemini': False,
        }
    elif 'registration' in query_lower or 'course' in query_lower or 'enroll' in query_lower:
        return {
            'answer': "**Course Registration (UDOM CIVE)**\n\n"
                      "Steps:\n"
                      "1. Log into the student portal (portal.udom.ac.tz)\n"
                      "2. Navigate to 'Course Registration'\n"
                      "3. Select your semester courses\n"
                      "4. Verify prerequisites are met\n"
                      "5. Submit and print confirmation\n\n"
                      "Issues? Contact your academic advisor or the CIVE Academic Office.\n"
                      "Email: academics@cive.udom.ac.tz",
            'sources': [],
            'from_gemini': False,
        }
    elif 'exam' in query_lower or 'grade' in query_lower or 'mark' in query_lower or 'result' in query_lower:
        return {
            'answer': "**Exams & Results (UDOM CIVE)**\n\n"
                      "1. **Exam Schedule**: Check the student portal or department notice board\n"
                      "2. **Results**: View grades on the portal after official release\n"
                      "3. **Missing Marks**: Contact your course lecturer or department\n"
                      "4. **Appeal Process**: Submit an appeal to the Academic Affairs office within 14 days\n\n"
                      "For specific academic concerns, visit the CIVE Dean's Office.",
            'sources': [],
            'from_gemini': False,
        }
    elif 'submit' in query_lower or 'complaint' in query_lower:
        return {
            'answer': "**How to Submit a Complaint (UDOM CIVE System)**\n\n"
                      "1. Log into your account\n"
                      "2. Click 'Submit Complaint' from the dashboard\n"
                      "3. Enter a descriptive title\n"
                      "4. Provide detailed description (what, when, where, impact)\n"
                      "5. Click Submit\n\n"
                      "Our AI system will automatically classify and route your complaint to the right department.",
            'sources': [],
            'from_gemini': False,
        }
    elif 'contact' in query_lower or 'phone' in query_lower or 'email' in query_lower or 'support' in query_lower:
        return {
            'answer': "**Contact Information (UDOM CIVE)**\n\n"
                      "- **ICT Help Desk**: ithelpdesk@udom.ac.tz\n"
                      "- **Academic Office**: academics@cive.udom.ac.tz\n"
                      "- **Dean's Office**: dean.cive@udom.ac.tz\n"
                      "- **Library**: library@udom.ac.tz\n"
                      "- **Main Campus**: +255 700 000 000\n\n"
                      "Office Hours: Monday-Friday, 8:00 AM - 5:00 PM EAT",
            'sources': [],
            'from_gemini': False,
        }
    else:
        return {
            'answer': f"I'm your UDOM CIVE AI Assistant. I can help with:\n\n"
                      "🔹 **ICT Issues**: Network, portal, password, system errors\n"
                      "🔹 **Academic Issues**: Registration, exams, courses, grades\n"
                      "🔹 **Complaints**: How to submit, track, and resolve\n"
                      "🔹 **Contact Info**: Department emails and phone numbers\n\n"
                      f"Try asking something like:\n"
                      "- 'How do I reset my portal password?'\n"
                      "- 'The campus WiFi is not working'\n"
                      "- 'How to register for courses'\n"
                      "- 'Submit a complaint about a lecturer'\n\n"
                      "Or contact: support@udom-cive.edu | +255 700 000 000",
            'sources': [],
            'from_gemini': False,
        }
