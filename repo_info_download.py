'''
Download GitHub repository information sorted by stars in descending order

Created by He, Hao on 2019/04/03
'''

import requests
import json
import time


'''
Returns a json object that contains information of GitHub repos returned by GitHub REST v3 API

Example search url: https://api.github.com/search/repositories?q=language:java&sort=stars&order=desc
This URL collects GitHub Java project sorted by starts in descending order.
Remember that:
1. The results are returned in pages, so you have to fetch them page by page
2. You are limited to send only 10 requests per minute
3. You can only get up to 1000 search results

Reference Documentation: 
https://developer.github.com/v3/search/
https://help.github.com/en/articles/searching-for-repositories
'''
def get_repolist_by_stars(num=30, lang=''):
    url = 'https://api.github.com/search/repositories'
    params = {'q':'stars:>1000', 'sort':'stars', 'order':'desc', 'page':'1'}
    repolist = []

    if lang != '':
        params['q'] = 'language:' + lang

    print('Sending HTTP requests to GitHub, may need several minutes to complete...')

    for i in range(1, int(num / 30) + 2):
        params['page'] = str(i)
        json = requests.get(url, params).json()
        if json['items'] == None:
            print('Error: No result in page ' + str(i) + '!') 
            print('Message from GitHub: ' + str(json.get('message')))

        repolist.extend(json['items'])

        print('Downloaded repository information in page ' + str(i))
        time.sleep(7) # This rate is imposed by GitHub

    return repolist[0:num]


if __name__ == '__main__':
    languages = ['Java', 'C++', 'JavaScript', 'Python', 'Go']

    print('---------- Downloading Overall Repository Information ----------')
    repolist = get_repolist_by_stars(num=1000)

    # Count language freqencies
    language_freq = {}
    for repo in repolist:
        lang = repo['language']
        if lang == None: 
            continue
        if language_freq.get(lang) == None:
            language_freq[lang] = 1
        else:
            language_freq[lang] += 1

    print('Number of repositories: ' + str(len(repolist)))
    print('Language Distribution: ' + str(language_freq))

    with open('temp/repo_info.json', 'w') as file:
        json.dump(repolist, file)

    print('---------- Downloading Top Repository Information By Language ----------')
    repolist = []
    for lang in languages:
        print('Downloading repository by language ' + lang + '...')
        repolist.extend(get_repolist_by_stars(num=40, lang=lang))
    with open('temp/repo_info_selected.json', 'w') as file:
        json.dump(repolist, file)



    