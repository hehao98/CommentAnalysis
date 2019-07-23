'''
Read project info from result/Projects.csv, do the following
1. Remove duplicates
2. Initialize metrics
3. Print summary
4. Save to result/Projects.csv
5. Random Sample 500 projects and save to temp/ProjectSample.csv
'''

import pandas as pd


if __name__  == '__main__':
    projects = pd.read_csv('result/Projects.csv')

    projects = projects.drop_duplicates('url')

    metric_list = [
        'lines_of_code',
        'lines_of_comments',
        'lines_blank',
        'impl_comment',
        'doc_comment',
        'src_files',
        'file_header_comment',
    ]

    for metric in metric_list:
        if metric not in projects:
            projects[metric] = -1
    
    print(projects.describe)

    projects.to_csv('result/Projects.csv', index=False)

    projects = projects[projects['language'].isin(['Java', 'JavaScript', 'Python'])]

    projects.sample(n=500).to_csv('temp/ProjectSample.csv', index=False)