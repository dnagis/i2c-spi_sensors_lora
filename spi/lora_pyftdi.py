#!/usr/bin/python3


from pyftdi.spi import SpiController, SpiIOError


spi = SpiController()

spi.configure('ftdi://ftdi:2232h/1')


slave = spi.get_port(cs=0, freq=10E6, mode=0)



#out = slave.exchange([0x01, 0x00], 2)
#print(out)

write_buf = b'\x06\x00'
read_buf = slave.exchange(write_buf, duplex=True)
print(hex(read_buf[1]))

write_buf = b'\x07\x00'
read_buf = slave.exchange(write_buf, duplex=True)
print(hex(read_buf[1]))




write_buf = b'\x01\x00'
read_buf = slave.exchange(write_buf, duplex=True)
print(hex(read_buf[1]))
print(format(read_buf[1], '#010b'))

spi.terminate()
