'''
Count Line of Code for all projects in Projects.csv

Author: Hao He
'''

import pandas as pd
import requests
import subprocess
import os
import json
import shutil


if __name__ == '__main__':
    if not os.path.exists('temp'): 
        os.mkdir('temp')

    projects = pd.read_csv('result/Projects.csv')
    if 'lines_of_code' not in projects:
        projects['lines_of_code'] = -1
    if 'lines_of_comments' not in projects:
        projects['lines_of_comments'] = -1
    if 'lines_blank' not in projects:
        projects['lines_blank'] = -1

    print(projects.head())
    for index, row in projects.iterrows():
        if row['lines_of_code'] != -1: 
            continue
        
        # Initialize Directories
        if os.path.exists('temp/tempProject'):
            shutil.rmtree('temp/tempProject', ignore_errors=True)
        os.mkdir('temp/tempProject')

        lang = row['language']
        r = requests.get('http://localhost:23333/project/{}'.format(row['name']))
        files = r.json()['files']
        for f in files:
            code = ''
            try:
                code = requests.get('http://localhost:23333/file/{}'.format(f['sha'])).json()['content']
            except ValueError: # The file is corrupted for unknown reasons
                print('Something went wrong fetching {}...'.format(f))
            output = 'temp/tempProject/{}'.format(f['filename'])
            os.makedirs(os.path.dirname(output), exist_ok=True)
            with open(output, 'w') as tmp_file:
                tmp_file.write(code)
        subprocess.call('cloc temp/tempProject --json -out=temp/stats.json', shell=True)
        with open('temp/stats.json', 'r') as statsfile:
            stats = json.load(statsfile)
            try:
                projects['lines_of_code'][index] = stats[lang]['code']
                projects['lines_of_comments'][index] = stats[lang]['comment']
                projects['lines_blank'][index] = stats[lang]['blank']
            except KeyError: # The language does not exist
                projects['lines_of_code'][index] = 0
                projects['lines_of_comments'][index] = 0
                projects['lines_blank'][index] = 0
        print(projects.loc[index])
        projects.to_csv('result/Projects.csv', index=False)
        
        