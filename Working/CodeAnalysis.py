'''
Analyze source code and add various source code related metrics for a project

TODO: Finish this after the C++ parser is finished

Author: He, Hao
'''

import pandas as pd
import subprocess
import os
import json
import argparse
import hashlib
import sys
import resource
from termcolor import colored
import CodeParser


def get_file_list(path, suffix):
    '''
    Given a path, recursively retrieve and return all files with given suffix in the path
    '''
    result = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(suffix):
                result.append(os.path.join(root, file))
    return result


def chunk_reader(fobj, chunk_size=1024):
    '''
    Generator that reads a file in chunks of bytes
    '''
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk


def get_hash(filename, first_chunk_only=False, hash=hashlib.sha1):
    '''
    Compute hash for a given file path
    '''
    hashobj = hash()
    file_object = open(filename, 'rb')

    if first_chunk_only:
        hashobj.update(file_object.read(1024))
    else:
        for chunk in chunk_reader(file_object):
            hashobj.update(chunk)
    hashed = hashobj.digest()

    file_object.close()
    return hashed
    

def remove_duplicates(filelist):
    '''
    Given a list of file paths, return the list with duplicate files removed
    '''
    hashes_by_size = {}
    hashes_on_1k = {}
    hashes_full = {}
    result = []

    for path in filelist:
        try:
            # if the target is a symlink (soft one), this will 
            # dereference it - change the value to the actual target file
            path = os.path.realpath(path)
            file_size = os.path.getsize(path)
        except (OSError,):
            # not accessible (permissions, etc) - pass on
            continue
        duplicate = hashes_by_size.get(file_size)
        if duplicate:
            hashes_by_size[file_size].append(path)
        else:
            hashes_by_size[file_size] = []  # create the list for this file size
            hashes_by_size[file_size].append(path)

    # For all files with the same file size, 
    # get their hash on the 1st 1024 bytes
    for __, files in hashes_by_size.items():
        if len(files) < 2:
            result.extend(files)
            continue    # this file size is unique

        for filename in files:
            try:
                small_hash = get_hash(filename, first_chunk_only=True)
            except (OSError,):
                continue

            duplicate = hashes_on_1k.get(small_hash)
            if duplicate:
                hashes_on_1k[small_hash].append(filename)
            else:
                hashes_on_1k[small_hash] = []          # create the list for this 1k hash
                hashes_on_1k[small_hash].append(filename)

    # For all files with the hash on the 1st 1024 bytes, 
    # get their hash on the full file - collisions will be duplicates
    for __, files in hashes_on_1k.items():
        if len(files) < 2:
            result.extend(files)
            continue    # this hash of fist 1k file bytes is unique, no need to spend cpu cycles on it

        for filename in files:
            try: 
                full_hash = get_hash(filename, first_chunk_only=False)
            except (OSError,):
                # the file access might've changed till the exec point got here 
                continue

            duplicate = hashes_full.get(full_hash)
            if duplicate:
                print("Duplicate found: {} and {}".format(filename, duplicate))
            else:
                hashes_full[full_hash] = filename
                result.append(filename)

    return result


def get_file_stats(filepath, lang):
    '''
    Given a source code file and its programming language, return comment analysis result 
    '''
    stat = {'functions': 0, 'doc_comment': 0, 'impl_comment': 0}
    trees = CodeParser.get_json_syntax_tree(filepath)
    for tree in trees:
        stat['functions'] += CodeParser.count_functions(tree)
        comment_count = CodeParser.count_comments(tree, trees, lang)
        stat['doc_comment'] += comment_count['doc_comment']
        stat['impl_comment'] += comment_count['impl_comment']
    return stat


if __name__ == '__main__':
    # Set the recursion limit from 1000 to 10000 to avoid RecursionError
    # because when parsing AST, the tree might have very high depth
    sys.setrecursionlimit(10000)
    resource.setrlimit(resource.RLIMIT_STACK, (2**28, -1))

    # Parse Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'csv_path', help='Path to the CSV file storing project information')
    parser.add_argument('proj_path', help='Path where the projects are stored')
    parser.add_argument('-j', type=int, default=8,
                        help='Number of Jobs (Default 8)')
    args = vars(parser.parse_args())
    csv_path = args['csv_path']
    proj_path = args['proj_path']
    num_jobs = args['j']

    projects = pd.read_csv(csv_path)

    # Initialize metrics if not present
    # TODO Add more metrics to them
    #metrics = ['src_files', 'header_comment', 'functions', 'func_with_doc', 'doc_comment', 'impl_comment']
    metrics = ['src_files', 'functions', 'doc_comment', 'impl_comment']
    for metric in metrics:
        if metric not in projects:
            projects[metric] = -1

    for index, row in projects.iterrows():
        # Skipping analyzed projects if all the related fields is set
        should_skip = True
        for metric in metrics:
            if row[metric] == -1:
                should_skip = False
        if should_skip:
            continue

        print(colored('Processing {}...'.format(row['name']), 'green'))

        path = os.path.join(proj_path, row['name'])
        suffix_mapping = {'Java': '.java',
                          'JavaScript': '.js', 'Python': '.py'}
        suffix = suffix_mapping[row['language']]
        file_list = get_file_list(path, suffix)
        read_count = len(file_list)

        file_list = remove_duplicates(file_list)

        print('Read {} source files in which {} files are unique...'.format(
            read_count, len(file_list)))

        projects.at[index, 'src_files'] = len(file_list)
        projects.at[index, 'functions'] = 0
        projects.at[index, 'doc_comment'] = 0
        projects.at[index, 'impl_comment'] = 0
        for file in file_list:
            stat = get_file_stats(file, row['language'])
            # TODO Copy the stats into csv
            projects.at[index, 'functions'] += stat['functions']
            projects.at[index, 'doc_comment'] += stat['doc_comment']
            projects.at[index, 'impl_comment'] += stat['impl_comment']

        print(projects.loc[index])
        projects.to_csv(csv_path, index=False)

    
