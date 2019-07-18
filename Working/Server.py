'''
A Custom Server over SSH Tunnel that can serve requests on WoC data
For request and response documentation, see (TODO)

Author: He, Hao
'''

import oscar.ocsar as oscar
import json
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/project/<project_name>')
def project_metadata(project_name):
    p = oscar.Project(project_name)
    result = {'files': []}
    for mode, filename, sha in p.head.tree.traverse():
        if mode != 40000:
            result['files'].append({
                'mode': mode,
                'filename': filename,
                'sha': sha
            })
    return json.dumps(result)
    
    
@app.route('/file/<file_sha>')
def project_file(file_sha):
    return oscar.Blob(sha).data

