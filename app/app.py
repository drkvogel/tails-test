from flask import Flask, render_template
from flask.json import jsonify
import os
import sys
import json
import requests
from pprint import pprint

app = Flask(__name__)

latlng_cache = {}
stores = {}

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/test")
def test():
    get_config()
    return "stuff"

def get_latlng(postcode):
    global latlng_cache
    if postcode not in latlng_cache:
        r = requests.get('https://api.postcodes.io/postcodes/' + postcode)
        if r.status_code != 200:
            print("%s: status_code: %s" % (postcode, r.status_code), file=sys.stderr)
            # raise Exception("r.status_code != 200")
            # ? might be a temporary error with the provider, log it though...
            return (0, 0) # or some values reserved to mean "unknown" # FIXME...
        else:
            # get lat, long
            data = json.loads(r.text)
            result = data['result']
            lat = result['latitude']
            lng = result['longitude']
            latlng_cache[postcode] = (lat, lng)

    return latlng_cache[postcode]

@app.route("/stores")
def list_stores():
    get_config() # do on init instead
    rows = ''
    for name in sorted(stores):
        lat, lng = get_latlng(stores[name])
        rows = rows + "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n" % (name.replace('_', ' '), stores[name], lat, lng)
    return render_template('stores.html', stores=stores, rows=rows)

def get_config():
    global stores # !!
    print('get_config', file=sys.stderr)
    with open('stores.json') as json_file:
        rows = json.load(json_file) # dict of dicts
        for row in rows:
            stores[row['name']] = row['postcode']   # new dict

if __name__ == '__main__':
    print('__main__', file=sys.stderr)
    get_config()
    app.run(debug=True)
