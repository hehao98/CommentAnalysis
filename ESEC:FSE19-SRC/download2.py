'''
Download repositories using information in temp/repo_info_selected.json

Created By He, Hao at 2019-04-05
'''

import json
import os
import subprocess

repo_info = []
with open('temp/repo_info_selected.json') as f:
    repo_info = json.load(f)

if os.access('../projects', os.F_OK) == False:
    os.mkdir('../projects')

os.chdir('../projects')

# Download and arrange repos by language
languages = []
for repo in repo_info:
    lang = repo['language']
    if not lang in languages:
        languages.append(lang)
        if os.access(lang, os.F_OK) == False:
            os.mkdir(lang)
    os.chdir(lang)
    if os.access(repo['name'], os.F_OK) == True:
        print('Skipping ' + repo['full_name'] +
              ' because folder already exists')
        os.chdir('..')
        continue
    url = 'https://github.com/' + repo['full_name']
    subprocess.call('git clone ' + url, shell=True)
    print(url + ' has been cloned!')
    os.chdir('..')
