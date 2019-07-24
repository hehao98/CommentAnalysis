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
from termcolor import colored


if __name__ == '__main__':
    # Parse Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'csv_path', help='Path to the CSV file storing project information')
    parser.add_argument('-j', type=int, default=8,
                        help='Number of Jobs (Default 8)')
    args = vars(parser.parse_args())
    csv_path = args['csv_path']
    num_job = args['j']

    projects = pd.read_csv(csv_path)
    for index, row in projects.iterrows():
        pass

    