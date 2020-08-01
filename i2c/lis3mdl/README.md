## lis3mdl

# Keywords: Compass Bearing

# pinouts
	Alim 3v3 = pin "VDD" (pas VIN)
	pin "SDA"=DATA (attantion voir ci dessus astuce FTDI: il faut relier SDA à D1 ET D2))
	pin "SDO" permet de changer d'adresse si on le connecte au GND (DS page 17). Je suppose pour avoir 2 puces sur le même bus?
	LIS3MDL_SA1_HIGH_ADDRESS   0011110 ->0x1E
	LIS3MDL_SA1_LOW_ADDRESS    0011100 ->0x1C

# scripts python lis3mdl:
	rpi_smbus2.py -> rpi -> librairie smbus2
	i2c_pyftdi_lis3mdl.py -> FT2232H -> librairie pyftdi
	rpi_pigpio.py -> rpi -> librairie pigpio (j'aimerais laisser tomber: il faut un daemon qui tourne)	
	 
# Des valeurs X Y jusqu'au heading/bearing

-La datasheet page 14 et le diagramme au verso du PCB donnent les orientations des Axes X - Y - Z par rapport au chipset.
-Les valeurs X et Y (récupérées dans les registers OUT_[X,Y]_[L,H] 28h, 29h, 2Ah, 2Bh) donnent les coordonnées d'un vecteur: celui du champ magnétique mesuré
 (hopefully le champ magnétique terrestre), dans ce système de coordonnées de la puce.

Ce qui explique: que quand la face avec les pinouts (axe Y) est orientée vers le nord => Y est à son maximum, X est à 0

-Pour avoir un angle à partir de X et Y:
math.atan2(y, x) en python donne un résultat en coordonnées polaires, en radians compris entre -pi et +pi qu'on va appeler theta. atan2 peut donner le quadrant car il a le signe
pour récupérer les degrés à partir de theta: math.degrees(theta)

math.atan2(1, 1) -> 0.7853981633974483 et math.degrees(0.7853981633974483) -> 45.0 #juste pour ta culture personnelle

-De l'angle au Heading/Bearing: 
degrees(atan2(y, x)) te donne l'angle du vecteur champ magnétique dans le système d'axe du chipset. C'est bien tu veux probablement plutôt avoir la direction vers laquelle pointe par exemple
l'axe Y du chipset. Donc il faut transformer. Là c'est facile il faut juste négativer, donc -(degrees(atan2(y, x))).
La final touch c'est si tu ne veux pas avoir un heading -180 -> +180, alors là tu ajoutes 360 lorsque c'est neg if angle < 0: angle += 360


