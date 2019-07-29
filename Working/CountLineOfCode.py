'''
Progressively Count Line of Code for all projects from a csv file
If related fields are not -1, assume they have been properly computed and skip them

Author: Hao He
'''

import pandas as pd
import requests
import subprocess
import os
import json
import shutil
import argparse
import sys
from termcolor import colored


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'csv_file',  help='Path to the CSV file storing project information')
    csv_path = parser.parse_args().csv_file

    if not os.path.exists('temp'):
        os.mkdir('temp')

    projects = pd.read_csv(csv_path)
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

        lang = row['language']
        project_path = os.path.join('../../projects/', row['name'])
        if not os.path.exists(project_path):
            print(colored(
                'No project files for {}! Skipping this entry...\n'.format(row['name'], 'red')))
            continue

        subprocess.call(
            'cloc {} --json -out=temp/stats.json'.format(project_path), shell=True)

        with open('temp/stats.json', 'r') as statsfile:
            stats = json.load(statsfile)
            try:
                projects.at[index, 'lines_of_code'] = stats[lang]['code']
                projects.at[index,
                            'lines_of_comments'] = stats[lang]['comment']
                projects.at[index, 'lines_blank'] = stats[lang]['blank']
            except KeyError:  # The language does not exist
                projects.at[index, 'lines_of_code'] = 0
                projects.at[index, 'lines_of_comments'] = 0
                projects.at[index, 'lines_blank'] = 0

        print(projects.loc[index])
        projects.to_csv(csv_path, index=False)
