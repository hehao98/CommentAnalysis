import csv
import json
import argparse
import pandas as pd

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file')
    csv_file = parser.parse_args().csv_file

    projects = pd.read_csv(csv_file)

    with open('temp/Functions.csv', 'w') as output_csv:
        fieldnames = ['name', 'code', 'visibility', 'has_comment', 'line_comment', 'line_count',
                      'max_indent', 'is_abstract', 'is_static', 'is_native', 'is_synchronized', 'child_comment']
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()
        for index, row in projects.iterrows():
            print(index, row['name'])
            json_file = 'temp/comment_code_data/{}.json'.format(row['name'])
            try:
                with open(json_file, 'r') as f:
                   comment_data = json.load(f)
            except (FileNotFoundError, ValueError):
                continue
            for file in comment_data:
                method_info = comment_data[file]['methodInfo']
                for method in method_info:
                    if 'comment' not in method:
                        method['comment'] = ''
                    writer.writerow({
                        'visibility': method['visibility'],
                        'name': method['name'],
                        'has_comment': 'comment' in method and len(method['comment']) > 0,
                        'line_comment': method['comment'].count('\n'),
                        'line_count': method['lineCount'],
                        'max_indent': method['maxIndentation'],
                        'is_abstract': method['isAbstract'],
                        'is_static': method['isStatic'],
                        'is_native': method['isNative'],
                        'is_synchronized': method['isSynchronized'],
                        'child_comment': len(method['commentsInMethod'])
                    })
    print('Finished!')