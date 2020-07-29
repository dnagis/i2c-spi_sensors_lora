### FTDI 2232H = (gros breakout violet) pour avoir du pinout en USB donc sur un ordi

## datasheet
FTDI 2232HL https://www.ftdichip.com/Support/Documents/DataSheets/ICs/DS_FT2232H.pdf

update librairies focus juillet 2020:

## pyftdi (i²c et spi)
pip install pyftdi

--> seule dep de pyftdi = libusb (https://eblot.github.io/pyftdi/requirements.html)! je l'ai installée dans core.sfs	

pip install pyftdi
--> installe automatiquement des tools dans la PATH dont un pour scanner les devices: /usr/bin/ftdi_urls.py 
/usr/bin/ftdi_urls.py i2cscan.py ... la doc: https://eblot.github.io/pyftdi/tools.html


# doc pyftdi:
https://eblot.github.io/pyftdi/index.html
https://eblot.github.io/pyftdi/urlscheme.html --> accéder au device

# pinouts pyftdi: 
**ATTENTION PINOUT PYFTDI** pour i²c sur FT2232H il faut connecter AD1 et AD2 ensembles (https://eblot.github.io/pyftdi/pinout.html)
p.9 de la datasheet: DS_FT2232H.pdf correspondance A[D;C]BUS[0;7] et B[D;C]BUS[0;7] (inscriptions dongle) et MPSSE



***Les librairies libftdi1 et libmpsse***
Si je comprends bien elles servent à parler au dongle en C, en C++, en python... 
Elles ne sont pas nécessaires au fonctionnement de pyftdi


## libftdi1 https://www.intra2net.com/en/developer/libftdi/download/libftdi1-1.5.tar.bz2
cmake -DCMAKE_INSTALL_PREFIX=/usr -DFTDI_EEPROM=OFF -DEXAMPLES=OFF -DLINK_PYTHON_LIBRARY=ON -DSTATICLIBS=OFF ../
re-compilée en focus, mais pas testée

## libmpsse-1.3 (pour SPI)
pas re-compilée en focus: je laisse ici les notes d'avant:
	il faut être en python2 pas 3
	CFLAGS=-I/usr/include/libftdi1 ./configure --prefix=/usr --libdir=/usr/lib64
	builder les exemples dans libmpsse: CFLAGS=-I/usr/include/libftdi1 CC=gcc make

	

















