'''
Retrieve project names and urls from WoC, save in temp/ProjectInfo/
Note that this script will run for a long time and may halt for somewhile in the middle, so just be patient

Author: He, Hao
'''

import oscar.oscar as oscar
import json
import os


def initdir(dir):
    '''
    Check whether a directory is available for outputing data
    '''
    if os.path.isdir(dir):
        return True
    if os.path.exists(dir):
        print('{} already exists and is not a directory! Quiting...')
        quit()
    os.mkdir(dir)
    return True


if __name__ == '__main__':
    # Check folder availability
    initdir('temp')
    initdir('temp/ProjectInfo')

    data = []
    curr_chunk = 0
    chunk_size = 1000000
    for project in oscar.Project.all(): 
        data.append({
            'name': project.uri,
            'url': project.toURL()
        })  

        # Divide data into chunks since it is extremely large
        if len(data) >= chunk_size:
            with open('temp/ProjectInfo/ProjectList_Chunk{}.json'.format(curr_chunk), 'w') as f:
                f.write(json.dumps(data))
            print('Successfully retreived project list chunk {}'.format(curr_chunk))
            data = []
            curr_chunk += 1

    # Finish off the remaining data
    with open('temp/ProjectInfo/ProjectList_Chunk{}.json'.format(curr_chunk), 'w') as f:
        f.write(json.dumps(data))
    print('Successfully retreived project list chunk {}'.format(curr_chunk))

    print('Finished retreiving all projects!')

