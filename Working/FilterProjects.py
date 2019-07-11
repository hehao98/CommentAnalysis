'''
Filter projects to identify recent and successful software projects using the following criteria
1. Have more than 500 commits
2. Have more than 100 commits in the past two years of activity
3. Language is in {Python, Java, JavaScript, C++, C, GO}
4. Available in GHTorrent Dataset(means it's on GitHub)

Note: It must be executed on da4 or it will go wrong for unknown reasons

Author: He, Hao
'''

import oscar.oscar as oscar
import os
import json
from multiprocessing import Pool
from datetime import datetime, timedelta, tzinfo
import sqlite3

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
        print('{} already exists and is not a directory! Quiting...'.format(dir))
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


def filter_project(projects, chunk_id):
    '''
    The main filter function
    '''
    filtered = []
    counter = 0
    conn = sqlite3.connect('temp/project.db')
    cursor = conn.cursor()
    for project in projects:
        counter += 1
        # Filter pass 1 using GHTorrent Data
        if 'github.com' not in project['url']: # ignore none github projects
            continue 
        # Using custom database built from GHTorrent, ignore forked projects, deleted projects, 
        # and projects that are not in some programming languages
        if 'github.com' in project['url']: 
            url_key = 'https://api.github.com/repos/{}'.format(project['name'].replace('_', '/'))
            cursor.execute('SELECT * FROM projects WHERE url=?', (url_key,))
            values = cursor.fetchall()
            if len(values) == 0: # Not existent in GHTorrent Database
                continue

        # Filter pass 2 using World of Code Data
        try: 
            commits = tuple(oscar.Project(str(project['name'])))
            num_commits_last_two_year = 0
            num_commits = len(commits)
            if num_commits < 500:
                continue
            for commit in commits:
                if commit.authored_at != None and datetime.now(tz=utc) - commit.authored_at <= timedelta(days=365*2):
                    num_commits_last_two_year += 1
            if num_commits_last_two_year <= 100:
                continue
            print('{}: {}, Commits: {}, Last-two-year Commits: {}'
                .format(counter, project['name'], num_commits, num_commits_last_two_year))
            filtered.append(project)
        except ValueError as e: 
            # This occurs because the project has no commits in it
            # probably because its source has been deleted
            print('In Project {}({}): ValueError, {}'.format(project['name'], project['url'], e))
    output_file = 'temp/FilteredProjects/ProjectList_chunk{}.json'.format(chunk_id)
    with open(output_file, 'w') as f:
        f.write(json.dumps(filtered))
    print('Written {} filtered projects to {}\n'.format(output_file))
    conn.close()


def run_proc(path, chunk_id):
    print('Processing projects from {}...'.format(path))
    projects = []
    with open(path, 'r') as f:
        projects = json.load(f)
    filter_project(projects, chunk_id)


if __name__ == '__main__':
    initdir('temp/FilteredProjects/')
    chunk_paths = get_chunks('temp/ProjectInfo')

    # Create a process pool
    begin_time = datetime.now()
    chunk_id = 0
    pool = Pool(12)
    for path in chunk_paths:
        pool.apply_async(run_proc, args=(path, chunk_id))
        chunk_id += 1
    pool.close()
    pool.join()
    print('All subprocess tasks finished!')

    print('Start joining files...')
    chunk_paths = get_chunks('temp/FilteredProjects/')
    filtered_projects = []
    for path in chunk_paths:
        with open(path, 'r') as f:
            print path
            filtered_projects.extend(json.load(f))
    with open('temp/FinalProjects.json', 'w') as f:
        f.write(json.dumps(filtered_projects))
    print('Total number of projects after filtering: {}'.format(len(filtered_projects)))
    print('Total running time: {}'.format(datetime.now() - begin_time))
