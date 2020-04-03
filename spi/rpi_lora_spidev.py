#!/bin/python
# -*-coding:Latin-1 -*

#lora en spidev direct pour homogeneite avec pyftdi. Pas dutilisation d interrupts



import spidev
from time import sleep
from vvnx_utils import logbdd





FXOSC = 32000000.0
FSTEP = (FXOSC / 524288)
frf = 868 #frequ en MHz

def read_one(register):
	out = spi.xfer([register] + [0])
	return out[1]
	
def write_one(register, payload):
	print 'on ecrit 0x{:X} dans le register 0x{:X}'.format(payload, register)
	out = spi.xfer([register | 0x80 , payload])
	
def lecture_rx():
	rx_len = read_one(0x13)#REG_13_RX_NB_BYTES -> taille du packet recu
	cur_adr = read_one(0x10) #REG_10_FIFO_RX_CURRENT_ADDR	
	print 'RX!!! len {:d} cur_adr 0x{:X}'.format(rx_len, cur_adr)
	write_one(0x0d , cur_adr) #REG_0D_FIFO_ADDR_PTR "FIFO SPI pointer"
	out = spi.xfer(bytearray(rx_len+1)) #astuce: le premier byte = REG_00_FIFO = 0x00 "FIFO r/w access"
	rx_string = "".join(map(chr, out[1:])) #on enleve le premier byte
	print 'on a recu: {:s}'.format(rx_string) #<type 'list'>
	if len(rx_string) != 0 and rx_string.isalnum(): #protection de messages qui font planter (IndexError: string index out of range, invalid literal for int() with base 10: '\xfa'...)
		logbdd(rx_string) 


	

#initialisation du bus spi
spi = spidev.SpiDev()
#bus, device -> /dev/spidev<bus>.<device> -> /dev/spidev0.0
spi.open(0, 0)
#spi.mode=0b00 #pas indispensable                  
spi.max_speed_hz = 5000 #indispensable !

resp = read_one(0x01)  #REG_01_OP_MODE                                    
print '0x{:X} -- {:#010b}'.format(resp, resp)

write_one(0x01, 0x80) #REG_01_OP_MODE -> long range mode (LoRa) (p 108 )
#sleep(0.1) #tester voir si necessaire

resp = read_one(0x01)                                      
print '0x{:X} -- {:#010b}'.format(resp, resp)

write_one(0x01 , 0x01) #REG_01_OP_MODE -> mode STDBY (p108)
#sleep(0.1) #tester voir si necessaire

#set frequency
frf = int((frf * 1000000.0) / FSTEP)
write_one(0x06 , (frf >> 16) & 0xff)
write_one(0x07 , (frf >> 8) & 0xff  )
write_one(0x08 , frf & 0xff)
sleep(0.1)

#modem config Bw125Cr45Sf128 (0x72, 0x74, 0x04)
write_one(0x1d , 0x72) #REG_1D_MODEM_CONFIG1
write_one(0x1e , 0x74) #REG_1E_MODEM_CONFIG2
write_one(0x26 , 0x04) #REG_26_MODEM_CONFIG3

write_one(0x12 , 0xff) #REG_12_IRQ_FLAGS clear ses flags

write_one(0x01 , 0x05) #mode RxContinuous

#boucle de Rx check de flags
while True:
	#print 'IRQ FLAGS: {:#010b}'.format(read_one(0x12)) #REG_12_IRQ_FLAGS
	if(read_one(0x12) & 0x40): # RX_DONE flag is up!
		lecture_rx()
		write_one(0x12 , 0xff) #REG_12_IRQ_FLAGS clear ses flags
	sleep(1)

spi.close()
