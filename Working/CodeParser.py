'''
Some utility functions for parsing and analyzing comments
Uses the semantic library: https://github.com/github/semantic/
'''

import subprocess
import json
import collections
import argparse
import sys
from termcolor import colored


def get_json_syntax_tree(file):
    '''
    Given a source code file path, return its syntax tree as a list of OrderedDict
    '''
    result = '{"trees": {}}'
    try:
        print(file.replace(' ', '\ '))
        result = subprocess.check_output(
            "semantic parse {} --json".format(file.replace(' ', '\ ')), shell=True)
    except subprocess.CalledProcessError as e:
        print(colored('ERROR when parsing {}: \n{}'.format(file, e.output), 'red'))
    obj = {'trees': {}}
    try:
        obj = json.loads(result, object_pairs_hook=collections.OrderedDict)
    except RecursionError:
        print(colored('RecursionError occured at {}!'.format(file), 'red'))
    return obj['trees']


def print_tree(node, depth=0):
    '''
    Print the syntax tree acquired above in a simple format to the console
    '''
    prefix = depth * ' '
    if 'term' in node:
        print(prefix + node['term'])
    for attribute, value in node.items():
        # Find child nodes using the following rules
        if isinstance(value, dict):
            print_tree(value, depth + 1)
        if isinstance(value, list):
            for obj in value:
                if isinstance(obj, dict):
                    print_tree(obj, depth + 1)
    return


def count_functions(node, depth=0):
    '''
    Count and return number of functions in a syntax tree
    '''
    result = 0
    if 'term' in node and node['term'] in ['Function', 'Method']:
        result += 1
    for attribute, value in node.items():
        # Find child nodes using the following rules
        if isinstance(value, dict):
            result += count_functions(value, depth + 1)
        if isinstance(value, list):
            for obj in value:
                if isinstance(obj, dict):
                    result += count_functions(obj, depth + 1)
    return result


def count_comments(node, parent, lang, depth=0):
    '''
    Count and return number of comments in the syntax tree, including:
    1. the number of documentation comments
    2. the number of implementation comments
    '''
    result = {
        'doc_comment': 0,
        'impl_comment': 0,
    }

    # Inspect this node
    if lang == 'Java' or lang == 'JavaScript':
        if 'term' in node and node['term'] == 'Comment':
            if node['commentContent'].startswith('/**'):
                result['doc_comment'] += 1
            else:
                result['impl_comment'] += 1
    elif lang == 'Python':
        if 'term' in node and node['term'] == 'TextElement':
            if node['textElementContent'].startswith('"""') or node['textElementContent'].startswith("'''"):
                result['doc_comment'] += 1
        if 'term' in node and node['term'] == 'Comment':
            result['impl_comment'] += 1

    # Recursively iterate the remaining nodes
    for attribute, value in node.items():
        # Find child nodes using some heuristic rules
        if isinstance(value, dict):
            temp = count_comments(value, node, lang, depth + 1)
            for key in temp.keys():
                result[key] += temp[key]
        if isinstance(value, list):
            for obj in value:
                if isinstance(obj, dict):
                    temp = count_comments(obj, node, lang, depth + 1)
                    for key in temp.keys():
                        result[key] += temp[key]
    return result


def extract_comments(node, depth=0):
    '''
    Given a syntax tree, extract all comments from it and return them as an array
    '''


if __name__ == '__main__':
    # Some simple unit tests
    argparser = argparse.ArgumentParser()
    argparser.add_argument('src')
    src = vars(argparser.parse_args())['src']
    lang = ''
    if src.endswith('.js'):
        lang = 'JavaScript'
    elif src.endswith('.py'):
        lang = 'Python'
    elif src.endswith('.java'):
        lang = 'Java'

    trees = get_json_syntax_tree(src)
    print(json.dumps(trees))
    for tree in trees:
        print_tree(tree)
    print('Number of Functions: ', count_functions(tree))
    print('Number of Comments: ', count_comments(tree, trees, lang))

