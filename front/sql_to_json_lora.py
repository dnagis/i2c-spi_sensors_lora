#!/usr/bin/python

#CREATE TABLE data(epoch INT, payload TEXT);

import sqlite3
import json
import sys


db_file=str(sys.argv[1])

ma_requete = 'SELECT * from data where epoch > 1583073102 and epoch < 1583080115'

conn = sqlite3.connect(db_file)
cur = conn.cursor()


cur.execute(ma_requete)
rows = cur.fetchall()
lora_array = []
length = len(rows) 



for i in range(length):
	featureDict = {"epoch":rows[i][0],"payload":int(rows[i][1])}
	lora_array.append(featureDict)
	
outputfile = open("data.js", "w+") 
outputfile.write("lora_array ="+str(lora_array)+"\n")
