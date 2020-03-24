#!/bin/python

#CREATE TABLE log (id INTEGER PRIMARY KEY, epoch INTEGER, data TEXT);
#sqlite3 log_lora.db "select datetime(epoch, 'unixepoch', 'localtime'), data from log;"

import sqlite3
import time

def logbdd(data):
	con = sqlite3.connect('log_lora.db') 
	epoch = int(time.time())
	cur = con.cursor()
	values = (epoch, data)
	cur.execute("insert into log (epoch, data) values (?, ?)", values)
	con.commit()
	con.close()

