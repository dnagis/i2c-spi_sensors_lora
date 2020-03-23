# i2c 
"I squared C"


## pigpio: python pour le rpi: utilisée initialement pour les bmp280 (voir à côté bmp280.py)
	lancer pigpiod, astuce: ifconfig lo 127.0.0.1 sinon pigpio.py -- socket.create_connection((localhost, 8888), None) -- plante (hang longtemps+++)
	
## pyftdi
	c''est du python3 MAIS c''est bien documenté
	pip install pyftdi (je suppose qu'il faut que les librairies mpsse et ftdi soient installées)
	
	**ATTENTION** pour i2c sur FT2232H il faut connecter AD1 et AD2 ensembles et au SDA du slave 
		(https://eblot.github.io/pyftdi/api/i2c.html#i2c-wiring et https://eblot.github.io/pyftdi/pinout.html)	
	
	i2cscan.py équivalent de i2cdetect est ici:
		https://github.com/eblot/pyftdi/tree/master/pyftdi/bin





	
# lis3mdl (magnetometer pour compass boussole) ***en cours***
https://www.st.com/resource/en/datasheet/lis3mdl.pdf 
VDD pour 3v3 (pas VIN)
pin "SDA"=DATA, le pin "SDO" permet de changer d'adresse si on le connecte au GND (DS page 17). Je suppose pour avoir 2 puces sur
	le même bus?

LIS3MDL_SA1_HIGH_ADDRESS   0011110 ->0x1E
LIS3MDL_SA1_LOW_ADDRESS    0011100 ->0x1C

librairies
* arduino:
https://github.com/pololu/lis3mdl-arduino
* adafruit:
https://github.com/adafruit/Adafruit_CircuitPython_LIS3MDL/blob/master/adafruit_lis3mdl.py



bin->dec 		bc <<< "ibase=2;obase=A;100"		-> 4
bin->hex		bc <<< "ibase=2;obase=10000;1011"	-> B
hex->bin		bc <<< "obase=2;ibase=16;1E" -> 11110


# espoirs de compass:
https://github.com/adafruit/Adafruit_CircuitPython_LIS3MDL/blob/master/examples/lis3mdl_compass.py
https://github.com/tkurbad/mipSIE/blob/master/python/AltIMU-10v5/lis3mdl.py
https://github.com/pololu/lis3mdl-arduino/issues/3 --> float Heading = 180*atan2( mag.m.y, mag.m.z)/PI;
