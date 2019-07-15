'''
Using information from temp/FinalProjectsWithGitHubInfo.json, build a csv file
Will query world of code for additional information
The result will be saved to result/Projects.csv

Author: He, Hao
'''

import json
import unicodecsv as csv
import os
import sys
import oscar.oscar as oscar

if __name__ == '__main__':
    print('Reading JSON in temp/FinalProjectsWithGitHubInfo.json...')
    project_info = []
    with open('temp/FinalProjectsWithGitHubInfo.json', 'r') as f:
        project_info = json.load(f)
    if not os.path.exists('result/'):
        os.mkdir('result/')

    print('Writing to result/Projects.csv...')
    counter = 0
    with open('result/Projects.csv', 'w') as f:
        fieldnames = ['name', 'url', 'description', 'size', 'stars', 
            'watchers', 'language', 'forks', 'commits', 'authors']
        writer = csv.DictWriter(f, fieldnames=fieldnames, encoding='utf-8') 
        writer.writeheader()
        for proj in project_info:
            try:
                name = proj['full_name'].replace('/', '_') # For easy querying in WoC
                commits = tuple(oscar.Project(str(name)))
                authors = set()
                for commit in commits:
                    if commit.author not in authors:
                        authors.add(commit.author)
                writer.writerow({
                    'name': name,
                    'url': proj['html_url'],
                    'description': proj['description'],
                    'size': proj['size'],
                    'stars': proj['stargazers_count'],
                    'watchers': proj['watchers_count'],
                    'language': proj['language'],
                    'forks': proj['forks'],
                    'commits': len(commits),
                    'authors': len(authors)
                })   
            except ValueError as e:
                print('ValueError: {} when reading {}'.format(e, proj['full_name']))
            counter += 1
            sys.stdout.write('\r')
            sys.stdout.write('Progress: {}/{}'.format(counter, len(project_info)))
            sys.stdout.flush()
        sys.stdout.write('\n')
