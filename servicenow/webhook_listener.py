
from fastapi import FastAPI, Request
from groq_agent.rca_analyzer import analyze_incident
from servicenow.api_handler import update_incident_notes
import uvicorn
import re
import html

app = FastAPI()

# Function to clean text
def clean_text(text):

    # Try to find the content=... part using regex (greedy inside single quotes)
    match = re.search(r"content='(.*?)'\s*(\w+_kwargs|response_metadata|id|usage_metadata|$)", text, re.DOTALL)
    if not match:
        return "Note: No content found."

    raw_content = match.group(1)

    # Clean and format the content
    formatted = raw_content.replace('\\n', '\n')         # Decode newline characters
    #formatted = re.sub(r'\s*n\s*', '', formatted)         # Remove stray 'n'
    #formatted = re.sub(r'-\s*•', '•', formatted)          # Clean up bullets

    return formatted.strip()

@app.post("/analyze_incident")
async def analyze_incident_endpoint(request: Request):
    data = await request.json()
    incident_id = data.get("incident_id")
    sys_id = data.get("sys_id")
    analysis = analyze_incident(data)
    formatted_rca = clean_text(analysis)
    update_incident_notes(sys_id, formatted_rca)
    return {"status": "RCA posted", "incident_id": incident_id, "RCA": formatted_rca}

def start_webhook_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)