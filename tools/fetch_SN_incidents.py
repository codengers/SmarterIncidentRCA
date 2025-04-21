import  os
from dotenv import load_dotenv
import pandas as pd
import requests
import json

load_dotenv()

def get_SN_incidents():

    try:
        # Set the request parameters
        url = 'https://dev303713.service-now.com/api/now/table/incident?sysparm_limit=10'
        headers = {'Content-Type': 'application/json','Accept':'application/json'}
        username = os.environ.get("SERVICENOW_USER")
        password = os.environ.get("SERVICENOW_PASSWORD")
        auth = (username,password)
        # Do the HTTP request
        response = requests.get(url, auth=auth, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['result']
    except json.decoder.JSONDecodeError as e:
        text_data = response.text
        print("text_data: ", text_data)
    except requests.exceptions.RequestException as e:
        print("Request error: {}".format(e))
    except ValueError as e:
        print("Value error: {}".format(e))

#create function to create csv file using pandas
def create_csv_file(results):
    data_json_list=[]
    for data in results:
        data_json={'sys_id': data['sys_id'],
               'incident_id': data['number'],
               'short_description': data['short_description'],
               'description': data['description'],
               'assignment_group': data['assignment_group'],
               'category': data['category']
              }
        data_json_list.append(data_json)
    df = pd.DataFrame(data_json_list)
    df.to_csv('SN_incident_data.csv', index=False)
    print("CSV file created successfully!")


resp = get_SN_incidents()
create_csv_file(resp)


