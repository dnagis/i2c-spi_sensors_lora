#!/usr/bin/python3

#lis3mdl (magnetometer)


from pyftdi.i2c import I2cController, I2cNackError
from binascii import hexlify
from math import atan2, degrees


WHO_AM_I_ADDR 	 = 0x0F #Dummy: pratique pour tester un controle positif

CTRL_REG1_ADDR   = 0x20 #les controles: reglages
CTRL_REG2_ADDR   = 0x21
CTRL_REG3_ADDR   = 0x22
CTRL_REG4_ADDR   = 0x23
CTRL_REG5_ADDR   = 0x24

STATUS_REG_ADDR  = 0x27
OUT_X_L_ADDR     = 0x28 #Les 6 mag value a chaque fois: High and Low Bytes, the value is expressed as two's complement 
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

#Transformer un hex en binary avec les leading zeros
def hex_vers_bin(value):
	#https://www.devdungeon.com/content/working-binary-data-python
	return format(ord(value), '#010b')

#l inverse	
def bin_vers_hex(value):
	return hex(int(value))

#les valeurs sont en High et Low bytes, et le 16 bit resultant est un 2s complement ce qui permet d avoir des valeurs signed
#Two's complement subtracts off (1<<bits) if the highest bit is 1. Taking 8 bits for example, this gives a range of 127 to -128.	
def twos_comp(val):
    """compute the 2's complement of int value val"""
    if (val & (1 << (16 - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << 16)        # compute negative value
    return val                         # return positive value as is

def vector_2_degrees(x, y):
    angle = degrees(atan2(y, x))
    if angle < 0:
        angle += 360
    return angle

#initialisation du bus, de la puce FTDI
ctrl = I2cController()
ctrl.configure('ftdi://ftdi:2232h/1')

#ttps://eblot.github.io/pyftdi/api/i2c.html

slave = ctrl.get_port(0x1E) #l'adresse sur le bus, i2cdetect (i2c-tools) ou i2cscan.py (pyftdi). Definie dans DS p.17, depend de SDO au GND ou pas

#print(bin_vers_hex(0b11110000))
slave.write_to(CTRL_REG1_ADDR, b'\xF0') #0x70 = 0b01110000, 0xF0 = 0b11110000 (TEMP_EN, OM = 11 (ultra-high-performance mode for X and Y); DO = 100 (10 Hz ODR))
REG_1 = slave.read_from(CTRL_REG1_ADDR,1) #print(type(REG_DATA)) -> #<class 'bytearray'>
print("REG1=",hex_vers_bin(REG_1))

slave.write_to(CTRL_REG2_ADDR, b'\x00') #pour la suite voir lis3mdl-arduino
REG_2 = slave.read_from(CTRL_REG2_ADDR,1) 
print("REG2=",hex_vers_bin(REG_2))

slave.write_to(CTRL_REG3_ADDR, b'\x00') 
REG_3 = slave.read_from(CTRL_REG3_ADDR,1) 
print("REG3=",hex_vers_bin(REG_3))

slave.write_to(CTRL_REG4_ADDR, b'\x0C') 
REG_4 = slave.read_from(CTRL_REG4_ADDR,1) 
print("REG4=",hex_vers_bin(REG_4))

REG_5 = slave.read_from(CTRL_REG5_ADDR,1) 
print("REG5=",hex_vers_bin(REG_5))

#Temperature
#TEMP_OUT = slave.read_from(TEMP_OUT_L_ADDR | 0x80, 2) 
#TEMP = TEMP_OUT[1] << 8 | TEMP_OUT[0] #combine high and low bytes
#print("TEMP=",twos_comp(TEMP))


MAG_OUT = slave.read_from(OUT_X_L_ADDR, 6) #pas besoin de ORer le MSB pour avoir addr auto-increment: la librairie le fait je pense
MAG_X = MAG_OUT[1] << 8 | MAG_OUT[0] #combine high and low bytes
MAG_Y = MAG_OUT[3] << 8 | MAG_OUT[2]
MAG_Z = MAG_OUT[5] << 8 | MAG_OUT[4]
print("X=",twos_comp(MAG_X))
print("Y=",twos_comp(MAG_Y))
print("Z=",twos_comp(MAG_Z))


print("{:.2f}".format(vector_2_degrees(MAG_X,MAG_Y)))

