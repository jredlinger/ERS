#!/usr/bin/python
# Rage Growers Industries
# Author: Andrew Stine

import sys
import Adafruit_DHT
import sqlite3
import time


# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
				'22': Adafruit_DHT.DHT22,
				'2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
	sensor = sensor_args[sys.argv[1]]
	pin = sys.argv[2]
else:
	print 'usage: sudo ./read_temp.py [11|22|2302] GPIOpin#'
	print 'example: sudo ./read_temp.py 2302 4 - Read from an AM2302 connected to GPIO #4'
	sys.exit(1)

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Un-comment the line below to convert the temperature to Fahrenheit.
# temperature = temperature * 9/5.0 + 32

timestamp = time.time()

connection = sqlite3.connect("temps.db")
cursor = connection.cursor()
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='readings';").fetchall()
if len(tables) == 0 :
        cursor.execute("CREATE TABLE readings (label, value, timestamp)")

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).  
# If this happens try again!
if humidity is not None and temperature is not None:
        cursor.execute("INSERT INTO readings VALUES (?,?,?);", ("Temperature", temperature, timestamp))
        cursor.execute("INSERT INTO readings VALUES (?,?,?);", ("Humidity", humidity, timestamp))
	print 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)
else:
	print 'Failed to get reading. Try again!'
	sys.exit(1)

connection.commit()
connection.close()
