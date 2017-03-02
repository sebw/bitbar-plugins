#!/usr/bin/env PYTHONIOENCODING=UTF-8 python
# -*- coding: utf-8 -*-
# <bitbar.title>Syncthing Folders Status</bitbar.title>
# <bitbar.version>0.3</bitbar.version>
# <bitbar.author>Sebastien Wains</bitbar.author>
# <bitbar.author.github>sebw</bitbar.author.github>
# <bitbar.desc>Provides status of Syncthing folders</bitbar.desc>
# <bitbar.image>https://raw.githubusercontent.com/sebw/bitbar-plugins/master/syncthing.png</bitbar.image>
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

# API functions
folder_stat_path = "/rest/stats/folder"
folder_info_path = "/rest/db/status?folder="
system_config_path = "/rest/system/config"
system_status_path = "/rest/system/status"
system_version_path = "/rest/system/version"
system_connections_path = "/rest/system/connections"

# API URLs
folder_stat = url_strip + folder_stat_path
folder_info = url_strip + folder_info_path
system_config = url_strip + system_config_path
system_status = url_strip + system_status_path
system_version = url_strip + system_version_path
system_connections = url_strip + system_connections_path

headers = {'X-API-Key': api_strip}

# Get list of shared folders with last sync info
data = syncthing_api(folder_stat, headers)

# Get system configuration (containing folder labels)
system_config_info = syncthing_api(system_config, headers)

# Get folder labels
folder_labels = {}
for folder in system_config_info['folders']:
    folder_labels[folder.get('id')] = folder.get('label')

# Get system information
system_status_info = syncthing_api(system_status, headers)
system_version_info = syncthing_api(system_version, headers)
myID = system_status_info['myID']

print "⇵"

# Construct menu: system information
print "---"
print "Syncthing " + system_version_info['version'] + "| href=" + url_strip

print "---"

# Construct menu: folders out of sync are red, otherwise green
print "Folders: | color = black"
for folder_id, value in sorted(data.iteritems()):
    detail = syncthing_api(folder_info + folder_id, headers)
    if detail['globalFiles'] == detail['localFiles']:
        color = 'green'
    else:
        color = 'red'
    if folder_labels[folder_id] == '':
        folder_labels[folder_id] = folder_id
    if folder_id == folder_labels[folder_id]:
        print '- ' + folder_id + "| color=" + color
    else:
        print '- ' + folder_labels[folder_id] + "| color=" + color
    print "-- Global: files " + str(detail['globalFiles']) + " - directories " + str(detail['globalDirectories'])
    print "-- Local: files " + str(detail['localFiles']) + " - directories " + str(detail['localDirectories'])
    date = value['lastScan']
    date_day = date.rsplit('T')[0]
    date_hour = date.rsplit('T')[1].rsplit('.')[0]
    print "-- Last scan: " + date_day + " " + date_hour
    if value['lastFile']['filename'] != '':
        print "-- Last received file: " + value['lastFile']['filename'].encode('ascii', 'ignore')

# Construct menu: devices
print "---"
print "Remote Devices: | color = black"
connections = syncthing_api(system_connections, headers)
for device in sorted(system_config_info['devices']):
    if device.get('deviceID') != myID:
        online = connections['connections'][device.get('deviceID')]['connected']
        paused = connections['connections'][device.get('deviceID')]['paused']
        if online == 1 and paused == 0:
            print '- ' + device.get('name') + '| color = black'
        if online == 0 and paused == 0:
            print '- ' + device.get('name') + ' (offline)'
        if online == 1 and paused == 1:
            print '- ' + device.get('name') + ' (paused)'
        if online == 0 and paused == 1:
            print '- ' + device.get('name') + ' (offline, paused)'
