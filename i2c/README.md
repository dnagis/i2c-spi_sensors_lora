# i2c

## pigpio: python pour le rpi: utilisée initialement pour les bmp280 (voir à côté bmp280.py)
	lancer pigpiod, astuce: ifconfig lo 127.0.0.1 sinon pigpio.py -- socket.create_connection((localhost, 8888), None) -- plante (hang longtemps+++)
	
## pyftdi
	**ATTENTION** pour i2c sur FT2232H il faut connecter AD1 et AD2 ensembles (https://eblot.github.io/pyftdi/pinout.html)	
	
# lis3mdl (magnetometer pour compass boussole) ***en cours***

https://www.st.com/resource/en/datasheet/lis3mdl.pdf en i2c. 
https://github.com/pololu/lis3mdl-arduino/issues/3 --> float Heading = 180*atan2( mag.m.y, mag.m.z)/PI;



i2cget -y 1 0x1e 0x0f "WHO_AM_I" --> 0x3d 
bc <<< "obase=2;ibase=16;3D"
echo $((0x14))

stable en mouvement, c est du transfer quil faut faire... comme en spi
librairies
arduino:
https://github.com/pololu/lis3mdl-arduino







comment lui parler?
DS page 17 -> Slave Adress  -> moi ce serait 1e donc 0011110 donc SD0/SA pin serait connecté au voltage supply
Bon il me faut l équivalent de spidev selon ce que je vois sur la page 17.

i2c en python j ai déjà fait avec pigpio -> travail là dessus

