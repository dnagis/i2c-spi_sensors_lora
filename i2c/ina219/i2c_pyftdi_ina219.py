#!/usr/bin/python3
# -*-coding:Latin-1 -*

#INA219 -> current sensor
#https://github.com/chrisb2/pi_ina219/
#https://github.com/chrisb2/pi_ina219.git
#"PGA" = Programmable Gain Amplifier
#Le breakout violet de chez adafruit: https://cdn-learn.adafruit.com/downloads/pdf/adafruit-ina219-current-sensor-breakout.pdf
#la resistance Rshunt sur le breakout vient d'adafruit. Texas Instrument ne fabrique que l'ina219. 
#"R100" ("R" est the decimal place) sur la résistance =>  0.1 ohms. La logique: 100R = 100ohms. R est utilisé comme marqueur de decimal point (moins de risque de se
#	perdre sur un dessin industriel pendant conversion de taille de fichier). 




#ToDo
#Measure du current. Comme référence il me faut la lecture avec le multimètre. Avec la LED qui s'allume! 
#Et démystifier: est ce que l'intensité mesurée en n'importe quel
#endroit du circuit est censée être identique? Et est ce que je peux calculer l'intensité attendue? Après s'attaquer aux calculs de la calibration ina219.




from pyftdi.i2c import I2cController, I2cNackError
from binascii import hexlify
from math import trunc
import time
import sys


#2' complement pour 16 bits: si le MSB est != 0 (ligne 1) c'est une valeur négative:
# dans ce cas on renvoie val - (0xFFFF + 1) (c'est à dire 1<<16)
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








#Lecture config avant modif
data = slave.read_from(CONFIG_ADDR,2)
CONFIG = data[0] << 8 | data[1] #data[0] -> byte du haut (most significant)
print("config avant = {:08b} {:08b} ({:x})".format(data[0], data[1], CONFIG)) #pour contrôle: au reset doit être à 0x399F

#Ecriture nouvelle config
# default config: 0011100110011111 (399f)
new_config = int('0011100110011111',2).to_bytes(2,byteorder='big')
#slave.write_to(CONFIG_ADDR, b'\x00\x00') -> c'est ce format qu'il faut pour écrire dans le register
slave.write_to(CONFIG_ADDR, new_config)


#Lecture config après écriture dans le register de config
data = slave.read_from(CONFIG_ADDR,2)
CONFIG = data[0] << 8 | data[1] #data[0] -> byte du haut (most significant)
print("config apres = {:08b} {:08b} ({:x})".format(data[0], data[1], CONFIG)) #pour contrôle: au reset doit être à 0x399F





#J'ai du courant toujours à zero, normal selon DS: il faut remplir calibration register (par défaut à 0)

#Programming page calibration 5
#La map du register calibration est page 24

#max_possible_amps = shunt_volts_max / self._shunt_ohms ina219.py li 283
max_possible_amps = 32 * 10 #j'adapte. -> 32V de range
current_lsb = max_possible_amps / 32767
calibration = trunc(0.04096 / (current_lsb * 0.1)) #DS p.12 + ina219.py li 302



print("calibration= 0x{:x} decimal {:d}".format(calibration, calibration))

#int.to_bytes(length, byteorder, *, signed=False) (41).to_bytes(2, byteorder='big') #Créer un bytearray de taille 2 

cal_to_write = calibration.to_bytes(2, byteorder='big') 
print("bits calibration qu'on va ecrire: {:08b} {:08b}".format(cal_to_write[0], cal_to_write[1]))
#Ecrire la calibration dans le register
#le bit0 "is a void bit and always be 0: calibration is the value stored in FS:15:FS1 DS p 24 -> je ne sais pas comment on fait???

slave.write_to(CALIBRATION_ADDR, cal_to_write)
#time.sleep(0.5)
calib_reg = slave.read_from(CALIBRATION_ADDR,2)
CALIB_REG = calib_reg[0] << 8 | calib_reg[1]
print("calibration reg lecture = {:#010b} {:#010b} ({:x})".format(calib_reg[0], calib_reg[1], CALIB_REG)) 







#En cours!
def lire_current():
	data = slave.read_from(CURRENT_ADDR,2)
	RAW_DATA = data[0] << 8 | data[1]	
	#print("{:#010b} {:#010b}".format(data[0], data[1]))
	#sys.stdout.write("current = {:#010b} {:#010b}   \r".format( data[0], data[1]))
	RESULT = twos_comp(RAW_DATA) * current_lsb * 1000 #Datasheet p.23
	sys.stdout.write("{:.2f} \r".format(RESULT))	



#J'arrive à avoir le même output que si je place les contacteurs du multimètre aux bornes de la résistance de shunt sur le breakout
#Bien distinguer le voltage du BUS et celui du SHUNT (la resistance visible)
#Voltage Shunt: 
#avec le gain par défaut ( PGA= /8 ) c'est le cas de la figure 20 DS. p.21. Seul un bit (le MSB) contient le sign.
#j'obtiens la correspondance bits <-> voltage décrite pp.21 et tableau p. 22 en faisant un twos_complement
def lire_voltage_shunt():
	data = slave.read_from(SHUNT_VOLT_ADDR,2)
	RAW_BITS = data[0] << 8 | data[1]
	sys.stdout.write("voltage = {:016b} {:.02f}mV\r".format(RAW_BITS, twos_comp(RAW_BITS) / 100)) #Comparer à la lecture au voltmètre sur les bornes de la résistance du shunt ("R100")


#def lire_voltage_bus():	
	#Le voltage du BUS a les 3 LSB qui ne holdent pas de value:
	#	ref: DS p 12 (en bas) + p.23 et github.com/chrisb2/pi_ina219.git dans ina219.py li. 359

while(True):
	lire_current()
	#lire_voltage_shunt()
	time.sleep(0.1)
	


