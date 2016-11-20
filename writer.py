#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import time
import datetime
from sense_hat import SenseHat

SLEEP = 300

sense = SenseHat()
sense.clear()


def init_db():
    """Connects to the specific database."""
    con = lite.connect("sensehat.db")
    cur = con.cursor()
    query = """CREATE TABLE IF NOT EXISTS
                    sensehat(epoch INT,
                             humidity REAL,
                             pressure REAL,
                             temp_hum REAL,
                             temp_prs REAL)"""
    cur.execute(query)


if __name__ == "__main__":
    humidity = round(sense.humidity, 1)
    pressure = round(sense.get_pressure(), 2)
    temperature_from_humidity = round(sense.get_temperature(), 1)
    temperature_from_pressure = round(sense.get_temperature_from_pressure(), 1)

    init_db()
    while 1:
        humidity = round(sense.humidity, 1)
        pressure = round(sense.get_pressure(), 2)
        temperature_from_humidity = round(sense.get_temperature(), 1)
        temperature_from_pressure = round(
            sense.get_temperature_from_pressure(), 1)

        con = lite.connect("sensehat.db")
        with con:
            print("%s - Inserting data." % datetime.datetime.now().isoformat())
            cur = con.cursor()
            command = "INSERT INTO sensehat VALUES(%i,%0.2f,%0.2f,%0.2f,%0.2f)" % (int(
                time.time()), humidity, pressure, temperature_from_humidity, temperature_from_pressure)
            cur.execute(command)

        print("%s - Sleeping for %i seconds." %
              (datetime.datetime.now().isoformat(), SLEEP))
        time.sleep(SLEEP)
