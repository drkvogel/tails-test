from flask import Flask, render_template
from flask.json import jsonify
import os
import sys
import json
from pprint import pprint

app = Flask(__name__)

# app.config['DATA_DIR'] = '.'

# cache = {}

stores = {}

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/test")
def test():
    get_config()
    return "stuff"

@app.route("/stores")
def list_stores():
    get_config()
    # print('/stores', file=sys.stderr)
    # pprint(stores) # prints sorted version of stores??
    rows = ''
    for name in sorted(stores):
        rows = rows + "<tr><td>%s</td><td>%s</td></tr>\n" % (name.replace('_', ' '), stores[name])
    return render_template('stores.html', stores=stores, rows=rows)

def get_config():
    global stores # !!
    with open('stores.json') as json_file:
        rows = json.load(json_file) # dict of dicts
        for row in rows:
            stores[row['name']] = row['postcode']   # new dict

if __name__ == '__main__':
    get_config()
    app.run(debug=True)
