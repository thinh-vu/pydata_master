# Copyright 2022 Thinh Vu @ GitHub
# See LICENSE for details.
import requests
import json
from pandas import json_normalize

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

