#!/bin/python
# -*-coding:Latin-1 -*

#CREATE TABLE log (id INTEGER PRIMARY KEY, epoch INTEGER, data TEXT);
#sqlite3 log_lora.db "select datetime(epoch, 'unixepoch', 'localtime'), data from log;"


import sqlite3
import time

def logbdd(data):
	con = sqlite3.connect('log_lora.db') 
	con.text_factory = str #sinon plante avec sqlite3.ProgrammingError: You must not use 8-bit bytestrings unless you use a text_factory... quand je reçois des trucs du genre VÔXèÆeßHÆÿ·cçJ
	epoch = int(time.time())
	cur = con.cursor()
	values = (epoch, data)
	cur.execute("insert into log (epoch, data) values (?, ?)", values)
	con.commit()
	con.close()
	
def parse_rx_data(rx_string):
	rx=list(rx_string)
	lat_hex=rx[1:(rx[0]+1)] #'slicing -> récupérer la latitude (la longueur qu'elle occupe est dans rx_string[0]
	lon_hex=rx[

