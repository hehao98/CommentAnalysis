'''
Generate a SQLite Database in temp/project.db storing all of the project metadata from GHTorrent dump csv file

Author: He, Hao
'''

import sqlite3
import csv

if __name__ == '__main__':
    path = raw_input('Please enter path to projects.csv of the GHTorrent dump(with filename): ')

    conn = sqlite3.connect('temp/project.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE projects (
            id integer, url text PRIMARY KEY, owner_id integer, 
            name text, language text, 
            created_at text, forked_from text, deleted integer, updated_at text
        );
    ''')

    with open(path, 'rU') as csv_file:
        reader = csv.reader(csv_file)
        num_read = 0
        num_write = 0
        for row in reader:
            num_read += 1
            # Sanity checks for the row, filter out forked and deleted projects
            if len(row) < 10:
                continue
            if row[2] == -1: # no owner, indicates empty project
                continue
            if row[7] != '\N': # forked_from field
                continue
            if row[8] == '1': # deleted field
                continue
            if row[5] not in ('Java', 'JavaScript', 'Python', 'C', 'C++', 'Go'): # filter out language
                continue
            try:
                cursor.execute('''
                    INSERT INTO projects 
                    (id, url, owner_id, name, language, created_at, forked_from, deleted, updated_at) 
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (int(row[0]), str(row[1]), int(row[2]), str(row[3]), str(row[5]), str(row[6]), str(row[7]), int(row[8]), str(row[9])))
            except sqlite3.IntegrityError:
                print('ERROR: ID already exists in PRIMARY KEY column {}'.format(row[1]))
            num_write += 1
        print('Read {} entries from CSV in which {} entries are written to database'.format(num_read, num_write))

    conn.commit()
    conn.close()
