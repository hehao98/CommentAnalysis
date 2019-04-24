'''
Print and plot analysis results for downloaded GitHub repository information
Also, output temp/repo_info.csv and temp/repo_info_selected.csv for repository statistics
Assume the information is in 'temp/repo_info.json', run repo_info_download.py first to download that
Uses CLOC(https://github.com/AlDanial/cloc) to count lines of code and comments

Created By He, Hao on 2019/04/03
'''

import json
import matplotlib.pyplot as plt
import numpy as np
import csv
import subprocess


def plot_lang_freq(repo_info):
    '''
    Plot language frequencies for repository informaton in repo_info
    '''
    # Count language freqencies
    language_freq = {}
    for repo in repo_info:
        lang = repo['language']
        if lang == None:
            continue
        if language_freq.get(lang) == None:
            language_freq[lang] = 1
        else:
            language_freq[lang] += 1

    print('Number of repositories: ' + str(len(repo_info)))
    print('Language Distribution: ' + str(language_freq))

    # Plot lanugage frequency
    sorted_lang_freq = sorted(language_freq.items(),
                              key=lambda x: x[1])
    sorted_lang_freq.reverse()
    xaxis = []
    yaxis = []
    for lang, freq in sorted_lang_freq[0:20]:
        xaxis.append(lang)
        yaxis.append(freq)
    plt.barh(xaxis, yaxis)
    plt.title('Top 20 Languages among 1000 Most Starred GitHub Repositories')
    plt.xlabel('# of Repositories')
    plt.show()
    return


def plot_repo_size_dist(repo_info):
    '''
    Plot distribution of repository size
    '''
    xaxis = []
    yaxis = []
    for item in repo_info:
        xaxis.append(item['size'] / 1024)
    xaxis = sorted(xaxis)
    for i in range(0, len(xaxis)):
        yaxis.append((i + 1) / len(xaxis))
    plt.plot(xaxis, yaxis)
    plt.xlabel('Repository Size(MB)')
    plt.title('CDF of Repository Size')
    plt.ylim(0, 1)
    plt.xlim(0)
    plt.show()
    return


def count_src_files(repo):
    '''
    Given repository info, count number of src files, blank lines, code lines and comment lines
    Use open source tool cloc(https://github.com/AlDanial/cloc)
    Assume the repositories have been downloaded in '../projects/' by download2.py
    '''
    src_files = 0
    lines_blank = 0
    lines_code = 0
    lines_comment = 0

    print('Counting source files in ' + repo['full_name'])

    project_path = '../projects/%s/%s' % (repo['language'], repo['name'])
    subprocess.call('cloc %s --csv -out=temp/temp.txt' %
                    (project_path), shell=True)

    with open('temp/temp.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['language'] != repo['language']:
                continue
            src_files = row['files']
            lines_blank = row['blank']
            lines_code = row['code']
            lines_comment = row['comment']

    return src_files, lines_blank, lines_code, lines_comment


def gen_statistics(repo_info, output_file):
    '''
    Generate statistics for each repository in repo_info[] and write result as csv to output_file
    '''
    fieldnames = ['full_name', 'language', 'commits', 'stars', 'forks',
                  'contributors', 'open_issues', 'src_files', 'lines_code',
                  'lines_blank', 'lines_comment', 'comment_ratio']

    # Output interesting repository metrics to CSV
    with open(output_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in repo_info:
            src_files, lines_blank, lines_code, lines_comment = count_src_files(
                item)
            comment_ratio = 0
            if int(lines_code) != 0:
                comment_ratio = int(lines_comment) / int(lines_code)
            writer.writerow({
                'full_name': item['full_name'],
                'language': item['language'],
                'commits': item['commit_count'],
                'stars': item['stargazers_count'],
                'forks': item['forks'],
                'contributors': item['contributor_count'],
                'open_issues': item['open_issues_count'],
                'src_files': src_files,
                'lines_blank': lines_blank,
                'lines_code': lines_code,
                'lines_comment': lines_comment,
                'comment_ratio': comment_ratio,
            })
 

    return


if __name__ == '__main__':
    repo_info = []
    with open('temp/repo_info.json', 'r') as f:
        repo_info = json.load(f)
    repo_info_selected = []
    with open('temp/repo_info_selected.json', 'r') as f:
        repo_info_selected = json.load(f)

    # plot_lang_freq(repo_info)
    # plot_repo_size_dist(repo_info_selected)

    # gen_statistics(repo_info, 'temp/repo_info.csv')
    gen_statistics(repo_info_selected, 'temp/repo_info_selected.csv')
