'''
NOTE: This is deprecated because we are not using data from WoC
A Custom Server over SSH Tunnel that can serve requests on WoC data
For request and response documentation, see (TODO)

Author: He, Hao
'''

import oscar.oscar as oscar
import json
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/project/<project_name>')
def project_metadata(project_name):
    p = oscar.Project(str(project_name))
    result = {'files': [], 'directories': []}
    for mode, filename, sha in p.head.tree.traverse():
        item = {'mode': mode, 'filename': filename, 'sha': sha}
        if mode == "40000":
            result['directories'].append(item)
        else:
            result['files'].append(item)
    return json.dumps(result)
    
    
@app.route('/file/<file_sha>')
def project_file(file_sha):
    result = {'content': ''}
    try:
        result['content'] = oscar.Blob(str(file_sha)).data
    except:
        print('Error Retrieving file/{}'.format(file_sha))
    return json.dumps(result)

