# Spi Lora mcp3008 FT2232H 

NSS = Chip select

# Datasheets
FTDI 2232HL https://www.ftdichip.com/Support/Documents/DataSheets/ICs/DS_FT2232H.pdf
semtech module Lora https://www.semtech.com/products/wireless-rf/lora-transceivers/sx1276 -> @ datasheet


# FTDI puce FT2232 (gros breakout violet)
## librairies pour faire fonctionner en USB (donc sur le NUC)
libusb (1.0.22 --prefix=/usr --libdir=/usr/lib64)
libftdi1-1.4 (cmake)
	(pour builder les exples --mais je retrouve pas le gpio, autant le faire avec libmpsse--: gcc -o vvnx -I/usr/include/libftdi1 -lftdi1 vvnx.c)
libmpsse-1.3 (pour SPI). 
	des prereqs en commun avec mon tarball GEO (swig / pcre / ...) donc untar GEO
	CFLAGS=-I/usr/include/libftdi1 ./configure --prefix=/usr --libdir=/usr/lib64
	builder les exemples dans libmpsse: CFLAGS=-I/usr/include/libftdi1 CC=gcc make



## pinouts: p.9 DS_FT2232H.pdf correspondance A[D;C]BUS[0;7] et B[D;C]BUS[0;7] (inscriptions dongle) et MPSSE
###MCP3008:
AD1 (TDI/DO = OUTPUT cf p.14 de la DS) sur DIN du mcp3008
AD2 (TDO/DI) sur DOUT du mcp3008
AD3 (CS) et AD0 (CLK) pas de pb
****Ne pas oublier d alimenter le mcp3008!!!!****

# Lora puces semtech 

Première commande: RFM95W achetés en 2019 (Kloug's) chez Aliexpress -> Semtech SX1276/77/78/79 based boards. Puces reçues: A l'arrière: 868Mhz coché. Et RFM95 coché
Les breakout boards LoRa chez Tindie, reste à commander les supports d'antenne, l'antenne dépend de la fréquence (attention à l'achat)
voir le projet partagé klougien sur gitlab "LORA - Node to Node"

Soudure des supports d'antennes (envoyées par Larry) -> j'ai merdé la première, la deuxième nickel. Technique: 1) Prochaine fois souder les picots sur la breakout APRES avoir soudé l'antenne, 
2) flux à l'extrémité des picots cuivre 3) mini boule au bout de la panne à appliquer direct avec la panne (pas l'étaim direct) 4) pour avoir une panne préétamée au bout: la gratounette en cuivre: lui
défoncer le fion: y aller FRANCO, pas comme une tarlouze (hummmm)

##semtech - FT2232H
voir lora_mpsse.py

parler au module lora RFM95 via une puce FTDI 2232H avec la librairie mpsse
base = https://gitlab.com/the-plant/raspi-lora
cote esp32 jutilise https://github.com/Inteform/esp32-lora-library
connexions: 
RFM95			FT2232H (voir dataSheet FT2232H pp 9 et 14 - pour lhistoire output/input)

SCK				AD0
MO  			AD1 = OUTPUT (TDI/DO) 
MI 				AD2 = INPUT (TDO/DI)
CS/NSS 			AD3

NB jutilise pas d interrupts donc 4 connexions SPI + l'alim et cest tout!

##semtech - esp32 
https://github.com/Inteform/esp32-lora-library (pas évident d'adapter librairies arduino sur esp32)
cp -af esp32-lora-library/components/lora $ESP-IDF/components/  (tu peux aussi le copier dans ton projet/components je crois)
les codes pour Tx/Rx sont dans le README.md

Connexions: config GPIO ça se fait en menuconfig (dans components/lora),
esp32	RFM95
-----	-----
CS		NSS
MISO	MI
MOSI	MO
SCK		SCK
RST		RST //pas obligatoire

Ne pas oublier d'alimenter le module en 3v3! 


##rpi / python2
il faut modprobe spidev et spi-bcm2835
il faut les librairies python spidev et RPi.GPIO -> un peu chiant (libpython2.7) voir rpi->python
semtech: j'utilise le projet https://gitlab.com/the-plant/raspi-lora
-> ils disent python3 only mais pas vrai..
-> install = cp le raspi_lora/ qui contient __init__.py dans site-packages/ 
-> voir ci joint rpi_lora.py

###pinout rpi
Rpi	(pinout.xyz)					RFM95
-----								-----
BCM8 (CE0)							NSS
BCM9 (MISO)							MI
BCM10 (MOSI)						MO
BCM11 (SCLK)						SCK
BCM17 (configurable dans le code)	D0





