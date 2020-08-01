#!/usr/bin/python3
# -*-coding:Latin-1 -*

#lis3mdl (magnetometer)


from pyftdi.i2c import I2cController, I2cNackError
from binascii import hexlify
from math import atan2, degrees
import time
import sys
import sqlite3



WHO_AM_I_ADDR 	 = 0x0F #Dummy: pratique pour tester un controle positif

CTRL_REG1_ADDR   = 0x20 #les controles: reglages
CTRL_REG2_ADDR   = 0x21
CTRL_REG3_ADDR   = 0x22
CTRL_REG4_ADDR   = 0x23
CTRL_REG5_ADDR   = 0x24

STATUS_REG_ADDR  = 0x27
OUT_X_L_ADDR     = 0x28 #Les 6 mag(netometer) values a chaque fois: "H"igh and "L"ow Bytes, the value is expressed as two's complement (cf ci dessous)
OUT_X_H_ADDR     = 0x29
OUT_Y_L_ADDR     = 0x2A
OUT_Y_H_ADDR     = 0x2B
OUT_Z_L_ADDR     = 0x2C
OUT_Z_H_ADDR     = 0x2D
TEMP_OUT_L_ADDR  = 0x2E #temperature. jai toujours des valeurs elevees: comme pour l esp32 (genre 50)
TEMP_OUT_H_ADDR  = 0x2F
INT_CFG_ADDR     = 0x30
INT_SRC_ADDR     = 0x31
INT_THS_L_ADDR   = 0x32
INT_THS_H_ADDR   = 0x33




#"""compute the 2's complement of int value val"""
#les valeurs dans les registers sont en High et Low bytes, et le 16 bit resultant est un 2s complement ce qui permet d avoir des valeurs signed
#(la logique: pour encoder un negatif, tu binary le positif, et tu inverses les bits.
#Avec cette manip: forcément si le MSB est a 1 c'est que le nombre encodé était négatif. Pourquoi? Parce que le nombre total de valeurs que tu peux encoder
#dans 16 bits est toujours le même: ça ne peut pas changer. Donc si le MSB est à 1 c'est que la manip d'inversion a été faite (le range est moitie moindre en fait)
#	
#Two's complement subtracts off (1<<bits) if the highest bit is 1. Taking 8 bits for example, this gives a range of 127 to -128.	
def twos_comp(val):
    if (val & (1 << (16 - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << 16)        # compute negative value
    return val                         # return positive value as is

#Conversion des valeurs en bits vers valeur en Gauss
#la scale (paramètre "FS" = Full Scale) est en Gauss. DS page 8. 
#quand tu es à FS +/- 4 (REG2) le tableau dit: il y a 6842 LSB par Gauss. J'ai mon result en LSB donc regle de 3.
def scaled(val):
	return val / 6842
	
##Calibration
#https://appelsiini.net/2018/calibrate-magnetometer/
#les valeurs float raw (genre -0.5781935) ne sont pas réparties autour de 0 --> on corrige par offset
#pour  faire la calibration comme sur un téléphone:
# --> log dans une bdd et rotater le capteur comme un avion (tilt, tanguage, roll, etc...) , puis récupérer les valeurs min et max pour chaque axe
#select min(X) from mag; et max(X), etc......


#Calibration (uniquement pour récupérer les valeurs min et max de chaque axe lors de la calibration, inutile sinon)
#prends un tuple (X, Y, Z)
#CREATE TABLE mag (id INTEGER PRIMARY KEY, X REAL, Y REAL, Z REAL);
def logbdd_mag(data):
	con = sqlite3.connect('mag.db') 
	cur = con.cursor()
	cur.execute("insert into mag (X, Y, Z) values (?, ?, ?)", data)
	con.commit()
	con.close()

#Dernière calibration (Arles bureau inside)
#X : MIN -0.501461560947091 MAX 0.332943583747442
#Y : MIN -0.532154340836013 MAX 0.00555393159894768
#Z : MIN 0.247003800058462 MAX 0.978807366267173

#le max moins la moitié du range est soustrait de la valeur. Le but est que ça tourne autour de zero.
def correction_offset(data):
	cx = data[0] - (0.332943583747442 - ((0.332943583747442 + 0.501461560947091) / 2))
	cy = data[1] - (0.00555393159894768 - ((0.00555393159894768 + 0.532154340836013) / 2))
	cz = data[2] - (0.978807366267173 - ((0.978807366267173 - 0.247003800058462) / 2))
	cd = (cx, cy, cz)
	return cd

	
	
#Explications du calcul dans le README.md
def vector_2_degrees(y, x):
    angle = -int(degrees(atan2(y, x)))
    if angle < 0:
        angle += 360
    return angle

#initialisation du bus, de la puce FTDI
ctrl = I2cController()
ctrl.configure('ftdi://ftdi:2232h/1')

#ttps://eblot.github.io/pyftdi/api/i2c.html

slave = ctrl.get_port(0x1E) #l'adresse sur le bus, i2cdetect (i2c-tools) ou i2cscan.py (pyftdi). Definie dans DS p.17, depend de SDO au GND ou pas

#commentaires extensifs dans lis3mdl-arduino
#slave.write_to(CTRL_REG1_ADDR, b'\xF0') #0x70 = 0b01110000, 0xF0 = 0b11110000 (TEMP_EN, OM = 11 (ultra-high-performance mode for X and Y); DO = 100 (10 Hz ODR))
slave.write_to(CTRL_REG1_ADDR, int('01110000',2).to_bytes(1, 'big'))
print("REG1: {:#010b}".format(   slave.read_from(CTRL_REG1_ADDR,1)[0]   ))

slave.write_to(CTRL_REG2_ADDR, b'\x00') 
print("REG2: {:#010b}".format(   slave.read_from(CTRL_REG2_ADDR,1)[0]   ))
slave.write_to(CTRL_REG3_ADDR, b'\x00') 
print("REG3: {:#010b}".format(   slave.read_from(CTRL_REG3_ADDR,1)[0]   ))


#slave.write_to(CTRL_REG4_ADDR, b'\x0C') 
slave.write_to(CTRL_REG4_ADDR, int('00001100',2).to_bytes(1, 'big'))
print("REG4: {:#010b}".format(   slave.read_from(CTRL_REG4_ADDR,1)[0]   ))
print("REG5: {:#010b}".format(   slave.read_from(CTRL_REG5_ADDR,1)[0]   ))



#Temperature (des résultats proche de 50°c, un peu ce que j'avais sur l'esp32
#TEMP_OUT = slave.read_from(TEMP_OUT_L_ADDR | 0x80, 2) 
#TEMP = TEMP_OUT[1] << 8 | TEMP_OUT[0] #combine high and low bytes
#print("TEMP=",twos_comp(TEMP))

while(True):
	MAG_OUT = slave.read_from(OUT_X_L_ADDR, 6) #pas besoin de ORer le MSB pour avoir addr auto-increment (p17 DS): la librairie le fait je pense
	
	MAG_X = MAG_OUT[1] << 8 | MAG_OUT[0] #combine high and low bytes
	MAG_Y = MAG_OUT[3] << 8 | MAG_OUT[2]
	MAG_Z = MAG_OUT[5] << 8 | MAG_OUT[4]
	
	#twos_comp -> encodage en 16 bits de valeurs signées
	#scaled -> la sensibilité, résolution, qui dépend de la configuration
	raw_data=(scaled(twos_comp(MAG_X)), scaled(twos_comp(MAG_Y)), scaled(twos_comp(MAG_Z)))
	
	#pas print() car je veux une ligne qui s'auto écrase
	#sys.stdout.write("X={:.6f} Y={:.6f} Z={:.6f} \r".format( raw_data[0],  raw_data[1], raw_data[2] ))
	#logbdd_mag(raw_data) #calibration, cf explication ci dessous	
	
	cd = correction_offset(raw_data) #pour ça il faut avoir fait la calibration
	sys.stdout.write("X={:.6f} Y={:.6f} Z={:.6f} angle={}   \r".format( cd[0], cd[1], cd[2], vector_2_degrees(cd[0],cd[1]) ))

	time.sleep(0.1)








