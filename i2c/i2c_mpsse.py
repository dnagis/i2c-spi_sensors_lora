#!/usr/bin/python


#define LIS3MDL_SA1_HIGH_ADDRESS   0011110
#define LIS3MDL_SA1_LOW_ADDRESS    0011100

#bin->dec 		bc <<< "ibase=2;obase=A;100"		-> 4
#bin->hex		bc <<< "ibase=2;obase=10000;1011"	-> B
#bc <<< "obase=2;ibase=16;1E" -> 11110

from mpsse import *

i2c = MPSSE(I2C, FOUR_HUNDRED_KHZ)

print "start"

i2c.Start()
#00111101 = 3d -> SA1 HIGH + READ
#00111001 = 39 -> SA1 LOW + READ 
i2c.Write("\x39")

if i2c.GetAck() == ACK:			# Make sure the last written byte was acknowledged
		print "on a ack"
		i2c.Write("\x0F")
		i2c.Start()			# Send a re-start condition
		data = i2c.Read(1)		# Read one byte from the I2C slave
		i2c.SendNacks()			# Respond with a NACK for all subsequent reads
		i2c.Read(1)			# Read one last "dummy" byte from the I2C slave in order to send the NACK


i2c.Stop()
i2c.Close()


 
