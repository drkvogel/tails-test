from flask import Flask, render_template
from flask.json import jsonify
import os
import sys
import json

app = Flask(__name__)

# app.config['DATA_DIR'] = '.'

cache = {}

json_data = None

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/test")
def test():
    # return render_template('index.html')
    get_config()
    print('test2', file=sys.stderr) # prints to console
    print(json_data, file=sys.stderr) # prints to console
    return "stuff"

@app.route("/stores")
def stores():
    get_config()
    print('/stores', file=sys.stderr) # prints to console
    # print(json_data, file=sys.stderr) # prints to console
    # return json_data
    for row in json_data:
        print("town: %s, postcode: %s" % (row['name'], row['postcode']), file=sys.stderr) # prints to console
    return render_template('stores.html', stores=json_data)

def get_config():
    global json_data # !!
    # with open(os.path.join(app.config['DATA_DIR'], 'stores.json')) as json_file:
    with open('stores.json') as json_file:
        json_data = json.load(json_file)
        print('json loaded', file=sys.stderr)

if __name__ == '__main__':
    # print('test1', file=sys.stderr)
    get_config()
    app.run(debug=True)