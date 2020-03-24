#!/bin/python
import spidev

#lora en spidev direct pour homogeneite avec pyftdi

spi = spidev.SpiDev()
#bus, device -> /dev/spidev<bus>.<device> -> /dev/spidev0.0
spi.open(0, 0)
#spi.mode=0b00 #pas indispensable                  
spi.max_speed_hz = 5000 #indispensable !

resp = spi.xfer([0x01, 0x00])
print '0x{:X} -- {:#010b}'.format(resp[1], resp[1])

resp2 = spi.xfer([0x06, 0x00])
print '0x{:X} -- {:#010b}'.format(resp2[1], resp2[1])




spi.close()
