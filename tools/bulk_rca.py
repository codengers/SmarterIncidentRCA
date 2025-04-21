import csv
import requests

with open("incident_data.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"Running RCA for {row['incident_id']}...")
        response = requests.post("http://localhost:8000/analyze_incident", json=row)
        print(response.json())