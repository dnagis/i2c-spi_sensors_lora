#!/bin/python
from raspi_lora import LoRa, ModemConfig
import time
import datetime
import signal
import sys
import sqlite3

#Rx: _handle_interrupt() -> packet est Rx ici. ajouter un self.on_recv(packet) dans le premier if des que le packet est recupere
#Tx: _spi_write() -> self.spi.xfer([register | 0x80] + payload) marche si payload = [10, 2, 1, 0, 10, 20, 30], pas si [10, 2, 1, 0, 'H', 'e', 'l', 'l', 'o']
#	error: Non-Int/Long value in arguments: 7a0315a8 -> faut faire la conversion des lettres en ascii, j'ai pas fait encore (spi.xfer([0x80] + list(bytearray(payload)))???)


db_file='/root/lora.db' #CREATE TABLE data(epoch INT, payload TEXT);

def receiveSignal(signalNumber, frame):
    print('Received:', signalNumber)
    lora.close()
    sys.exit()
    
def on_recv(payload):
    #print("message recu:" + str(bytearray(payload)) + " @ " + str(datetime.datetime.now()))
    count = payload[1] + (payload[0] << 8) #encodage dun int dans 2 bytes (anemo)
    print("recu count=" + str(count)) 
    new_data = [int(time.time()), count]
    #select payload, datetime(epoch, 'unixepoch','localtime') from data;    
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("insert into data (epoch, payload) values (?, ?);", new_data);
    conn.commit()
    conn.close()

signal.signal(signal.SIGINT, receiveSignal)

#arg2 numero du pin rpi (BCM) a connecter a D0 de la puce semtech
lora = LoRa(0, 17, 2,  freq=868, modem_config=ModemConfig.Bw125Cr45Sf128, tx_power=14, acks=True)
lora.on_recv = on_recv 
lora.set_mode_rx()

while True:
    print('Waiting...')
    time.sleep(10)
    
#Tx:    
#message = [10, 20, 30, 66, 218, 1, 1] #message = "Hello"	
#message = "Hello"
#status = lora.send_to_wait(message, 10, retries=0)
#lora.close()    


