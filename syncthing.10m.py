#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <bitbar.title>Syncthing Folders Status</bitbar.title>
# <bitbar.version>0.1</bitbar.version>
# <bitbar.author>Sebastien Wains</bitbar.author>
# <bitbar.author.github>sebw</bitbar.author.github>
# <bitbar.desc>Provides status of Syncthing folders</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>

import urllib2
import json
import ConfigParser
import os

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
rest = "/rest/stats/folder"

url_full = url_strip + rest
headers = {'X-API-Key': api_strip}

req = urllib2.Request(url_full, None, headers)
resp = urllib2.urlopen(req)
data = json.load(resp)

print "🔁"
print "---"

for key, value in data.iteritems():
    print key
    print "Last scan: " + value['lastScan']
    print "---"
