'''
Download projects in result/Projects.csv and put them in ../../projects
'''

import pandas as pd
import subprocess
import os
from datetime import datetime
from multiprocessing import Pool

def run_proc(url, name):
    subprocess.call('git clone --depth=1 {}.git {}'.format(url, name), shell=True)

if __name__ == '__main__':
    begin_time = datetime.now()

    projects = pd.read_csv('result/Projects.csv')
    os.chdir('../../')
    if not os.path.exists('projects/'):
        os.mkdir('projects')
    os.chdir('projects')
    
    pool = Pool(12)
    for index, row in projects.iterrows():
        pool.apply_async(run_proc, args=(row['url'], row['name']))
    pool.close()
    pool.join()
    print('Total running time: {}'.format(datetime.now() - begin_time))
        