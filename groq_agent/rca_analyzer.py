from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from memory.search_memory import get_similar_incidents

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",  # You can also try "llama3-70b-8192"
    temperature=0.2,
    api_key=GROQ_API_KEY
)

TEMPLATE = """
You are an AI assistant performing Root Cause Analysis for IT incidents.
Given the incident details, analyze the likely cause and suggest a fix.

Incident ID: {incident_id}
Short Description: {short_description}
Description: {description}
Assignment Group: {assignment_group}
Category: {category}

Similar Incidents:
{similar_cases}

Respond in this format:
- Root Cause:
- Suggested Fix:
- Related Incidents (if any):
"""

prompt = PromptTemplate(
    input_variables=["incident_id", "short_description", "description", "assignment_group", "category", "similar_cases"],
    template=TEMPLATE
)

def analyze_incident(data):
    similar_cases = get_similar_incidents(data)
    data["similar_cases"] = similar_cases
    formatted_prompt = prompt.format(**data)
    result = llm.invoke(formatted_prompt)
    return "\n\nRCA Bot Suggestion:\n\n{}".format(result)