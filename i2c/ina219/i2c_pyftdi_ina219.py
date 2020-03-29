#!/usr/bin/python3
# -*-coding:Latin-1 -*

#ina219
#https://github.com/chrisb2/pi_ina219/

from pyftdi.i2c import I2cController, I2cNackError
from binascii import hexlify




CONFIG_ADDR 	 = 0x00 


#initialisation du bus, de la puce FTDI
ctrl = I2cController()
ctrl.configure('ftdi://ftdi:2232h/1')

#https://eblot.github.io/pyftdi/api/i2c.html

slave = ctrl.get_port(0x40) #l'adresse sur le bus, i2cdetect (i2c-tools) ou i2cscan.py (pyftdi) -> voir le README.md 

#print("REG1: {:#010b}".format(   slave.read_from(CTRL_REG1_ADDR,1)[0]   ))

data = slave.read_from(CONFIG_ADDR,2)
print("{:#010b}".format(data[0]))
print("{:#010b}".format(data[1]))
