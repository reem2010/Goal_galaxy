#!/usr/bin/python3
"""the app file"""
from flask import Flask, jsonify, make_response
from data import storage
import os

app = Flask(__name__)



@app.teardown_appcontext
def teardown(var):
    storage.close()



if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    app.run(host=host, port=port, threaded=True)