#!/bin/python3
# -*-coding:Latin-1 -*

#lis3mdl (magnetometer) 
#en smbus2 pour le rpi, pas pigpio (pas besoin de daemon avec cette librairie)
#les commentaires dans la version pyftdi

from smbus2 import SMBus
import time
from math import atan2, degrees
import sys
import sqlite3

SLAVE_ADDR		=  0x1E

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
TEMP_OUT_L_ADDR  = 0x2E 
TEMP_OUT_H_ADDR  = 0x2F
INT_CFG_ADDR     = 0x30
INT_SRC_ADDR     = 0x31
INT_THS_L_ADDR   = 0x32
INT_THS_H_ADDR   = 0x33


def logbdd_mag(data):
	con = sqlite3.connect('mag.db') 
	cur = con.cursor()
	cur.execute("insert into mag (X, Y, Z) values (?, ?, ?)", data)
	con.commit()
	con.close()


def correction_offset(data):
	cx = data[0] - ((0.363197895352236 - 0.578193510669395) / 2)
	cy = data[1] - ((0.143671441099094 - 0.748757673194972) / 2)
	cz = data[2] - ((0.989330605086232 + 0.106986261327097) / 2)
	cd = (cx, cy, cz)
	return cd

def twos_comp(val):
    if (val & (1 << (16 - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << 16)        # compute negative value
    return val 

def scaled(val):
	return val / 6842
	
def vector_2_degrees(x, y):
    angle = int(degrees(atan2(x, y)))
    if angle < 0:
        angle += 360
    return angle


bus = SMBus(1)

#print("{:#010b}".format(bus.read_byte_data(SLAVE_ADDR, WHO_AM_I_ADDR)))

bus.write_byte_data(SLAVE_ADDR, CTRL_REG1_ADDR, 0x70)
print("REG1: {:#010b}".format(bus.read_byte_data(SLAVE_ADDR, CTRL_REG1_ADDR)))

bus.write_byte_data(SLAVE_ADDR, CTRL_REG2_ADDR, 0x00)
print("REG2: {:#010b}".format(bus.read_byte_data(SLAVE_ADDR, CTRL_REG2_ADDR)))
bus.write_byte_data(SLAVE_ADDR, CTRL_REG3_ADDR, 0x00)
print("REG3: {:#010b}".format(bus.read_byte_data(SLAVE_ADDR, CTRL_REG3_ADDR)))
bus.write_byte_data(SLAVE_ADDR, CTRL_REG4_ADDR, 0x0C)
print("REG4: {:#010b}".format(bus.read_byte_data(SLAVE_ADDR, CTRL_REG4_ADDR)))

print("REG5: {:#010b}".format(bus.read_byte_data(SLAVE_ADDR, CTRL_REG5_ADDR)))




while(True):
	MAG_OUT = bus.read_i2c_block_data(SLAVE_ADDR, OUT_X_L_ADDR,6)
	
	MAG_X = MAG_OUT[1] << 8 | MAG_OUT[0] #combine high and low bytes
	MAG_Y = MAG_OUT[3] << 8 | MAG_OUT[2]
	MAG_Z = MAG_OUT[5] << 8 | MAG_OUT[4]
	
	raw_data=(scaled(twos_comp(MAG_X)), scaled(twos_comp(MAG_Y)), scaled(twos_comp(MAG_Z)))
	
	cd = correction_offset(raw_data)
	
	#logbdd_mag(raw_data) #calibration
	
	sys.stdout.write("X={:.6f} Y={:.6f} Z={:.6f} angle={}   \r".format( cd[0], cd[1], cd[2], vector_2_degrees(cd[0],cd[1]) ))
	time.sleep(0.1)
	
