#!/usr/bin/python
# Rage Growers Industries
# Author: Andrew Stine

import sys
import sqlite3
import time

timestamp = time.time()

connection = sqlite3.connect("temps.db")
cursor = connection.cursor()
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='readings';").fetchall()
if len(tables) == 0 :
        cursor.execute("CREATE TABLE readings (label, value, timestamp, sequence);")

tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='settings';").fetchall()
if len(tables) == 0 :
        cursor.execute("CREATE TABLE settings (setting, value);")
        cursor.execute("INSERT INTO settings VALUES (?, ?);", ("last_sequence", 0))
