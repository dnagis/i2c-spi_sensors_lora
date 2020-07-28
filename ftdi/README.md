## FTDI 2232HL = les gros dongles violets

install en focus juillet 2020:


libusb https://github.com/libusb/libusb/releases/download/v1.0.23/libusb-1.0.23.tar.bz2  --prefix=/usr
pip install pyftdi


--> seule libusb est nécessaire pour que pyftdi fonctionne!
	https://eblot.github.io/pyftdi/requirements.html

/usr/lib/python3.8/site-packages/pyftdi
installe automatiquement des tools dans la PATH dont un pour scanner les devices
/usr/bin/ftdi_urls.py i2cscan.py ... la doc: https://eblot.github.io/pyftdi/tools.html


#doc pyftdi:
https://eblot.github.io/pyftdi/index.html
https://eblot.github.io/pyftdi/urlscheme.html --> accéder au device












libftdi1 https://www.intra2net.com/en/developer/libftdi/download/libftdi1-1.5.tar.bz2
cmake -DCMAKE_INSTALL_PREFIX=/usr -DFTDI_EEPROM=OFF -DEXAMPLES=OFF -DLINK_PYTHON_LIBRARY=ON -DSTATICLIBS=OFF ../



