#!/usr/bin/python3
# -*-coding:Latin-1 -*

#ina219
#https://github.com/chrisb2/pi_ina219/
#"PGA" = Programmable Gain Amplifier

from pyftdi.i2c import I2cController, I2cNackError
from binascii import hexlify
import time



def twos_comp(val):
    if (val & (1 << (16 - 1))) != 0: 
        val = val - (1 << 16)        
    return val                         


CONFIG_ADDR 	 = 0x00 
SHUNT_VOLT_ADDR	 = 0x01
BUS_VOLT_ADDR 	 = 0x02 
CURRENT_ADDR 	 = 0x04 


#initialisation du bus, de la puce FTDI
ctrl = I2cController()
ctrl.configure('ftdi://ftdi:2232h/1')

#https://eblot.github.io/pyftdi/api/i2c.html

slave = ctrl.get_port(0x40) #l'adresse sur le bus, i2cdetect (i2c-tools) ou i2cscan.py (pyftdi) -> voir le README.md 

#http://henrysbench.capnfatz.com/henrys-bench/arduino-current-measurements/ina219-arduino-current-sensor-voltmeter-tutorial-quick-start/

data = slave.read_from(CONFIG_ADDR,2)
print("{:#010b} {:#010b}".format(data[0], data[1]))
CONFIG = data[0] << 8 | data[1] 
print("{:x}".format(CONFIG)) #pour contrôle: au reset doit être à 399f

#print(twos_comp(int('1000001100000000',2)))


#Le voltage du BUS a les 3 LSB qui ne holdent pas de value (DS p.23) . Il faut bricoler surement


while(True):
	data = slave.read_from(SHUNT_VOLT_ADDR,2)
	RAW_DATA = data[0] << 8 | data[1]
	RESULT = twos_comp(RAW_DATA) * .01 #LSB = 4 mv pour le bus, 10 µV pour le shunt. Datasheet p.23
	print("{:.2f}".format(RESULT))
	time.sleep(0.1)

