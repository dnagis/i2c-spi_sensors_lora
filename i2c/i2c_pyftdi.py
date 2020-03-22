#!/usr/bin/python3




from pyftdi.i2c import I2cController, I2cNackError
from binascii import hexlify

ctrl = I2cController()

ctrl.configure('ftdi://ftdi:2232h/1')

#https://eblot.github.io/pyftdi/api/i2c.html

slave = ctrl.get_port(0x1e) #l'adresse sur le bus, i2cdetect ou i2cscan.py chez pyftdi

data = slave.read_from(0x0f,1)

print(hexlify(data))
#print(hexlify(data).decode(), data.decode('utf8', errors='replace'))


 
