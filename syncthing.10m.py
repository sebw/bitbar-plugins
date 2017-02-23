#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <bitbar.title>Syncthing Folders Status</bitbar.title>
# <bitbar.version>0.2</bitbar.version>
# <bitbar.author>Sebastien Wains</bitbar.author>
# <bitbar.author.github>sebw</bitbar.author.github>
# <bitbar.desc>Provides status of Syncthing folders</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>

import urllib2
import json
import ConfigParser
import os

def syncthing_api(url, headers):
    req = urllib2.Request(url, None, headers)
    resp = urllib2.urlopen(req)
    data = json.load(resp)
    return data

conf_path = os.path.dirname(os.path.realpath(__file__)) + "/conf/syncthing.ini"

Config = ConfigParser.ConfigParser()
Config.read(conf_path)

# variables from conf
api = Config.get("main", "api")
url = Config.get("main", "url")
# end of variables

# Strip quotes from strings returned by ConfigParser
api_strip = api.strip("'")
url_strip = url.strip("'")

# API function
folder_stat_path = "/rest/stats/folder"
folder_info_path = "/rest/db/status?folder="

# API URL
folder_stat = url_strip + folder_stat_path
folder_info = url_strip + folder_info_path

headers = {'X-API-Key': api_strip}

# Get list of shared folders with last sync info
data = syncthing_api(folder_stat, headers)

print "🔁"
print "---"

# Construct menu, folders out of sync are red, otherwise green
for folder_id, value in data.iteritems():
    detail = syncthing_api(folder_info + folder_id, headers)
    if detail['globalFiles'] == detail['localFiles']:
        color = 'green'
    else:
        color = 'red'
    print folder_id + "| color=" + color
    print "-- Global files: " + str(detail['globalFiles']) + " Local files: " + str(detail['localFiles'])
    date = value['lastScan']
    date_day = date.rsplit('T')[0]
    date_hour = date.rsplit('T')[1].rsplit('.')[0]
    print "-- Last scan: " + date_day + " " + date_hour
