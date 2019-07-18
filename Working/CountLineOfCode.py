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
            code = requests.get('http://localhost:23333/file/{}'.format(f['sha'])).json()['content']
            output = 'temp/tempProject/{}'.format(f['filename'])
            os.makedirs(os.path.dirname(output), exist_ok=True)
            with open(output, 'w') as tmp_file:
                tmp_file.write(code)
        subprocess.call('cloc temp/tempProject --json -out=temp/stats.json', shell=True)
        with open('temp/stats.json', 'r') as statsfile:
            stats = json.load(statsfile)
            row['lines_of_code'] = stats[lang]['code']
            row['lines_of_comments'] = stats[lang]['comment']
            row['lines_blank'] = stats[lang]['blank']
        print(row)
        projects.to_csv('result/Projects.csv')
        
        