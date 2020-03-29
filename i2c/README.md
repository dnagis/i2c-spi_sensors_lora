# i²c 
"I squared C"
pins en i²c: CLK SDA et l'alim


## pigpio: python pour le rpi: utilisée initialement pour les bmp280 (voir à côté bmp280.py)
	lancer pigpiod, astuce: ifconfig lo 127.0.0.1 sinon pigpio.py -- socket.create_connection((localhost, 8888), None) -- plante (hang longtemps+++)
	
## pyftdi
	c''est du python3 MAIS c''est bien documenté
	pip install pyftdi (je suppose qu'il faut que les librairies mpsse et ftdi soient installées)
	
	**ATTENTION BIG TRICK** pour i2c sur FT2232H il faut connecter AD1 et AD2 ensembles et au SDA du slave 
		(https://eblot.github.io/pyftdi/api/i2c.html#i2c-wiring et https://eblot.github.io/pyftdi/pinout.html)	
	
	i2cscan.py (équivalent de i2cdetect) est ici:
		git clone https://github.com/eblot/pyftdi.git --> dans pyftdi/bin/
		Faut parfois bricoler un peu: 
			gérer un import manquant (mais inutile: from pyftdi.misc import add_custom_devices) --> commenter
		Interprétation:
		
				# ./i2cscan.py ftdi://ftdi:2232:1:58/1
		    0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F 
		 0: .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
		 1: .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
		 2: .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
		 3: .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
		 4: X  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
		 5: .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
		 6: .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
		 7: .  .  .  .  .  .  .  .  .

			adresse = 0x40



	
# lis3mdl (magnetometer compass boussole) 

Alim 3v3 = pin "VDD" (pas VIN)
pin "SDA"=DATA (attantion voir ci dessus astuce FTDI: il faut relier SDA à D1 ET D2))
pin "SDO" permet de changer d'adresse si on le connecte au GND (DS page 17). Je suppose pour avoir 2 puces sur le même bus?
LIS3MDL_SA1_HIGH_ADDRESS   0011110 ->0x1E
LIS3MDL_SA1_LOW_ADDRESS    0011100 ->0x1C

Mes deux scripts python pour ce sensor:
	rpi_i2c_lis3mdl.py -> raspberry pi -> utilise pigpio
	i2c_pyftdi_lis3mdl.py -> ftdi -> pyftdi 


