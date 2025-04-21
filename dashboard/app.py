import streamlit as st
import requests
import pandas as pd

import math
import pandas as pd

def sanitize_for_json(data_dict):
    """Replace NaN values with None for JSON serialization."""
    return {k: (None if (isinstance(v, float) and (pd.isna(v) or math.isnan(v))) else v) for k, v in data_dict.items()}

st.set_page_config(page_title="Real-time Incident RCA Dashboard", layout="wide")
st.title("📊 RCA Dashboard")

# Load incident data (could come from ServiceNow directly)
if "data" not in st.session_state:
    st.session_state.data = []

uploaded_file = st.file_uploader("Upload Incidents CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state.data = df.to_dict("records")
    st.success("Incidents loaded")

if st.session_state.data:
    for incident in st.session_state.data:
        with st.expander(f"{incident['incident_id']} - {incident['short_description']}"):
            st.write(incident)
            if st.button("Run RCA", key=incident['incident_id']):
                sanitized_incident = sanitize_for_json(incident)
                response = requests.post("http://localhost:8000/analyze_incident", json=sanitized_incident)
                st.write(response.json())