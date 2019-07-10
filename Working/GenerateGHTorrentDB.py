'''
Generate a SQLite Database in temp/project.db storing all of the project metadata from GHTorrent dump csv file

Author: He, Hao
'''

import sqlite3

if __name__ == '__main__':
    path = raw_input('Please enter path to projects.csv of the GHTorrent dump(with filename): ')

    conn = sqlite3.connect('temp/project.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE projects (
            id int, url text, owner_id int, 
            name text, descriptor text, language text, 
            created_at text, forked_from int, deleted int, updated_at text
        );
    ''')

    with open(path, 'r') as csv:
        for i in range(1, 100):
            line = csv.readline()
            print(line)

    conn.commit()
    conn.close()
