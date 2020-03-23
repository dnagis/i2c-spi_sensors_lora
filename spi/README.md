# SPI (Lora, mcp3008, ...) 

NSS = Chip select



## MCP3008 (essentiellement pour tests)
connextion FTDI 2232 - MCP3008:
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

PCB easyEDA de décembre 2019 pour RFM95

Première commande: 2019 (Kloug's) chez Aliexpress -> Semtech SX1276/77/78/79 based boards + breakout boards LoRa chez Tindie (cf projet partagé klougien sur gitlab "LORA - Node to Node")

Soudure
1) module 2) antenne 3) pinouts
RFM95 -> si les castellated vias merdés à la pâte, possible de faire au fer à souder classique: réussi au moins une fois en janvier 2020 (j'avais pas le pistolet à air chaud encore)
Connecteurs d'antennes: flux + mini boule au bout de la panne à appliquer direct avec la panne (pas l'étaim direct).




## Lora SX1276 - FT2232H
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

## Lora SX1276 - esp32 
https://github.com/Inteform/esp32-lora-library (pas évident d'adapter librairies arduino sur esp32)
	builder dans le dir cloné, après avoir ajouté le dir main/ de hello-world, et juste changer le nom du .c et adapter CMakeLists.txt
	ou
	cp -af esp32-lora-library/components/lora $ESP-IDF/components/  (tu peux aussi le copier dans ton projet/components je crois)
	les codes pour Tx/Rx sont dans leur README.md

Connexions: *********ATTENTION PINS ESP32 ET LORA: RISQUE DE MOMENTS DE SOLITUDE+++++***********
config numéros GPIO ça se fait en menuconfig (dans components/lora) 
Le PCB que je design mars 2020 donne en menuconfig
	(32) CS GPIO 
	(32) RST GPIO
	(25) MISO GPIO
	(26) MOSI GPIO
	(33) SCK GPIO

possibilités (ce qui a marché au moins une fois en pins sur l'esp32 pour éviter les moments de solitude): 

RFM95		NSS	SCK	MI	MO RST //pas obligatoire

esp32		32	33	21	19
esp32(alt)	23	22	21	19
esp32(alt)	32	33	27	14
esp32(alt)	25	26	27	14 
esp32(alt)	32	33	25	26

oublier 34 et 35 sur l'esp pour SPI, que ce soit pour NSS SCK, MI ou MO
RST à 1 donne un comportement très misleading: bloquage dans le bootup causé par lora_init() et on ne voit même pas un printf() avant!



RST pas obligatoire pour Lora pour fonctionnement de base avec l'esp32.


## Lora SX1276 - rpi 
https://gitlab.com/the-plant/raspi-lora -> NB je n'ai pas à bricoler dans la librairie!
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
BCM17 (arg n°2 de Lora())			D0	#Attention il **faut** le mettre pour le rpi (alors qu'esp32 pas obligatoire). Je suppose que c'est un interrupt




## moments de solitude
J'ai déjà eu des non fonctionnements qui ont été résolu peu de temps après que je modifie la fréquence (915 -> 868, et vice et versa) sur l'émetteur et sur le 
récepteur, sans que je comprenne pourquoi

#ToDo lora
-Demystifier pourquoi des fois dans un nouveau système (une nouvelle install) ça marche pas out of the box: pquoi des fois bricolage de la fréquence fait
	fonctionner...
-Garder les tarball libftdi et libmpsse qq part sur kimsufi ils sont précieux +++
-Essais real life: 

Il faut recommencer à l'arbre mort: quand ça n'a pas marché à l'arbre mort, l'antenne était à l'intérieur, et en rentrant ça marchait pas non plus. J'avais pas encore de manière de visualiser sur le 
tel les dernieres réceptions en direct

au carré mer par contre ça passait pas alors qu'en rentrant ça passait. Antenne à l'exterieur, mais archi mal positionnée.


Mon système: un script sur le XPS13 qui scp la db, requete les 10 dernieres lignes -> fichier txt -> upload vers kimsufi:
while true
do
	scp pal:/root/lora.db .
	sqlite3 lora.db "select payload, datetime(epoch, 'unixepoch','localtime') from data order by epoch desc limit 10" > log_lora.txt
	scp log_lora.txt ks:/var/www/fileserver/public/perso/
	sleep 60
done

	

