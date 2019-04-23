'''
Download GitHub repository information sorted by stars in descending order

Created by He, Hao on 2019/04/03
'''

import requests
import json
import time


def get_repolist_by_stars(num=30, lang=''):
    '''
    Returns a json object that contains information of GitHub repos returned by GitHub REST v3 API

    Example search url: https://api.github.com/search/repositories?q=language:java&sort=stars&order=desc
    This URL collects GitHub Java project sorted by stars in descending order.
    Remember that:
    1. The results are returned in pages, so you have to fetch them page by page
    2. You are limited to send only 10 requests per minute
    3. You can only get up to 1000 search results

    Reference Documentation: 
    https://developer.github.com/v3/search/
    https://help.github.com/en/articles/searching-for-repositories
    '''
    url = 'https://api.github.com/search/repositories'
    params = {'q': 'stars:>1000', 'sort': 'stars',
              'order': 'desc', 'page': '1'}
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
        time.sleep(7)  # This rate is imposed by GitHub

    return repolist[0:num]


def add_commit_and_contributor_info(repolist):
    '''
    Add 'commit_count' and 'contributor_count' field to each repo object
    the data is collected using other GitHub APIs
    '''

    print('Downloading commit information from GitHub...')
    for repo in repolist:
        url = 'https://api.github.com/repos/' + repo['full_name'] + '/commits'
        response = requests.get(url)
        # Example link: https://api.github.com/resource?page=5
        last_link = response.links['last']['url']
        first_page = response.json()
        last_page_num = int(last_link.split('=')[1])
        last_page_item_count = len(requests.get(
            url, params={'page': last_page_num}).json())
        repo['commit_count'] = (
            last_page_num - 1) * len(first_page) + last_page_item_count
        print(repo['full_name'] + ': ' +
              str(repo['commit_count']) + ' commits')
        # This rate is imposed by GitHub, and we send 2 requests each iteration
        time.sleep(14)

    # Why duplicate code like this?
    print('Downloading contributor information from GitHub...')
    for repo in repolist:
        url = 'https://api.github.com/repos/' + \
            repo['full_name'] + '/contributors'
        response = requests.get(url)
        last_link = response.links()['last']['url']
        first_page = response.json()
        last_page_num = int(last_link.split('=')[1])
        last_page_item_count = len(requests.get(
            url, params={'page': last_page_num}).json())
        repo['contributor_count'] = (
            last_page_num - 1) * len(first_page) + last_page_item_count
        print(repo['full_name'] + ': ' +
              str(repo['contributor_count']) + ' contributors')
        # This rate is imposed by GitHub, and we send 2 requests each iteration
        time.sleep(14)


def download_overall_info():
    '''
    Download information of 1000 most starred information
    '''
    print('---------- Downloading Overall Repository Information ----------')
    repolist = get_repolist_by_stars(num=1000)

    # Get number of commits and number of contributors of this repository,
    # which is not included in the response by default
    add_commit_and_contributor_info(repolist)

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


def download_by_language():
    '''
    Download reposiory information by language
    '''
    languages = ['Java', 'C++', 'JavaScript', 'Python', 'Go']

    print('---------- Downloading Top Repository Information By Language ----------')
    repolist = []
    for lang in languages:
        print('Downloading repository in language ' + lang + '...')
        repolist.extend(get_repolist_by_stars(num=20, lang=lang))
    add_commit_and_contributor_info(repolist)
    with open('temp/repo_info_selected.json', 'w') as file:
        json.dump(repolist, file)


if __name__ == '__main__':
    download_overall_info()
    download_by_language()
