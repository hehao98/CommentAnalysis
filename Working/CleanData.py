'''
Read project info from result/Projects.csv, do the following
1. Remove duplicates
2. Initialize metrics
3. Print summary
4. Save to Projects2.csv
5. Random Sample 500 projects and save to temp/ProjectSample.csv
'''

import pandas as pd


if __name__  == '__main__':
    projects = pd.read_csv('result/Projects.csv')

    projects = projects.drop_duplicates('url')

    for index, row in projects.iterrows():
        projects.at[index, 'lines_of_code'] = -1
        projects.at[index, 'lines_of_comments'] = -1
        projects.at[index, 'lines_blank'] = -1
    
    print(projects.describe)

    projects.to_csv('result/Projects.csv', index=False)

    projects = projects[projects['language'].isin(['Java', 'JavaScript', 'Python'])]

    projects.sample(n=500).to_csv('temp/ProjectSample.csv', index=False)