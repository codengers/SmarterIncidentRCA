
from fastapi import FastAPI, Request
from groq_agent.rca_analyzer import analyze_incident
from servicenow.api_handler import update_incident_notes
import uvicorn
import re
import html

app = FastAPI()

def format_rca_for_servicenow(raw_text):
    # Extract just the content part
    content_match = re.search(r"content='(.*?)'[\s,]", raw_text, re.DOTALL)
    if not content_match:
        #return "No RCA content found."
        content = raw_text
    else:   
        content = content_match.group(1)

    # Decode HTML and escape sequences
    content = html.unescape(content)
    content = content.encode().decode('unicode_escape')  # Handle \n and others

    # Clean and beautify
    content = content.strip()
    formatted = f"""🧠 *RCA Bot Suggestion*\n\n{content}"""
    return formatted

@app.post("/analyze_incident")
async def analyze_incident_endpoint(request: Request):
    data = await request.json()
    incident_id = data.get("incident_id")
    sys_id = data.get("sys_id")
    analysis = analyze_incident(data)
    formatted_rca = format_rca_for_servicenow(analysis)
    update_incident_notes(sys_id, formatted_rca)
    return {"status": "RCA posted", "incident_id": incident_id, "RCA": formatted_rca}

def start_webhook_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)