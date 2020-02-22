#!/bin/python
from raspi_lora import LoRa, ModemConfig
import time
import datetime
import signal
import sys

#Rx: _handle_interrupt() -> packet est Rx ici. ajouter un self.on_recv(packet) dans le premier if dès que le packet est récupéré
#Tx: _spi_write() -> self.spi.xfer([register | 0x80] + payload) marche si payload = [10, 2, 1, 0, 10, 20, 30], pas si [10, 2, 1, 0, 'H', 'e', 'l', 'l', 'o']
#error: Non-Int/Long value in arguments: 7a0315a8 -> faut faire la conversion des lettres en ascii, j'ai pas fait encore (spi.xfer([0x80] + list(bytearray(payload)))???)

def receiveSignal(signalNumber, frame):
    print('Received:', signalNumber)
    lora.close()
    sys.exit()
    
def on_recv(payload):
    current_time = str(datetime.datetime.now())
    print("message recu:" + str(bytearray(payload)) + " @ " + current_time)
    f = open("log_lora", "a")
    f.write(str(bytearray(payload)) + " @ " + current_time + "\n")
    f.close()

signal.signal(signal.SIGINT, receiveSignal)

lora = LoRa(0, 17, 2,  freq=868, modem_config=ModemConfig.Bw125Cr45Sf128, tx_power=14, acks=True)
lora.on_recv = on_recv 
lora.set_mode_rx()

while True:
    print('Waiting...')
    time.sleep(10)
    
#Tx:    
#message = [10, 20, 30, 66, 218, 1, 1] #message = "Hello"	
#status = lora.send_to_wait(message, 10, retries=2)
#lora.close()    


