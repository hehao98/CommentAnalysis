'''
Given comment data in temp/comment_data/, analyze and produce comment feature in temp/comment_feature/
The statistics are
1. Bag of words

Author: He, Hao
'''

import os
import re
import json
import argparse
import multiprocessing
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def extract_words(comment):
    '''
    Given a comment string, split it into a list of words using a number of heuristic rules
    '''
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
    return [w for w in words if len(w) >= 3 and w not in set(stopwords.words('english'))]


def process_worker(index, row):
    '''
    Work to be done by each process
    '''
    comment_data = []
    bag_of_words = {}
    with open('temp/comment_data/{}.json'.format(row['name']), 'r') as f:
        comment_data = json.load(f)
    for file_name in comment_data:
        comments = comment_data[file_name]['comments']
        for comment in comments:
            words = extract_words(comment['content'])
            for w in words:
                if w in bag_of_words:
                    bag_of_words[w] += 1
                else:
                    bag_of_words[w] = 1
    with open('temp/comment_feature/{}.json'.format(row['name']), 'w') as f:
        f.write(json.dumps({
            'bag_of_words': bag_of_words
        }))
    print('{}: Finished {}'.format(index, row['name']))


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

    pool = multiprocessing.Pool(num_jobs)
    for index, row in projects.iterrows():
        pool.apply_async(process_worker, args=(index, row))
    pool.close()
    pool.join()

    print('Finished!')
