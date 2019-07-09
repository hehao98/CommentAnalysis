'''
Filter projects to identify recent and successful software projects using the following criteria
1. Have more than 500 commits
2. Have more than 100 commits in the past two years of activity
3. Have more than 5 authors in commit info

Author: He, Hao
'''

import oscar.oscar as oscar
import os
import json
from datetime import datetime, timedelta, tzinfo


ZERO = timedelta(0)

class UTC(tzinfo):
  def utcoffset(self, dt):
    return ZERO
  def tzname(self, dt):
    return "UTC"
  def dst(self, dt):
    return ZERO

utc = UTC()


def initdir(dir):
    '''
    Check whether a directory is available for outputing data
    '''
    if os.path.isdir(dir):
        return True
    if os.path.exists(dir):
        print('{} already exists and is not a directory! Quiting...')
        quit()
    os.mkdir(dir)
    return True


def get_chunks(path):
    '''
    Return a string of filenames that are chunks storing projects
    '''
    result = []
    for f in os.listdir(path):
        chunk_path = os.path.join(path, f)
        if os.path.isfile(chunk_path):
            result.append(chunk_path)
    return result


class ProjectSaver(object):
    def __init__(self):
        self.chunk_size = 1000000
        self.curr_chunk = 0
        self.curr_json = [] 
        self.counter = 0

       
    def save(self, projects):
        for project in projects:
            self.curr_json.append(project)
            self.counter += 1
            if len(self.curr_json) == self.chunk_size:
                with open('temp/FilteredProjects/ProjectList_chunk{}.json'.format(self.curr_chunk), 'w') as f:
                    f.write(json.dumps(self.curr_json))
                self.curr_json = []
                self.curr_chunk += 1
                    
    def finish(self):
        with open('temp/FilteredProjects/ProjectList_chunk{}.json'.format(self.curr_chunk), 'w') as f:
            f.write(json.dumps(self.curr_json))
        self.curr_json = []
        self.curr_chunk += 1


project_saver = ProjectSaver()

def filter_project(projects):
    global project_saver
    result = []
    for project in projects:
        try: 
            commits = tuple(oscar.Project(str(project['name'])))
            authors = set()
            num_commits_last_two_year = 0
            if len(commits) < 500:
                continue
            for commit in commits:
                if commit.author not in authors:
                    authors.add(commit.author)
                if commit.authored_at != None and datetime.now(tz=utc) - commit.authored_at <= timedelta(days=365*2):
                    num_commits_last_two_year += 1
            if len(authors) < 5:
                continue
            if num_commits_last_two_year <= 100:
                continue
            print('{}, Commits: {}, Authors: {}, Last-two-year Commits: {}'
                .format(project['name'], len(commits), len(authors), num_commits_last_two_year))
            result.append(project)
        except ValueError as e: 
            # This occurs because the project has no commits in it
            # probably because its source has been deleted
            print('In Project {}({}): ValueError, {}'.format(project['name'], project['url'], e))
    project_saver.save(result)


if __name__ == '__main__':
    initdir('temp/FilteredProjects/')
    chunk_paths = get_chunks('temp/ProjectInfo')

    for path in chunk_paths:
        print('Processing projects from {}...'.format(path))
        projects = []
        with open(path, 'r') as f:
            projects = json.load(f)    
        filtered = filter_project(projects)
        save_projects(filtered)
    
    project_saver.finish()
    print('{} projects in total'.format(project_saver.counter))

        
                
            