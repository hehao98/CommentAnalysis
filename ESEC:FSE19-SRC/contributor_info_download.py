'''
Given a repository info list, add top 500 contributor information to it
'''

import argparse
import json
import requests

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('repo_json', help="JSON file storing repository information")
    parser.add_argument('username', help="GitHub User Name")
    parser.add_argument('auth_token', help="GitHub Access Token")

    args = parser.parse_args()
    username = args.username
    auth_token = args.auth_token

    repo_info = []
    with open(args.repo_json, 'r') as f:
        repo_info = json.load(f)
    
    for repo in repo_info:
        url = 'https://api.github.com/repos/' + repo['full_name'] + '/contributors'
        repo['contributors'] = []
        while True: 
            response = requests.get(url, auth=(username, auth_token))
            print('GET {0:s} {1:d}'.format(url, response.status_code))
            repo['contributors'].extend(response.json())
            if 'next' in response.links: 
                url = response.links['next']['url']
            else:
                break
    
    with open(args.repo_json, 'w') as f:
        json.dump(repo_info, f)

    