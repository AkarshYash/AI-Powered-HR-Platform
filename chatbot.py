import re

def get_chatbot_response(message: str) -> str:
    \"\"\"
    A rule-based and regex intent classifier for the HR Assistant Chatbot.
    Simulates ML inference for local environments.
    \"\"\"
    text = message.lower()
    
    # Intents
    if re.search(r'\b(schedule\s*interview|interview)\b', text):
        return "I can help you schedule an interview. Please navigate to the Applicant Management section and click the calendar icon next to the candidate."
        
    elif re.search(r'\b(open\s*positions|jobs|hiring)\b', text):
        return "You can view all open positions in the Recruitment Center. Do you want me to fetch the latest active jobs for you?"
        
    elif re.search(r'\b(reports|export|csv|pdf)\b', text):
        return "I can generate reports for you. You can find export options in the HR Analytics dashboard or use the Reports section for monthly summaries."
        
    elif re.search(r'\b(top\s*performers|performance|review)\b', text):
        return "Top performers can be tracked in the Employee Management tab. The top performer this month is Alice Smith with a 4.9 rating."
        
    elif re.search(r'\b(hello|hi|hey)\b', text):
        return "Hello! I am the IntelliHire AI Assistant. How can I help you today? You can ask me to schedule an interview, show reports, or check performance."
        
    else:
        return "I am still learning! I'm best at handling interview scheduling, showing open positions, and generating reports. Could you rephrase your question?"
