
from fastapi import FastAPI, Request
from groq_agent.rca_analyzer import analyze_incident
from servicenow.api_handler import update_incident_notes
import re
import html

# Function to clean text
def clean_text(text):
    # Remove 'additional_kwargs={...} response_metadata={...} id='...' usage_metadata={...}'
    cleaned_text = re.sub(r"additional_kwargs=\{.*?usage_metadata=\{.*?\}", "", text)
    text = cleaned_text.strip()
    content_prefix = "content="
    if content_prefix in text:
        start_index = text.find(content_prefix) + len(content_prefix)
        content_str = text[start_index:].strip()
        if content_str.startswith('"') and content_str.endswith('"'):
            content_str = content_str[1:-1]
        elif content_str.startswith("'") and content_str.endswith("'"):
            content_str = content_str[1:-1]
        content_str = content_str.replace('\\n', '\n')
        return content_str.strip()
    else:
        return text.strip()

def analyze_incident_endpoint(data):
    incident_id = data.get("incident_id")
    sys_id = data.get("sys_id")
    analysis = analyze_incident(data)
    formatted_rca = clean_text(analysis)
    update_incident_notes(sys_id, formatted_rca)
    return {"status": "RCA posted", "incident_id": incident_id, "RCA": formatted_rca}
