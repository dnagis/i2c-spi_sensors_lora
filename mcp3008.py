#!/usr/bin/env python

#scp mcp3008.py ks:/home/lora/

from mpsse import *
from time import sleep


spi = MPSSE(SPI0, ONE_MHZ, MSB)

channel=1
byte2= 0x80 | channel<<4 #bin(0x80 | channel<<4) -> '0b10010000' bit1 single, bits  2 a 4: channel (p.19 ds_mcp3008)


while True: 


	spi.Start()	
	
	#datasheet mcp3008 page 19
	#'0b00000001' '0b10000000' -> 1st byte: start bit, 2nd byte: cf plus haut 
	
	CMD=bytearray([1,byte2,0]) #les bytes les uns apres les autres a la python2
	
	resp = spi.Transfer(str(CMD))
	
	#print(bin(ord(resp[0]))) #voir un des bytes en bin
	##print((hex(ord(resp[1])))) #voir un des bytes en hex
	##print((hex(ord(resp[2]))))
	
	result = ((ord(resp[1])&3) << 8) | ord(resp[2]) #2 lower bits de resp[1] (mask &3) , shift up de 8, OR avec resp[2]


	print(result)			
	spi.Stop()	
	sleep(1)




			
spi.Close()				
