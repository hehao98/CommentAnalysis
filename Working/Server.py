'''
A Custom Server over SSH Tunnel that can serve requests on WoC data
For request and response documentation, see (TODO)

Author: He, Hao
'''

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
    

