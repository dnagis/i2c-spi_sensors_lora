#!/usr/bin/python3
# -*-coding:Latin-1 -*

#INA219 -> current sensor

## ToDo
#Porter sur le RPi (en attente pour savoir si ce sera en python3)



#"PGA" = Programmable Gain Amplifier
#Le breakout violet de chez adafruit: https://cdn-learn.adafruit.com/downloads/pdf/adafruit-ina219-current-sensor-breakout.pdf
#la resistance Rshunt sur le breakout vient d'adafruit. Texas Instrument ne fabrique que l'ina219. 
#"R100" sur la résistance du breakout =>  0.1 ohms. La logique: 100R = 100ohms ( R est utilisé comme marqueur de decimal point: historique = moins de risque de se
#	perdre sur un dessin industriel pendant conversion de taille de fichier). 

#Les règles à connaître absolument (pour un circuit en série - series circuit):
#	https://www.allaboutcircuits.com/textbook/direct-current/chpt-5/simple-series-circuits/
#	
#	-The amount of current in a series circuit is the same through any component in the circuit. -> la mesure de I en n'importe quel point du circuit (en série) sera la même
#	
#	-Loi d'additivité des tensions = Kirchoff's voltage law -> la somme des voltage drops par composant est nulle (alimentation et différents composants)
	
#Pour les essais: en série: une pile de 9V, une led, et une ***PETITE*** résistance (pas 4k7 -> la led ne s'allumera pas), plutôt de l'ordre de 200R (200 ohms)

#N.B. Le multimètre jaune a le fuse de 250 mA grillé très probablement: il faut lire avec le fuse 10A (borne de gauche)
#	https://github.com/chrisb2/pi_ina219.git







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


#Calibration: c'est écrit plusieurs fois dans la datasheet: tant que le register de calibration à 0 le current register restera à 0

#Le principe de la calibration (si j'ai bien compris...) c'est de permettre d'ajuster la valeur du courant si on fait des mesures de contrôle (page 13 en haut)

#Une fois la calibration entrée, le chip donne une valeur dans le register current que tu peux calculer et qui est: 
# (shunt_volt_register * calibration) / 4096  
# (la valeur du shunt_volt_register n'est pas en volts mais en µV: DS. p. 21)



#max_possible_amps = shunt_volts_max / self._shunt_ohms ina219.py li 283
#Dans les librairies et la ds je vois des chiffres énormes genre 12V ou 32V. Si je mets ça j'ai une résolution minable dans le current register. (si je mets
#32 -> max possible amps devient 320A !!! du coup la résolution s'adapte à 320A et pour atteindre des modifications significatives avec ça va falloir se lever tôt!
#donc je mets 1V vu que je m'attends plutôt à mesurer des millivolts dans mes systèmes.
max_possible_amps = 1 * 10 
current_lsb = max_possible_amps / 32767 #Pourquoi 2^15 et pas 2^16? Parce que la vraie équation devrait être range_amp(i.e. de -max_amp à +max_amp) / 2^16 
	#mais ils ont simplifié en réduisant à la valeur positive de max expected current, donc le dénominateur n'est plus la totalité des bits disponibles (2^16) mais la moitié (2^15)
calibration = trunc(0.04096 / (current_lsb * 0.1)) #DS p.12 + ina219.py li 302



print("calibration= 0x{:x} decimal {:d}".format(calibration, calibration))

#int.to_bytes(length, byteorder, *, signed=False) (41).to_bytes(2, byteorder='big') #Créer un bytearray de taille 2 

cal_to_write = calibration.to_bytes(2, byteorder='big') 
#print("bits calibration qu'on va ecrire: {:08b} {:08b}".format(cal_to_write[0], cal_to_write[1]))
#Ecrire la calibration dans le register
#le bit0 "is a void bit and always be 0: calibration is the value stored in FS:15:FS1 DS p 24 -> je ne sais pas comment on fait???

slave.write_to(CALIBRATION_ADDR, cal_to_write)
#time.sleep(0.5)
calib_reg = slave.read_from(CALIBRATION_ADDR,2)
CALIB_REG = calib_reg[0] << 8 | calib_reg[1]
print("calibration reg lecture = {:#010b} {:#010b} ({:d})".format(calib_reg[0], calib_reg[1], CALIB_REG)) #j'ai toujours un de moins, surement à cause du bit FS0 dans lequel il est impossible d'écrire 1 (ds p. 24)








def lire_current():
	lecture = slave.read_from(CURRENT_ADDR,2)
	BITS_CUR = lecture[0] << 8 | lecture[1]	
	#tu peux vérifier en regardant twos_comp(BITS_CUR) en {:2f} que une fois la calibration faite, la valeur de current register = (voltage register * calibration / 4096) (ds p. 12 équation 4)
	CURRENT = twos_comp(BITS_CUR) * current_lsb * 1000 #Datasheet p.23 et ina219. * 1000 pour avoir des mA
	sys.stdout.write(" current = {:.2f} mA (register: {:2f}) \r".format(CURRENT, twos_comp(BITS_CUR)))	



#J'arrive à avoir le même output que si je place les contacteurs du multimètre aux bornes de la résistance de shunt ("R100") sur le breakout
#Bien distinguer dans la datasheet le voltage du BUS et celui du SHUNT (la resistance visible)
#Voltage Shunt: 
#avec le gain par défaut ( PGA= /8 ) c'est le cas de la figure 20 DS. p.21. Seul un bit (le MSB) contient le sign.
#j'obtiens la correspondance bits <-> voltage décrite pp.21 et tableau p. 22 en faisant un twos_complement, et comme un LSB = 10 µV (DS. p.21)
#il faut diviser par 100 pour avoir des mV
def lire_voltage_shunt():
	data = slave.read_from(SHUNT_VOLT_ADDR,2)
	BITS_VOLTS = data[0] << 8 | data[1]	
	sys.stdout.write("voltage = {:.02f}mV".format(twos_comp(BITS_VOLTS) / 100)) #pour voir les bits: {:016b}



while(True):
	lire_voltage_shunt()
	lire_current()
	time.sleep(0.1)
	


