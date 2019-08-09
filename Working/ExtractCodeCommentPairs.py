"""
Extract code comment pairs and all the related statistics using a Java program
"""

import os
import argparse
import subprocess
import pandas as pd
from termcolor import colored

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_path', help='Path to CSV file')
    csv_path = parser.parse_args().csv_path

    projects = pd.read_csv(csv_path)

    os.chdir('JavaAnalysis')
    subprocess.call('mvn package', shell=True)

    for index, row in projects.iterrows():
        print(colored('{}: Processing {}...'.format(index, row['name']), 'green'))
        subprocess.call('java -cp target/JavaAnalysis-1.0-SNAPSHOT.jar FunctionExtractor '
                        + '../../../projects/{} ../temp/comment_code_data/{}.json'
                        .format(row['name'], row['name']),
                        shell=True)
