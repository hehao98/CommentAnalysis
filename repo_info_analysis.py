'''
Print and plot analysis results for downloaded GitHub repository information
Plots will be in /temp/plots folder
Assume the information is in 'temp/repo_info.json', run repo_info_download.py first to download that

Created By He, Hao on 2019/04/03
'''

import json
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    repo_info = []
    with open('temp/repo_info.json', 'r') as f:
        repo_info = json.load(f)

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

    repo_info_selected = []
    with open('temp/repo_info_selected.json', 'r') as f:
        repo_info_selected = json.load(f)
