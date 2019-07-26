'''
Given project list from temp/FinalProjects.json, add additional metadata from GitHub
Save results to temp/FinalProjectsWithGitHubInfo.json

Author: He, Hao
'''

import os
import csv
import json
import requests
import argparse
import time
import datetime
import sys

username = ''
auth_token = ''

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('username', help="GitHub User Name")
    parser.add_argument('auth_token', help="GitHub Access Token")
    args = parser.parse_args()
    username = args.username
    auth_token = args.auth_token

    project_list = []
    new_project_list = []
    new_project_names = set()
    with open('temp/FinalProjects.json', 'r') as f:
        project_list = json.load(f)
    if os.path.isfile('temp/FinalProjectsWithGitHubInfo.json'):
        with open('temp/FinalProjectsWithGitHubInfo.json', 'r') as f:
            new_project_list = json.load(f)
            new_project_names = set([proj['full_name'] for proj in new_project_list])

    print('Retrieving info for {} projects...'.format(len(project_list)))
    for proj in project_list:
        if proj['name'].replace('_', '/') in new_project_names:
            continue
        try: 
            info_url = 'https://api.github.com/repos/{}'.format(proj['name'].replace('_', '/'))
            r = requests.get(info_url, auth=(username, auth_token))
            rate_remaining = int(r.headers['X-RateLimit-Remaining'])
            if rate_remaining <= 0:
                epoch_time = int(r.headers['X-RateLimit-Reset'])
                sleep_time = max(0, epoch_time - time.time() + 20)
                print('Exceeding rate limit, sleeping for {} seconds'.format(sleep_time))
                time.sleep(sleep_time)
            if r.status_code != 200: # Errors
                print('ERROR: Status code {} when accessing {}'.format(r.status_code, info_url))
                continue
            info = r.json()
            new_project_list.append(info)
            new_project_names.add(info['full_name'])
            print('{}: Retrieved {}, {} requests remaining in this time period'
                .format(datetime.datetime.now(), info_url, rate_remaining))
        except:
            print('Error when retrieving {}'.format(proj['name']), sys.exc_info()[0])
        # Wrtie to file for every 100 requests
        if len(new_project_list) % 100 == 0:
            with open('temp/FinalProjectsWithGitHubInfo.json', 'w') as f:
                f.write(json.dumps(new_project_list))
            
    with open('temp/FinalProjectsWithGitHubInfo.json', 'w') as f:
        f.write(json.dumps(new_project_list))
    
    print('Retrieved info of {} projects from GitHub'.format(len(new_project_list)))