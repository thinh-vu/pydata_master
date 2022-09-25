# Copyright 2022 Thinh Vu @ GitHub
# See LICENSE for details.
import yaml

def yaml_cred(item_name, cred_path):
    with open(cred_path) as file: 
        documents = yaml.full_load(file)
        for item, doc in documents.items():
            if item == item_name:
              secret_key = doc
              return secret_key


