#!/usr/bin/python
# Rage Growers Industries
# Author: Andrew Stine

import sys
import sqlite3
import urllib
import json
import time

timestamp = time.time()

connection = sqlite3.connect("temps.db")
cursor = connection.cursor()
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND (name='readings' OR name='settings');").fetchall()
if len(tables) == 0 :
        exec python setup.py


readings = cursor.execute("SELECT label, value, timestamp, sequence FROM readings;")

readings_output = json.dumps(readings)

urllib.urlopen("centralserver.com", readings_output)

connection.commit()
connection.close()
