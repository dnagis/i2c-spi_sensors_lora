# SPI (Lora, mcp3008, ...) 

* Disambiguation:
NSS = Chip select = CE(0/1) sur le rpi ("Chip Enable")

## Scripts:
NUC : utiliser lora_pyftdi.py (mpsse je trouve l'api moins documentée)
Rpi : utiliser rpi_lora_spidev.py (raspi-lora utilise interrupt et me cache la communication avec les registers)

pyftdi sur le NUC et spidev sur le Rpi -> homogénéité


## MCP3008 (essentiellement pour tester le SPI avec qq chose de simple)
connexion FTDI 2232 - MCP3008:
AD1 (TDI/DO = OUTPUT cf p.14 de la DS) sur DIN du mcp3008
AD2 (TDO/DI) sur DOUT du mcp3008
AD3 (CS) et AD0 (CLK) pas de pb
****Ne pas oublier d alimenter le mcp3008!!!!****


## Lora puces semtech
	"LoRa" je crois stands for "Long Range" (datasheet semtech p 35)

### Fréquence France
	868MHz
	
### Datasheet
https://www.semtech.com/products/wireless-rf/lora-transceivers/sx1276 -> @ datasheet

### Hardware
Ne jamais alimenter un module LoRa qui n'a pas d'antenne branchée
Ne pas oublier d'alimenter le module LoRa SX1276 en 3v3! 

Commandes: Aliexpress (11-19, ...)
	RFM95 RFM95W 868 915 RFM95-868MHz RFM95-915MHz LoRa SX1276 (A l'arrière: 868Mhz coché) -> Choisir 868MHz (France)
	Connecteur antenne: SMA connecteur Jack femelle pour 1.6mm bord de soudure PCB montage droit plaqué or connecteurs RF prise de soudure
	Antennes: 5 pièces/lot mini caoutchouc 868 MHz antennes, antenne 868 MHz ISM Terminal SMA (M)

Première commande: 2019 (Kloug's) chez Aliexpress -> Semtech SX1276/77/78/79 based boards + breakout boards LoRa chez Tindie (cf projet partagé klougien sur gitlab "LORA - Node to Node")

Soudure update 2020
RFM95 -> direct fer classique, pas la peine de se faire chier à la pâte à souder

## moments de solitude
J'ai déjà eu des non fonctionnements  de SX1276 qui ont été résolu peu de temps après que je modifie la fréquence (915 -> 868, et vice et versa) sur l'émetteur et sur le 
récepteur, sans que je comprenne pourquoi. J'avais noté ça à Palavas, je confirme à Arles à la reprise en juillet 2020, un module monté sur un PCB Tindie m'a fait le coup. Un de mes PCB en Rx sur le rpi fonctionnait
sans pb, mais pour le Tindie en Tx sur l'esp32 il a fallu que je passe fréquence à 915, puis revenir à 868.


## Lora SX1276 - FTDI breakout violet FT2232H
en python, sur un ordi en USB
lora_pyftdi -> Python3 j'essaie de passer à ça: la doc est plus explicite que mpsse
lora_mpsse.py -> Python2

NB pas d interrupts (car la puce FTDI ne le supporte pas contrairement à GPIO sur le rpi) donc 4 connexions SPI + l'alim

connexions: 
RFM95			FT2232H (voir dataSheet FT2232H pp 9 et 14 - pour l'histoire output/input)

SCK				AD0
MO  			AD1 = OUTPUT (TDI/DO) 
MI 				AD2 = INPUT (TDO/DI)
CS/NSS 			AD3




## Lora SX1276 - rpi 
-rpi_lora_spidev
	on parle direct aux registers via spidev, comme avec pyftdi. Pas d'interrupts (donc pin D0 inutile) -> lecture de flags dans un loop. 
	on voit ce qui se passe. du code bio.


-raspi-lora https://gitlab.com/the-plant/raspi-lora
	utilisé initialement. 
	raspi-lora utilise Rpi.GPIO pour recevoir un interrupt (D0 sur SX1276), et spidev pour parler à la puce en spi
	NB je n'ai pas à bricoler dans la librairie!
deps:
	python2 (ils disent python3 only mais pas vrai...)
	modprobe spidev + spi-bcm2835 ( --> /dev/spidev0.0  /dev/spidev0.1)
	librairies python spidev et RPi.GPIO -> un peu chiant (libpython2.7) voir rpi->python
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
BCM17 (arg n°2 de lora())			D0	#Attention il **faut** le mettre pour raspi-lora: c'est comme ça que le Rx est triggered (une LED sur D0 s'allume au Rx)





## Lora SX1276 - esp32 
https://github.com/Inteform/esp32-lora-library (pas évident d'adapter librairies arduino sur esp32)
	cp -af esp32-lora-library/components/lora $ESP-IDF/components/  (tu peux aussi le copier dans ton projet/components je crois)
	les codes pour Tx/Rx sont dans leur README.md
	
Pour lora + gatt pas de difficulté particulière prendre bluetooth/bluedroid/ble/gatt_server, ajouter le dir components/ de lora  
	initialisation (int(), set_frequ(), crc,) ->
		pour l'envoi, par exemple dans ESP_GATTS_WRITE_EVT:
	lora_send_packet(param->write.value, param->write.len);

Connexions: *********ATTENTION PINS ESP32 ET LORA: RISQUE DE MOMENTS DE SOLITUDE+++++***********
config numéros GPIO ça se fait en menuconfig (dans components/lora) 
Le PCB que je design mars 2020 donne en menuconfig
	(32) CS GPIO 
	(32) RST GPIO
	(25) MISO GPIO
	(26) MOSI GPIO
	(33) SCK GPIO

possibilités (ce qui a marché au moins une fois en pins sur l'esp32 pour éviter les moments de solitude): 

RFM95			NSS	SCK	MI	MO	(NB RST pas obligatoire)

config_esp_1	32	33	25	26	vérifié mars 2020
config_esp_2	32	33	21	19	
config_esp_3	23	22	21	19
config_esp_4	32	33	27	14
config_esp_5	25	26	27	14 


oublier 34 et 35 sur l'esp pour SPI, que ce soit pour NSS SCK, MI ou MO

RST à 1 donne un comportement très misleading: bloquage dans le bootup causé par lora_init() et on ne voit même pas un printf() avant!

RST pas obligatoire pour Lora pour fonctionnement de base avec l'esp32.







