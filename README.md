# Interfaces serial: SPI (mcp3008, sx1276[lora], ...) et I²C (bmx280, lis3mdl, ina219, ...)


## FTDI 2232H =(gros breakout violet) pour avoir du pinout en USB donc sur un ordi

### Datasheet
FTDI 2232HL https://www.ftdichip.com/Support/Documents/DataSheets/ICs/DS_FT2232H.pdf

### librairies 
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
	
pyftdi (pour i2c, au moins)
	pip install pyftdi -> les exemples sont en python3. je pense que tout est en python3.
	**ATTENTION** pour i2c sur FT2232H il faut connecter AD1 et AD2 ensembles (https://eblot.github.io/pyftdi/pinout.html)
	les exemples: https://github.com/eblot/pyftdi dans tests/
	

### pinouts FT2232H: p.9 de la datasheet: DS_FT2232H.pdf correspondance A[D;C]BUS[0;7] et B[D;C]BUS[0;7] (inscriptions dongle) et MPSSE

