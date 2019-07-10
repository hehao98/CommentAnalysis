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
from multiprocessing import Pool
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
    global project_saver
    filtered = []
    for project in projects:
        # TODO Filter pass 1 using GHTorrent Data

        # Filter pass 2 using World of Code Data
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
            filtered.append(project)
        except ValueError as e: 
            # This occurs because the project has no commits in it
            # probably because its source has been deleted
            print('In Project {}({}): ValueError, {}'.format(project['name'], project['url'], e))
    output_file = 'temp/FilteredProjects/ProjectList_chunk{}.json'.format(chunk_id)
    with open(output_file, 'w') as f:
        f.write(json.dumps(filtered))
    print('Written {} filtered projects to {}\n'.format(output_file))


def run_proc(path, chunk_id):
    print('Processing projects from {}...'.format(path))
    projects = []
    with open(path, 'r') as f:
        projects = json.load(f)[0:1000]
    filter_project(projects, chunk_id)


if __name__ == '__main__':
    initdir('temp/FilteredProjects/')
    chunk_paths = get_chunks('temp/ProjectInfo')

    # Create a process pool
    begin_time = datetime.now()
    chunk_id = 0
    pool = Pool(8)
    for path in chunk_paths:
        pool.apply_async(run_proc, args=(path, chunk_id))
        chunk_id += 1
    pool.close()
    pool.join()
    print('All subprocess tasks finished!')
    print('Total running time: {}'.format(datetime.now() - begin_time))
