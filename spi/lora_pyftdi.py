#!/usr/bin/python3
# -*-coding:Latin-1 -*

#https://eblot.github.io/pyftdi/api/spi.html
from pyftdi.spi import SpiController, SpiIOError
from time import sleep


FXOSC = 32000000.0
FSTEP = (FXOSC / 524288)
frf = 868 #frequ en MHz


#send one byte then receive one byte
def read_one(register):
	out = slave.exchange([register], 1)
	return out[0]

def write_one(register, payload):
	slave.exchange([register | 0x80 , payload]) #au vu de la datasheet page 80 -> on OR avec 0x80 pour que le premier bit soit à write
	
def lecture_rx():
	rx_len = read_one(0x13)#REG_13_RX_NB_BYTES -> taille du packet recu
	cur_adr = read_one(0x10) #REG_10_FIFO_RX_CURRENT_ADDR	
	print("RX_LEN: %s - CUR_ADR: %s" % (str(rx_len), hex(cur_adr)))
	write_one(0x0d , cur_adr) #REG_0D_FIFO_ADDR_PTR "FIFO SPI pointer"
	out = slave.exchange([0x00], rx_len) #REG_00_FIFO = 0x00 "FIFO r/w access"
	if chr(out[0]) == 's': #protection par lecture du premier byte (pour ne pas Rx des msgs d'autres senders
		print(out)




#initialisation SPI
spi = SpiController()
spi.configure('ftdi://ftdi:2232h/1')
slave = spi.get_port(cs=0, freq=10E6, mode=0)



print("OP_MODE=", format(read_one(0x01), '#010b'))
write_one(0x01 , 0x80) #0x01 = REG_01_OP_MODE -> 0b10000000 -> long range mode (LoRa) (p 108 )
#sleep(0.1)
write_one(0x01 , 0x01) #mode STDBY (p108)
#sleep(0.1)

#set frequency
frf = int((frf * 1000000.0) / FSTEP)
write_one(0x06 , (frf >> 16) & 0xff)
write_one(0x07 , (frf >> 8) & 0xff  )
write_one(0x08 , frf & 0xff)
#sleep(0.1)

#modem config Bw125Cr45Sf128 (0x72, 0x74, 0x04)
write_one(0x1d , 0x72) #REG_1D_MODEM_CONFIG1
write_one(0x1e , 0x74) #REG_1E_MODEM_CONFIG2
write_one(0x26 , 0x04) #REG_26_MODEM_CONFIG3


##Rx
#write_one(0x0f , 0x00) #REG_0F_FIFO_RX_BASE_ADDR --> p.35. tte la memory FIFO assignee au Rx
#write_one(0x12 , 0xff) #REG_12_IRQ_FLAGS clear ses flags
#write_one(0x01 , 0x05) #mode RxContinuous
#while True:
	#print("IRQ FLAGS:", format(read_one(0x12), '#010b'))  #REG_12_IRQ_FLAGS
#	if(read_one(0x12) & 0x40): # RX_DONE flag is up!
#		lecture_rx()
#		write_one(0x12 , 0xff) #REG_12_IRQ_FLAGS clear ses flags
#	sleep(1)
	
###Tx 
payload=bytearray(b'9105dc77b881dbcca8b')
write_one(0x0e , 0x00) #REG_0E_FIFO_TX_BASE_ADDR cf.p35 (si Rx en même temps???)
write_one(0x0d , 0x00) #REG_0D_FIFO_ADDR_PTR
slave.exchange(b'\x80' + payload) #premier byte = FIFO_ADDR8_PTR (0x00) oré avec write (0x80) cf p.80
write_one(0x22 , len(payload)) #REG_22_PAYLOAD_LENGTH
write_one(0x01 , 0x03) #mode Tx
sleep(1) #attendre que le Tx se fasse
write_one(0x01 , 0x01) #revenir en mode STDBY (0x01) (En Tx dapres datasheet p.36 devrait se faire seul)


#print(hex(read_one(0x06)))
#print(format(read_one(0x06), '#010b'))


spi.terminate()
