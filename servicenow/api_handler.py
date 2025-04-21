import requests
import os
from dotenv import load_dotenv

load_dotenv()

servicenow_instance = os.environ.get("SERVICENOW_INSTANCE")
username = os.environ.get("SERVICENOW_USER")
password = os.environ.get("SERVICENOW_PASSWORD")

BASE_URL = "https://{}.service-now.com".format(servicenow_instance)
AUTH = (username, password)

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def update_incident_notes(sys_id, note):
    url = "{}/api/now/table/incident/{}".format(BASE_URL, sys_id)
    #print("URL: ", url)

    #print("payload: ", {"work_notes": note})
    #print("AUTH: ", AUTH)
    print("note: ", note)
    #print("HEADERS: ", HEADERS)
    print("")
    try:    
        payload = {"work_notes": note}
        response = requests.patch(url, auth=AUTH, headers=HEADERS, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error updating incident notes:", e)
        if response.status_code != 200:
            print("Failed to update incident:", response.text)