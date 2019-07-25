'''
Some utility functions for parsing and analyzing comments
Uses the semantic library: https://github.com/github/semantic/
'''

import subprocess
import json
import collections
from termcolor import colored


def get_json_syntax_tree(file):
    try:
        result = subprocess.check_output('semantic parse {} --json'.format(file), shell=True)
    except subprocess.CalledProcessError as e:
        print(colored('ERROR when parsing {}: \n{}'.format(file, e.output), 'red'))
    return json.loads(result, object_pairs_hook=collections.OrderedDict)['trees']


def print_tree(node, depth=0):
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

if __name__ == '__main__':
    # Some simple unit tests
    trees = get_json_syntax_tree('Parser/test/sample.py')
    print(json.dumps(trees))
    for tree in trees:
        print_tree(tree)
    print('Number of Functions: ', count_functions(tree))