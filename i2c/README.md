# i²c 
"I squared C"
pins en i²c: CLK SDA et l'alim

## smbus2: python3 sur le rpi, parle directement au /dev/i2c*, pas besoin de daemon qui tourne comme pigpio. ina219 et lis3mdl passés là dessus. pas le bmp280

## pigpio: python pour le pi: utilisée initialement pour les bmp280 (voir à côté bmp280.py)
	pas réinstallé en 2020 dans ma nouvelle distribution
	il faut lancer pigpiod, astuce: ifconfig lo 127.0.0.1 sinon pigpio.py -- socket.create_connection((localhost, 8888), None) -- plante (hang longtemps+++)
	
## pyftdi: gros dongles violets FT2232H en USB sur les ordis 
	install: cf. ftdi/README.md dans ce repo
	
	pinouts ftdi pour l'i²c:
	SCL <-> AD0
	SDA --> **ATTENTION BIG TRICK** pour i2c sur FT2232H il faut connecter AD1 et AD2 ensembles <-> SDA du slave 
		(https://eblot.github.io/pyftdi/api/i2c.html#i2c-wiring et https://eblot.github.io/pyftdi/pinout.html)
		
	
	/usr/bin/i2cscan.py installé automatiquement à l'install pyftdi:
		
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

Mes scripts python pour lis3mdl:
	rpi_smbus2.py -> rpi -> librairie smbus2
	rpi_pigpio.py -> rpi -> librairie pigpio (j'aimerais laisser tomber: il faut un daemon qui tourne)	
	i2c_pyftdi_lis3mdl.py -> FT2232H -> librairie pyftdi 


