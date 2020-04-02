#!/bin/python
# -*-coding:Latin-1 -*

import sqlite3
import time

#Appelé par rpi_lora_spidev.py
	
def logbdd(rx_string):
	#décodage latlng à partir de mon encodage locgatt type '9105dc77b881dbcca8b' (9=length latitude, 8=length longitude)
	#rx = list('9105dc77b881dbcca8b') #pour tests
	rx=list(rx_string) #'9105dc77b881dbcca8b'
	if rx[0] == 9:
		return
	lat_hex_list=rx[1:(int(rx[0])+1)] #[x:y] = slicing -> récupérer la latitude (la longueur qu'elle occupe est dans rx_string[0])
	lng_offset=int(rx[0])+1 #offset longitude: après rx[0] + bytes occupés par la latitude
	lng_len=int(rx[lng_offset]) #taille de la lng est là (après ce qui concerne la lat)
	lng_hex_list=rx[lng_offset+1:lng_offset+1+lng_len] #récupération de la longitude (le slicing marche pas par size hélas)
	lat_hex=''.join(lat_hex_list) #transormation en string
	lng_hex=''.join(lng_hex_list)
	lat = int(lat_hex, 16) / 100000000.0 #transormation en float, décodage de ce qui a été fait dans LocGatt
	lng = int(lng_hex, 16) / 100000000.0
	print "on va ecrire", lat, lng
	#écriture dans la base de données
	#CREATE TABLE log (id INTEGER PRIMARY KEY, epoch INTEGER, lat REAL NOT NULL, lng REAL NOT NULL);
	#sqlite3 log_lora.db "select datetime(epoch, 'unixepoch', 'localtime'), lat, lng from log;"
	con = sqlite3.connect('log_lora.db') 
	con.text_factory = str #sinon plante avec sqlite3.ProgrammingError: You must not use 8-bit bytestrings unless you use a text_factory... quand je reçois des trucs du genre VÔXèÆeßHÆÿ·cçJ
	epoch = int(time.time())
	cur = con.cursor()
	values = (epoch, lat, lng)
	cur.execute("insert into log (epoch, lat, lng) values (?, ?, ?)", values)
	con.commit()
	con.close()
