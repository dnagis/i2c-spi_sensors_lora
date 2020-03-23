#!/usr/bin/python3

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
	slave.exchange([register | 0x80 , payload]) #au vu de la datasheet page 80 -> on OR avec 0x80 pour que le premier bit soit a write

#initialisation SPI
spi = SpiController()
spi.configure('ftdi://ftdi:2232h/1')
slave = spi.get_port(cs=0, freq=10E6, mode=0)


print("OP_MODE=", format(read_one(0x01), '#010b'))
write_one(0x01 , 0x80) #0x01 = REG_01_OP_MODE -> 0b10000000 -> long range mode (LoRa) (p 108 )
sleep(0.1)
write_one(0x01 , 0x01) #mode STDBY (p108)
sleep(0.1)

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

while True:
	print("IRQ FLAGS:", format(read_one(0x12), '#010b'))  #REG_12_IRQ_FLAGS
	sleep(1)


#print(hex(read_one(0x06)))
#print(format(read_one(0x06), '#010b'))


spi.terminate()
