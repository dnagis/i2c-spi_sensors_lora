#!/bin/python3
# -*-coding:Latin-1 -*

#Accéder à l'ina219 en i²c via la librairie smbus2 en python3 sur le rpi
#Tous les commentaires sont dans le script version pyftdi

from smbus2 import SMBus
from binascii import hexlify
from math import trunc
import time
import sys


CONFIG_ADDR 	 = 0x00 
SHUNT_VOLT_ADDR	 = 0x01
BUS_VOLT_ADDR 	 = 0x02 
CURRENT_ADDR 	 = 0x04 
CALIBRATION_ADDR = 0x05

SLAVE_ADDR		=  0x40



bus = SMBus(1)


data = bus.read_i2c_block_data(SLAVE_ADDR, CONFIG_ADDR,2)
CONFIG = data[0] << 8 | data[1] 
print("config avant = {:08b} {:08b} ({:x})".format(data[0], data[1], CONFIG)) 

new_config = int('0011100110011111',2).to_bytes(2,byteorder='big')
bus.write_i2c_block_data(SLAVE_ADDR, CONFIG_ADDR, new_config)

data = bus.read_i2c_block_data(SLAVE_ADDR, CONFIG_ADDR,2)
CONFIG = data[0] << 8 | data[1] 
print("config apres = {:08b} {:08b} ({:x})".format(data[0], data[1], CONFIG)) 

max_possible_amps = 1 * 10 
current_lsb = max_possible_amps / 32767 
calibration = trunc(0.04096 / (current_lsb * 0.1))

print("calibration= 0x{:x} decimal {:d}".format(calibration, calibration))
cal_to_write = calibration.to_bytes(2, byteorder='big') 
bus.write_i2c_block_data(SLAVE_ADDR, CALIBRATION_ADDR, cal_to_write)

calib_reg = bus.read_i2c_block_data(SLAVE_ADDR,CALIBRATION_ADDR,2)
CALIB_REG = calib_reg[0] << 8 | calib_reg[1]
print("calibration reg lecture = {:#010b} {:#010b} ({:d})".format(calib_reg[0], calib_reg[1], CALIB_REG)) 

def twos_comp(val):
    if (val & (1 << (16 - 1))) != 0: 
        val = val - (1 << 16)        
    return val 

def lire_current():
	lecture = bus.read_i2c_block_data(SLAVE_ADDR,CURRENT_ADDR,2)
	BITS_CUR = lecture[0] << 8 | lecture[1]	
	#tu peux vérifier en regardant twos_comp(BITS_CUR) en {:2f} que une fois la calibration faite, la valeur de current register = (voltage register * calibration / 4096) (ds p. 12 équation 4)
	CURRENT = twos_comp(BITS_CUR) * current_lsb * 1000 #Datasheet p.23 et ina219. * 1000 pour avoir des mA
	sys.stdout.write(" current = {:.2f} mA (register: {:2f}) \r".format(CURRENT, twos_comp(BITS_CUR)))	

def lire_voltage_shunt():
	data = bus.read_i2c_block_data(SLAVE_ADDR,SHUNT_VOLT_ADDR,2)
	BITS_VOLTS = data[0] << 8 | data[1]	
	sys.stdout.write("voltage = {:.02f}mV".format(twos_comp(BITS_VOLTS) / 100)) #pour voir les bits: {:016b}

while(True):
	lire_voltage_shunt()
	lire_current()
	time.sleep(0.1)


