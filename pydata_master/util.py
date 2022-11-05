# Copyright 2022 Thinh Vu @ GitHub
# See LICENSE for details.
import yaml
import os
import requests
import shutil
from trafilatura import fetch_url, extract

# Detect the running OS and return file path delimiter
def lmt_detect():
    if os.name == 'nt':
        lmt = '\\'
    else:
        lmt = '/'
    return lmt

ROOT_DIR = os.path.abspath(os.curdir)

# Read YAML config file
def yaml_cred(item_name, cred_path):
    with open(cred_path) as file: 
        documents = yaml.full_load(file)
        for item, doc in documents.items():
            if item == item_name:
              secret_key = doc
              return secret_key

# Download & extract a Google font to local folder
def get_google_font(font_family):
    lmt = lmt_detect()
    font_url = 'https://fonts.google.com/download?family={}'.format(font_family)
    response = requests.get(font_url)
    file_name = ROOT_DIR + lmt + '{}.zip'.format(font_family)
    with open(file_name, 'wb') as f:
        f.write(response.content)
    shutil.unpack_archive(file_name, lmt.join([ROOT_DIR, 'font', font_family]))

# Convert a web page content to text file
def web_to_text(url):
    downloaded = fetch_url(url)
    result = extract(downloaded)
    return result

# Open text file
def read_txt(path_to_file):
    with open(path_to_file) as f:
        content = f.read()
    return content
