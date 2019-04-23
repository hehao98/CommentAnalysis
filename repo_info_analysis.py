'''
Print and plot analysis results for downloaded GitHub repository information
Also, output a CSV file for repository statistics
Assume the information is in 'temp/repo_info.json', run repo_info_download.py first to download that

Created By He, Hao on 2019/04/03
'''

import json
import matplotlib.pyplot as plt
import numpy as np
import csv


def plot_lang_freq(repo_info):
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


def to_csv(repo_info, output_path):
    fieldnames = ['full_name', 'language', 'commits', 'stars', 'forks',
                  'contributors', 'open_issues', 'lines_of_code', 'lines_of_comment']

    # Output interesting repository metrics to CSV
    with open('temp/repo_info.csv') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in repo_info:
            writer.writerow({
                'full_name': item['full_name'],
                'language': item['language'],
                'commits': item['commit_count'],
                'stars': item['stargazers_count'],
                'forks': item['forks'],
                'contributors': item['contributor_count'],
                'open_issues': item['open_issues_count'],
                'src_files': 0,
                'lines_of_code': 0,
                'lines_of_comment': 0,
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

    to_csv(repo_info, 'temp/repo_info.csv')
    to_csv(repo_info_selected, 'temp/repo_info_selected.csv')
