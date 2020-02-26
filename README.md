 # Spi Lora mcp3008 FT2232H 

NSS = Chip select
RST pas obligatoire pour fonctionnement de base
ne jamais alimenter un module LoRa qui n'a pas d'antenne branchée

# Datasheets
FTDI 2232HL https://www.ftdichip.com/Support/Documents/DataSheets/ICs/DS_FT2232H.pdf
semtech module Lora https://www.semtech.com/products/wireless-rf/lora-transceivers/sx1276 -> @ datasheet


#ToDo
-Refaire une install des modules Lora sur esp32 et FT2232H pour voir si ce README est suffisament clair
-Garder les tarball libftdi et libmpsse qq part ils sont précieux +++
	

	






# FTDI puce FT2232 (gros breakout violet)
## librairies pour faire fonctionner en USB (donc sur le NUC)
prereqs (à démystifier):
	python2 (pas de python3 sinon le configure de mpsse trouve pas les includes qu'il cherche)
	en commun avec mon tarball GEO (swig / pcre / ...) donc untar GEO

libusb (1.0.22 ./configure --prefix=/usr --libdir=/usr/lib64)
libftdi1-1.4 (cmake, juste modifier le prefix, lib64 se mets automagiquement. Il faut qu'il trouve swig
	(pour builder les exples --mais je retrouve pas le gpio, autant le faire avec libmpsse--: gcc -o vvnx -I/usr/include/libftdi1 -lftdi1 vvnx.c)
libmpsse-1.3 (pour SPI)
	il faut être en python2 pas 3
	CFLAGS=-I/usr/include/libftdi1 ./configure --prefix=/usr --libdir=/usr/lib64
	builder les exemples dans libmpsse: CFLAGS=-I/usr/include/libftdi1 CC=gcc make



## pinouts: p.9 DS_FT2232H.pdf correspondance A[D;C]BUS[0;7] et B[D;C]BUS[0;7] (inscriptions dongle) et MPSSE
### MCP3008:
AD1 (TDI/DO = OUTPUT cf p.14 de la DS) sur DIN du mcp3008
AD2 (TDO/DI) sur DOUT du mcp3008
AD3 (CS) et AD0 (CLK) pas de pb
****Ne pas oublier d alimenter le mcp3008!!!!****

# Lora puces semtech 

-Commandes: 
Aliexpress novembre 19
	RFM95 RFM95W 868 915 RFM95-868MHz RFM95-915MHz LORA SX1276 (A l'arrière: 868Mhz coché) -> Choisir 868MHz (France)
	Connecteur antenne: SMA connecteur Jack femelle pour 1.6mm bord de soudure PCB montage droit plaqué or connecteurs RF prise de soudure
	Antennes: 5 pièces/lot mini caoutchouc 868 MHz antennes, antenne 868 MHz ISM Terminal SMA (M)
PCB easyEDA de décembre 2019 pour RFM95

Première commande: 2019 (Kloug's) chez Aliexpress -> Semtech SX1276/77/78/79 based boards + breakout boards LoRa chez Tindie (cf projet partagé klougien sur gitlab "LORA - Node to Node")

-Soudure
1) module 2) antenne 3) pinouts
RFM95 -> si merdé à la pâte, possible de faire au fer à souder classique: réussi au moins une fois en janvier 2020. 
support d'antennes: flux + mini boule au bout de la panne à appliquer direct avec la panne (pas l'étaim direct) (bien passer la panne dans la gratounette pour qu'elle accroche l'étaim).


## semtech - FT2232H
voir lora_mpsse.py -> attention c'est du python2

parler au module lora RFM95 via une puce FTDI 2232H avec la librairie mpsse
base = https://gitlab.com/the-plant/raspi-lora
cote esp32 jutilise https://github.com/Inteform/esp32-lora-library

connexions: 
RFM95			FT2232H (voir dataSheet FT2232H pp 9 et 14 - pour l'histoire output/input)

SCK				AD0
MO  			AD1 = OUTPUT (TDI/DO) 
MI 				AD2 = INPUT (TDO/DI)
CS/NSS 			AD3

NB jutilise pas d interrupts donc 4 connexions SPI + l'alim et cest tout!

## semtech - esp32 
https://github.com/Inteform/esp32-lora-library (pas évident d'adapter librairies arduino sur esp32)
	cp -af esp32-lora-library/components/lora $ESP-IDF/components/  (tu peux aussi le copier dans ton projet/components je crois)
	les codes pour Tx/Rx sont dans leur README.md

Connexions:
config numéros GPIO ça se fait en menuconfig (dans components/lora):
esp32	RFM95
-----	-----
CS		NSS
MISO	MI
MOSI	MO
SCK		SCK
RST		RST //pas obligatoire

Ne pas oublier d'alimenter le module en 3v3! 


## semtech - rpi 
https://gitlab.com/the-plant/raspi-lora
python2 (ils disent python3 only mais pas vrai...)
il faut modprobe spidev et spi-bcm2835
il faut les librairies python spidev et RPi.GPIO -> un peu chiant (libpython2.7) voir rpi->python
-> install = cp le raspi_lora/ qui contient __init__.py dans site-packages/ 
-> un truc que j'ai pas eu au départ: chelou: 
 raspi_lora/lora.py ligne 57
 # set modem config (Bw125Cr45Sf128)                                                      
        self._spi_write(REG_1D_MODEM_CONFIG1, self._modem_config.value[0]) --> AttributeError: 'tuple' object has no attribute 'value
		self._spi_write(REG_1D_MODEM_CONFIG1, self._modem_config[0]) --> OK
-> code pour appeler: ci joint rpi_lora.py
-> /lib/python2.7/site-packages/raspi_lora/lora.py est là où tout se passe. nb il m'est déjà arrivé d'y bidouiller des trucs dans _spi_write() et d'oublier de les enlever

        


Connexions:
Rpi	(pinout.xyz)					RFM95
-----								-----
BCM8 (CE0)							NSS
BCM9 (MISO)							MI
BCM10 (MOSI)						MO
BCM11 (SCLK)						SCK
BCM17 (configurable dans le code)	D0	#Attention il **faut** le mettre pour le rpi (alors qu'esp32 pas obligatoire)





