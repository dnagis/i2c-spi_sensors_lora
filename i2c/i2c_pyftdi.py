#!/usr/bin/python3

#lis3mdl en i2c via USB grâce au ftdi
#OK chiant mais c'est du python3

#pip install pyftdi (je suppose qu'il faut que les librairies mpsse et ftdi soient installées)
#pyftdi a un i2cscan.py qui marche comme i2cdetect
#https://eblot.github.io/pyftdi/pinout.html
#https://eblot.github.io/pyftdi/api/i2c.html#i2c-wiring --> attention il faut que AD1 ET AD2 du ftdi 2232 soient connectés au SDA du slave


#define LIS3MDL_SA1_HIGH_ADDRESS   0011110 ->0x1E
#define LIS3MDL_SA1_LOW_ADDRESS    0011100 ->0x1C (si le pin SDO/SA1 est au GND, datasheet lis3mdl p.17)

#bin->dec 		bc <<< "ibase=2;obase=A;100"		-> 4
#bin->hex		bc <<< "ibase=2;obase=10000;1011"	-> B
#hex->bin		bc <<< "obase=2;ibase=16;1E" -> 11110


#https://github.com/adafruit/Adafruit_CircuitPython_LIS3MDL/blob/master/adafruit_lis3mdl.py
#https://github.com/adafruit/Adafruit_CircuitPython_LIS3MDL/blob/master/examples/lis3mdl_compass.py
#https://github.com/tkurbad/mipSIE/blob/master/python/AltIMU-10v5/lis3mdl.py

from pyftdi.i2c import I2cController, I2cNackError
from binascii import hexlify

ctrl = I2cController()

ctrl.configure('ftdi://ftdi:2232h/1')

#https://eblot.github.io/pyftdi/api/i2c.html

slave = ctrl.get_port(0x1e) #l'adresse sur le bus, i2cdetect ou i2cscan.py chez pyftdi

data = slave.read_from(0x0f,1)

print(hexlify(data))
#print(hexlify(data).decode(), data.decode('utf8', errors='replace'))


 
