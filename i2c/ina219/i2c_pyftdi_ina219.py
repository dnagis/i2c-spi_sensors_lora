#!/usr/bin/python3
# -*-coding:Latin-1 -*

#ina219
#https://github.com/chrisb2/pi_ina219/
#https://github.com/chrisb2/pi_ina219.git
#"PGA" = Programmable Gain Amplifier

from pyftdi.i2c import I2cController, I2cNackError
from binascii import hexlify
from math import trunc
import time
import sys



def twos_comp(val):
    if (val & (1 << (16 - 1))) != 0: 
        val = val - (1 << 16)        
    return val                         


CONFIG_ADDR 	 = 0x00 
SHUNT_VOLT_ADDR	 = 0x01
BUS_VOLT_ADDR 	 = 0x02 
CURRENT_ADDR 	 = 0x04 
CALIBRATION_ADDR = 0x05


#initialisation du bus, de la puce FTDI
ctrl = I2cController()
ctrl.configure('ftdi://ftdi:2232h/1')

#https://eblot.github.io/pyftdi/api/i2c.html

slave = ctrl.get_port(0x40) #l'adresse sur le bus, i2cdetect (i2c-tools) ou i2cscan.py (pyftdi) -> voir le README.md 

#http://henrysbench.capnfatz.com/henrys-bench/arduino-current-measurements/ina219-arduino-current-sensor-voltmeter-tutorial-quick-start/

data = slave.read_from(CONFIG_ADDR,2)
CONFIG = data[0] << 8 | data[1] #data[0] -> byte du haut (most significant)
print("config = {:#010b} {:#010b} ({:x})".format(data[0], data[1], CONFIG)) #pour contrôle: au reset doit être à 399f


#hex(int('0011100110011111',2)) -> 0x399f
#print(twos_comp(int('1000001100000000',2)))


#slave.write_to(CONFIG_ADDR, b'\x00\x00') -> c'est ce format qu'il faut pour écrire dans le register


#Piste calibration
#J'ai du courant toujours à zero, normal selon DS: il faut remplir calibration register
#Logique: la resistance sur le breakout vient d'adafruit. Texas Instrument ne fabrique que l'ina219. Il faut dire à l'ina
#quelle est la valeur de la résistance.
#Programming page 5
#La map du register calibration est page 24

#max_possible_amps = shunt_volts_max / self._shunt_ohms ina219.py li 283
#max_possible_amps = 32 / 100 #j'adapte. -> 32V de range
#current_lsb = max_possible_amps / 32767
#calibration = trunc(0.04096 / (current_lsb * 100)) #DS p.12 + ina219.py li 302



#ToDo calibration:
#trouver la valeur de la résistance du breakout, ma mesure??? -> je trouve 100 milli ohms
#Trouver comment écrire la calibration dans le register en prenant compte que le premier bit est à 0
#	 (DS? librairie?)

#ToDo voltage:
#lire p20-21 pour comprendre comment convertir les bits en la valeur en volt
#est ce que deux voltmètres aux mêmes noeuds d'un circuit doivent lire la même chose en même temps???



essai = int('0111110100000000',2) 
print('original:  {:016b}'.format(essai))
essai -= 1
print('-1:        {:016b}'.format(essai))
essai = ( ~essai & 0xFFFF) #obligatoire car les int en python sont signés... ~essai ne suffit pas
print('inversion: {:016b}'.format(comp))
print('int:       {:d}'.format(comp))


essai = int('7d00', 16) -> 32000
print('{:016b}'.format(essai)) -> 0111110100000000
essai -= 1
print('{:016b}'.format(essai)) -> 0111110011111111
essai = ( ~essai & 0xFFFF)
print('{:016b}'.format(essai)) -> 1000001100000000
print(essai) -> 33536 alors que j'attends 

hypothèse: si le MSB est à 0 -> juste diviser par 100 l'integer récupéré, si le MSB est à 1 faut faire manip???


#print("calibration= 0x{:x} decimal {:d}".format(calibration, calibration))

#int.to_bytes(length, byteorder, *, signed=False) (41).to_bytes(2, byteorder='big') Créer un bytearray de taille 2 

#cal_to_write = calibration.to_bytes(2, byteorder='big') 
#print("bits calibration qu'on va ecrire: {:08b} {:08b}".format(cal_to_write[0], cal_to_write[1]))
#Ecrire la calibration dans le register
#Attention le bit0 "is a void bit and always be 0: calibration is the value stored in FS:15:FS1 DS p 24

#slave.write_to(CALIBRATION_ADDR, cal_to_write)
#time.sleep(0.5)
#calib_reg = slave.read_from(CALIBRATION_ADDR,2)
#CALIB_REG = calib_reg[0] << 8 | calib_reg[1]
#print("calibration reg lecture = {:#010b} {:#010b} ({:x})".format(calib_reg[0], calib_reg[1], CALIB_REG)) 


def lire_current():
	data = slave.read_from(CURRENT_ADDR,2)
	RAW_DATA = data[0] << 8 | data[1]	
	#print("{:#010b} {:#010b}".format(data[0], data[1]))
	sys.stdout.write("current = {:#010b} {:#010b}   \r".format( data[0], data[1]))
	#RESULT = twos_comp(RAW_DATA) * .01 #LSB = 4 mv pour le bus, 10 µV pour le shunt. Datasheet p.23
	#print("{:.2f}".format(RESULT))	

def lire_voltage():
	data = slave.read_from(SHUNT_VOLT_ADDR,2)
	bits_voltage = data[0] << 8 | data[1]
	#Le voltage du BUS a les 3 LSB qui ne holdent pas de value:
	#	ref: DS p 12 (en bas) + p.23 et github.com/chrisb2/pi_ina219.git dans ina219.py li. 359
	bits_voltage = bits_voltage >> 3
	#volts = bits_voltage * 4 / 1000 --> pas si simple...
	sys.stdout.write("voltage = {:016b} \r".format(bits_voltage))
	


#while(True):
#	lire_voltage()
#	time.sleep(0.1)
	


