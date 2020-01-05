#!/usr/bin/env python

from mpsse import *
from time import sleep

FXOSC = 32000000.0
FSTEP = (FXOSC / 524288)

frf = 915 #frequ en MHz



spi = MPSSE(SPI0, ONE_MHZ, MSB)


def spi_write_one(register, payload):
	spi.Start() 	# Bring chip-select low
	CMD=bytearray([register | 0x80 , payload]) #au vu de la datasheet page 80 -> on OR avec 0x80 pour que le premier bit soit a write
	spi.Write(str(CMD))
	spi.Stop()

def spi_read_one(register):
	spi.Start() 	# Bring chip-select low
	CMD=bytearray([register, 0])
	resp = spi.Transfer(str(CMD))	
	spi.Stop()
	return resp[1]

def lecture_rx():
	rx_len = spi_read_one(0x13)#REG_13_RX_NB_BYTES -> taille du packet recu
	#print("Rx nb bytes:"+str(ord(rx_len)))
	cur_adr = spi_read_one(0x10) #REG_10_FIFO_RX_CURRENT_ADDR	
	spi_write_one(0x0d , cur_adr)
	#Il faut un transfer pour pouvoir Rx. On recoit le msg donc plusieurs bytes. 
	CMD=bytearray(ord(rx_len)+1) #Bytearray remplis de 0 (initialisation de bytearray, essaie str(CMD)). le register REG_00_FIFO (0x00) est en premier 
	spi.Start()
	resp = spi.Transfer(str(CMD))
	spi.Stop()
	rx_string = resp[1:] #Enlever le premier byte (il servait au transfer seulement)
	print(rx_string)
	




spi_write_one(0x01 , 0x80) #0x01 = REG_01_OP_MODE -> 0b10000000 -> long range mode (LoRa) (p 108 )
sleep(0.1)

#spi_write_one(0x0f , 0x00) #REG_0F_FIFO_RX_BASE_ADDR --> p.35. tte la memory FIFO assignee au Rx
spi_write_one(0x0e , 0x00) #REG_0F_FIFO_TX_BASE_ADDR --> p.35. tte la memory FIFO assignee au Tx
sleep(0.1)

spi_write_one(0x01 , 0x01) #mode STDBY (p108)
sleep(0.1)



# set frequency
frf = int((frf * 1000000.0) / FSTEP)
#print( hex((frf >> 16) & 0xff) )
#print( hex( (frf >> 8) & 0xff  ) )
#print(  hex(  frf & 0xff  )  )
spi_write_one(0x06 , (frf >> 16) & 0xff)
spi_write_one(0x07 , (frf >> 8) & 0xff  )
spi_write_one(0x08 , frf & 0xff)

sleep(0.1)
#read frequency
#spi_read_one(0x06)
#spi_read_one(0x07)
#spi_read_one(0x08)

#modem config jessaie Bw125Cr45Sf128 (0x72, 0x74, 0x04)
spi_write_one(0x1d , 0x72) #REG_1D_MODEM_CONFIG1
spi_write_one(0x1e , 0x74) #REG_1E_MODEM_CONFIG2
spi_write_one(0x26 , 0x04) #REG_26_MODEM_CONFIG3


spi_write_one(0x12 , 0xff) #REG_12_IRQ_FLAGS clear ses flags



###Rx => lecture IRQ flags toutes les secondes dans un loop

#spi_write_one(0x01 , 0x05) #mode RxContinuous
#for x in range(10):
#	print("IRQ FLAGS:"+bin(ord(spi_read_one(0x12))))  #REG_12_IRQ_FLAGS
#	if(ord(spi_read_one(0x12)) & 0x40): # RX_DONE flag is up!
#		lecture_rx()
#	sleep(1)



###Tx 
payload='hello sri lanka...'
spi_write_one(0x0d , 0x00) #REG_0D_FIFO_ADDR_PTR
spi.Start()
spi.Write('\x80'+payload) #premier byte = 0x00 | 0x80 cf p.80
spi.Stop()
spi_write_one(0x22 , len(payload)) #REG_22_PAYLOAD_LENGTH
spi_write_one(0x01 , 0x03) #mode Tx
sleep(1) #histoire dattendre que le Tx se fasse

spi_write_one(0x01 , 0x01) #revenir en mode STDBY (0x01) (En Tx dapres datasheet p.36 devrait se faire seul)

		
spi.Close()		


		

