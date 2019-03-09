"""
Download whole repositories based on information from result/repolist.json
The repository will be in temp/ folder, separated by language and field
"""

import os
import json
import subprocess

# Load repository names from JSON file
repolist_json = ""
with open('result/repolist.json', 'r') as json_file:
    repolist_json = json_file.read()
repolist = json.loads(repolist_json)

# Create download folder out of this project
# To keep IDE from scanning the downloaded code (extremely CPU intensive)
if os.access('../projects', os.F_OK) is False:
    os.mkdir('../projects')
os.chdir('../projects')

# Download repositories for each language
languages = ['cpp', 'java', 'py', 'js']
for lang in languages:
    if os.access(lang, os.F_OK) is False:
        os.mkdir(lang) 
    os.chdir(lang)
    field_list = repolist[lang + 'list']
    for field in field_list:
        if os.access(field, os.F_OK) is False:
            os.mkdir(field)
        existing_dirs = os.listdir(field)
        os.chdir(field)
        for repo in repolist[lang + 'list'][field]:
            print(repo)
            repo = repo.split('/')
            user = repo[0]
            reponame = repo[1]
            r = 'https://github.com/%s/%s.git' % (user, reponame)
            if reponame in existing_dirs:
                # Simple heuristic for detecting duplicate and existing download
                continue
            subprocess.call('git clone %s' % r, shell=True)  # execute cmd
            print("%s/%s has been cloned!" % (user, reponame))
        os.chdir('..')
    os.chdir('..')

print('success!')
