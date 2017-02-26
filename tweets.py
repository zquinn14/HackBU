"""
    Grabs tweets from a user's account.
"""

from __future__ import absolute_import

import json
import twitter
import re
import time
import os
import os.path

secrets_file = "secrets.json"
data_folder = "tdata"
cache_file = data_folder + "/tweetcache.json"
update_interval = 18000

tapi = None

def init():
    sf = open(secrets_file, "r")
    secrets = json.load(sf)["twitter"]
    sf.close()

    global tapi
    tapi = twitter.Api(consumer_key=secrets["consumer_key"], consumer_secret=secrets["consumer_secret"], access_token_key=secrets["token"], access_token_secret=secrets["token_secret"])

def use_cache(uname):
    if not os.path.isfile(cache_file):
        return False
    
    cf = open(cache_file, "r")

    cfdata = json.load(cf)

    cf.close()

    if not (uname in cfdata):
        return False

    ucdata = cfdata[uname]

    return time.time() - ucdata["time"] < 18000


def update_cache(uname, statuses):
    if not os.path.isdir(data_folder):
        os.mkdir(data_folder)
    
    cdata = {}
    if os.path.isfile(cache_file):
        cf = open(cache_file, "r")
        cdata = json.load(cf)
        cf.close()

    ucdata = {"time": time.time(), "statuses":[]}
    
    for s in statuses:
        ucdata["statuses"].append(s)
    
    cdata[uname] = ucdata

    cf = open(cache_file, "w")

    json.dump(cdata, cf, indent=2)

    cf.close()


def read_cache(uname):
    cf = open(cache_file, "r")

    cdata = json.load(cf)

    cf.close()

    return cdata[uname]["statuses"]


def get_statuses(username):
    if use_cache(username):
        return read_cache(username)

    statuses = tapi.GetUserTimeline(screen_name=username, include_rts=False)

    clean = []    
    for s in statuses:
        clean.append(clean_status(s.text))
    
    while True:
        if not statuses:
            break
        
        statuses = tapi.GetUserTimeline(screen_name=username, include_rts=False, max_id=statuses[len(statuses)-1].id)
        for s in statuses:
            clean.append(clean_status(s.text))
    
    update_cache(username, clean)

    return clean


def clean_status(status):
    words = re.split(r"\s+", status)

    clean = []

    for word in words:
        if word.startswith("http"): continue
        if word.startswith("@"): continue
        if word.startswith("#"): continue

        match = re.match(r"\W*([a-zA-Z']+)\W*", word)
        if not match: continue

        word = match.group(1)

        if len(word) == 1 and word != "I" and word != "i": continue

        if len(word) == 0: continue
        
        clean.append(word)

    return clean