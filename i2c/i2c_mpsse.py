#!/usr/bin/python
# -*-coding:Latin-1 -*

#i2c avec la puce FTDI
#Un essai rapide avant que je decouvre pyftdi. Je n'ai pas explore
#Exemple tire de la librairie mpsse 
#jarrive juste a avoir un acknowledge mais pas plus, pas fouile.

from mpsse import *
from binascii import hexlify

i2c = MPSSE(I2C, FOUR_HUNDRED_KHZ)

print "start"

i2c.Start()
#00111101 = 3d -> SA1 HIGH + READ
#00111001 = 39 -> SA1 LOW + READ 
i2c.Write("\x3d")

if i2c.GetAck() == ACK:			# Make sure the last written byte was acknowledged
		print "on a ack"
		i2c.Write("\x0F")
		i2c.Start()			# Send a re-start condition
		data = i2c.Read(1)		# Read one byte from the I2C slave
		i2c.SendNacks()			# Respond with a NACK for all subsequent reads
		i2c.Read(1)			# Read one last "dummy" byte from the I2C slave in order to send the NACK

print(hexlify(data))

i2c.Stop()
i2c.Close()


 
