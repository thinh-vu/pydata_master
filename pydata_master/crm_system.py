# Copyright 2022 Thinh Vu @ GitHub
# See LICENSE for details.
import pandas as pd
import requests
import json
from pandas import json_normalize
import urllib.request, shutil #, zipfile
import time

# HUBSPOT
# contact_id = hs_object_id
def hs_search_contact(user_email, token_key, properties_list):
  """Search contact properties as a DataFrame with an email.
  Args:
        user_email (:obj:`str`, required): target user email to search.
        token_key (:obj:`str`, required): HubSpot Private App Token. See more: https://developers.hubspot.com/docs/api/private-apps
        properties_list (:obj:`list`, required): A list of properties you need to retrieve information. Ex: ['email', 'createdate', 'lastmodifieddate']
  """
  url = 'https://api.hubapi.com/crm/v3/objects/contacts/search'
  payload = json.dumps({
    "filterGroups": [
      {
        "filters": [
          {
            "value": "{}".format(user_email),
            "propertyName": "email",
            "operator": "EQ"
          }
        ]
      }
    ],
    "properties": "{}".format(properties_list)
  })
  headers = {'Authorization' : 'Bearer {}'.format(token_key),
             'content-type': 'application/json'}
  response = requests.post(url, headers=headers, data=payload).json()
  result = json_normalize(response['results'])
  result.columns = result.columns.str.replace('properties.','')
  return result

# FRESHCHAT

def fc_report_read(report_content):
  """Read FreshChat report. Convert JSON content into DataFrame using the output of the fc_retrieve_report function.
  Args:
  -----
  report_content (:obj:`str`, required): json contetn returned from the fc_retrieve_report function
  """
  for i in range(len(report_content['links'])):
    download_link = report_content['links'][i]['link']['href']
    file_name = 'freshchat_report2.zip'
    with urllib.request.urlopen(download_link) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    if i == 0:
      fc_report_df = pd.read_csv(file_name)
    elif i > 0:
      fc_report_df1 = pd.read_csv(file_name)
      fc_report_df = pd.concat([fc_report_df, fc_report_df1]).reset_index(drop=True)
  return fc_report_df


def fc_retrieve_report(report_id, token_key): 
  """Retrieve a FreshChat report by report ID.
  Args:
  -----
  report_id (:obj:`str`, required): a report_id that generated by the fc_extract_report function.
  token_key (:obj:`str`, required): FreshChat token key. For an approved Freshchat app, navigate to the `Settings` > `API Tokens` page and click the `Generate Token` button.
  """
  url = 'https://api.freshchat.com/v2/reports/raw/{}'.format(report_id)
  payload = {}
  headers = {'Authorization' : 'Bearer {}'.format(token_key)}
  response = requests.request("GET", url, headers=headers, data=payload, stream=True).json()
  return response


def fc_report_request(start_date, end_date, report_type, token_key): # Conversation-Created 
  """Schedule to extract a Freshchat report by report type and generate report id
  Args:
  -----
  start_date (:obj:`str`, required): Report start date in the `%Y-%m-%d` format. Ex: `2022-09-01`
  end_date (:obj:`str`, required): Report the end date in the `%Y-%m-%d` format. The reported range should be within 30 days. Ex: `2022-09-01`.
  report_type (:obj:`str`, required): Choose one of following report type: Conversation-Created, Chat-Transcript, Message-Sent, Conversation-Resolved, Conversation-Resolution-Label, Conversation-Activity, etc. See the full list here: https://developers.freshchat.com/api/#reports
  token_key (:obj:`str`, required): FreshChat token key. For an approved Freshchat app, navigate to the `Settings` > `API Tokens` page and click the `Generate Token` button.
  """
  url = 'https://api.freshchat.com/v2/reports/raw'
  payload = json.dumps({"start": "{}".format(start_date), 
            "end": "{}".format(end_date), 
            "event": "{}".format(report_type), 
            "format": "csv"
            })
  headers = {'Authorization' : 'Bearer {}'.format(token_key), 'Accept': 'application/json', 'Content-Type': 'application/json'}
  response = requests.request("POST", url, headers=headers, data=payload).json()
  report_id = response['id']
  return report_id

