'''
Download projects from a project csv file and put them in ../../projects

Author: He, Hao
'''

import pandas as pd
import subprocess
import os
import argparse
from datetime import datetime
from multiprocessing import Pool
from termcolor import colored

def run_proc(index, url, name):
    print(colored('Downloading Project {}...'.format(index), 'green'))
    subprocess.call('git clone --depth=1 {}.git {}'.format(url, name), shell=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_path', help='Path to the CSV file storing project information')
    csv_path = parser.parse_args().csv_path

    begin_time = datetime.now()

    projects = pd.read_csv(csv_path)
    os.chdir('../../')
    if not os.path.exists('projects/'):
        os.mkdir('projects')
    os.chdir('projects')
    
    pool = Pool(12)
    for index, row in projects.iterrows(): 
        pool.apply_async(run_proc, args=(index, row['url'], row['name']))
    pool.close()
    pool.join()
    print('Total running time: {}'.format(datetime.now() - begin_time))
        