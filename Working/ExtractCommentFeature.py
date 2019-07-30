'''
Given comment data in temp/comment_data/, analyze and produce comment feature in temp/comment_feature/
The statistics are
1. Number of words
2. Bag of words
3. Word frequency and inverse document frequency

NOTE: Delete temp/comment_data/ folder if you want to rerun this script again

Author: He, Hao
'''

import os
import re
import json
import math
import argparse
import multiprocessing
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from termcolor import colored

stop_words = set(stopwords.words('english'))


def extract_words(comment):
    '''
    Given a comment string, split it into a list of words using a number of heuristic rules
    '''
    global stop_words
    # split by non-word characters (excluding digit)
    words = re.split(r'[\W_]+', comment)
    new_words = []
    for w in words:
        # Split these words if there is camel case
        matches = re.finditer(
            '.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', w)
        splitted_words = [m.group(0) for m in matches]
        for w2 in splitted_words:
            new_words.append(w2)
    # Change into lower case letters and lemmatize
    wnl = WordNetLemmatizer()
    words = nltk.pos_tag([w.lower() for w in new_words])
    words = [wnl.lemmatize(i, j[0].lower()) if j[0].lower() in [
        'a', 'n', 'v'] else wnl.lemmatize(i) for i, j in words]
    # Remove stopwords and short words
    return [w for w in words if len(w) >= 3 and w not in stop_words]


def process_worker(index, row):
    '''
    Work to be done by each process
    '''
    comment_data = []
    bag_of_words = {}

    # Empirically skip generated data if it already exists
    if os.path.exists('temp/comment_feature/{}.json'.format(row['name'])):
        return

    with open('temp/comment_data/{}.json'.format(row['name']), 'r') as f:
        comment_data = json.load(f)

    for file_name in comment_data:
        comments = comment_data[file_name]['comments']
        for comment in comments:
            # Exclude comments that appears to be a license header
            if any(x in comment['content'] for x in ['license', 'copyright', 'warranty']):
                continue
            words = extract_words(comment['content'])
            for w in words:
                if w in bag_of_words:
                    bag_of_words[w]['count'] += 1
                else:
                    bag_of_words[w] = {'count': 1}

    total_words = sum([x['count'] for x in bag_of_words.values()])
    for word in bag_of_words:
        bag_of_words[word]['freq'] = bag_of_words[word]['count'] / total_words

    with open('temp/comment_feature/{}.json'.format(row['name']), 'w') as f:
        f.write(json.dumps({
            'total_words': total_words,
            'bag_of_words': bag_of_words
        }))

    print('{}: Finished {}'.format(index, row['name']))


def postprocess(projects):
    '''
    Post process comment data, add IDF and TF-IDF to each bag of word
    '''
    document_count = len(projects['name'])
    word_count_dict = {}  # For each word, count how many projects contain this word

    # First round, generate word existence data
    for index, row in projects.iterrows():
        comment_data = {}
        with open('temp/comment_feature/{}.json'.format(row['name']), 'r') as f:
            comment_data = json.load(f)
        for word in comment_data['bag_of_words']:
            if word in word_count_dict:
                word_count_dict[word] += 1
            else:
                word_count_dict[word] = 1

    # Second round, compute IDF and TF-IDF
    for index, row in projects.iterrows():
        comment_data = {}
        with open('temp/comment_feature/{}.json'.format(row['name'], 'r')) as f:
            comment_data = json.load(f)
        for word in comment_data['bag_of_words']:
            comment_data['bag_of_words'][word]['idf'] = math.log(
                document_count / word_count_dict[word])
            comment_data['bag_of_words'][word]['tfidf'] = comment_data['bag_of_words'][word]['freq'] * \
                comment_data['bag_of_words'][word]['idf']
        with open('temp/comment_feature/{}.json'.format(row['name'], 'w')) as f:
            f.write(json.dumps(comment_data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file', help="Path to the project CSV file")
    parser.add_argument('-j', type=int, default=8,
                        help='Number of Jobs (Default 8)')
    args = parser.parse_args()
    csv_file = args.csv_file
    num_jobs = args.j

    os.makedirs('temp/comment_feature/', exist_ok=True)

    projects = pd.read_csv(csv_file)

    print(colored('Processing comment data...', 'green'))

    pool = multiprocessing.Pool(num_jobs)
    results = []
    for index, row in projects.iterrows():
        results.append(pool.apply_async(process_worker, args=(index, row)))
        #process_worker(index, row)
    pool.close()
    for r in results:
        r.get() # If any exception occurred in child process, print them
    pool.join()

    print(colored('Adding additional data...', 'green'))

    postprocess(projects)

    print('Finished!')
