#!/usr/bin/python3

#pour lis3mdl (magnetometer)


from pyftdi.i2c import I2cController, I2cNackError
from binascii import hexlify


WHO_AM_I_ADDR = 0x0F
CTRL_REG_ADDR = 0x20

#https://www.devdungeon.com/content/working-binary-data-python
def hex_vers_bin(data):
	return "{0:b}".format(ord(REG_DATA))


#initialisation du bus, de la puce FTDI
ctrl = I2cController()
ctrl.configure('ftdi://ftdi:2232h/1')

#https://eblot.github.io/pyftdi/api/i2c.html

slave = ctrl.get_port(0x1E) #l'adresse sur le bus, i2cdetect (i2c-tools) ou i2cscan.py (pyftdi)




REG_DATA = slave.read_from(CTRL_REG_ADDR,1)

print(type(REG_DATA)) #<class 'bytearray'>

print(hexlify(REG_DATA))
#print(hexlify(data).decode(), data.decode('utf8', errors='replace'))


print(hex_vers_bin(REG_DATA))
#print("{0:b}".format(ord(REG_DATA)))
