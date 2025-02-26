#!/usr/bin/python3
# 3 Nov 2012 - Andrea Bonomi - <andrea.bonomi@gmail.com>
# https://github.com/andreax79/ServerlessNabaztag

# 1) Turn on the nose when you have unread mails
# 2) Change the lights according to the weather forecast

# ----------------------------------------------------------
# IMAP config
username = ' '
password = ''
server = 'imap. . '
port = 993
nabaztag_address = '192.168.0.*'
# weather config
city = ' '
# ----------------------------------------------------------

import socket
import urllib.request
import urllib.parse
import imaplib
import json

timeout = 10 # socket timeout in seconds
socket.setdefaulttimeout(timeout)
imap_server = imaplib.IMAP4_SSL(server, port)
imap_server.login(username, password)
imap_server.select('INBOX')

# Count the unread emails
# Count the unread emails
status, response = imap_server.status('INBOX', "(UNSEEN)")
# Decode the bytes to string and extract the unread count
unreadcount = int(response[0].decode('utf-8').split()[2].strip(').,]'))

if unreadcount:
    cmd = "nose?v=1" # turn on the nose
else:
    cmd = "nose?v=0" # turn off the nose

base_url = 'http://' + nabaztag_address + '/'
req = urllib.request.Request(base_url + cmd)
urllib.request.urlopen(req)

# Fetch the weather from openweathermap.org
with urllib.request.urlopen('http://api.openweathermap.org/data/2.5/forecast/daily?mode=json&appid=APIKEYHERE&units=metric&cnt=1&q=' + city) as response:
    data = response.read().decode('utf-8')
    data = json.loads(data)
    weather_id = data["list"][0]["weather"][0]["id"]
    v = 100
    if weather_id == 800:
        v = 0 # sun
    elif 801 <= weather_id <= 899:
        v = 1 # cloud
    elif 701 <= weather_id <= 799:
        v = 2 # fog
    elif (200 <= weather_id <= 299) or (300 <= weather_id <= 399) or (500 <= weather_id <= 599):
        v = 3 # rain
    elif 600 <= weather_id <= 699:
        v = 4 # snow
    elif 900 <= weather_id <= 999:
        v = 5 # storm

urllib.request.urlopen(base_url + "weather?v=%s" % v)
