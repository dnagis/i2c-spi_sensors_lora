# i²c 
"I squared C"
pins en i²c: CLK SDA et l'alim

## bash adresse de la chip et lire un register, exemple du bmp280
i2cdetect -y 1 --> busybox, montre que qq chose sur la matrice en 0x77
p.24 pdf datasheet du bmp280 --> lire le register à l'adresse 0xD0 doit retourner 0x58 -->
i2cget -y 1 0x77 0xD0 --> busybox, 0x58

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
		
	
	FTDI: /usr/bin/i2cscan.py (installé automatiquement à l'install pyftdi), sur le RPi équivalent = i2cdetect (busybox maintenant!!!)
		
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



	
# lis3mdl (magnetometer compass boussole) --> cf lis3mdl/README.md




