/**
 * sources avec git dans ks:/home/temperature/i2c/bmp280
 * i2c direct écriture / lecture dans les registers, sur le rpi
 * 
 * BMP280 datasheet pour les registers et le fonctionnement
 * 
 * Basé sur i2c-tools-4.0 --> en particulier tools/ 
 * copier les .o que tu veux (i2cbusses.o) dans le même dir pour bénéficier de leurs fonctions, et les .h...
 * 
 * *****compilation:*****
 * export PATH=/initrd/mnt/dev_save/cross/bin:$PATH
 * arm-linux-gnueabihf-gcc i2cbusses.o -o i2c_vvnx i2c_vvnx.c -li2c
 * 
 * Le script python qui m'a sauvé: 
 * https://www.raspberrypi.org/forums/viewtopic.php?t=147350
 * Basé sur pigpio (attention il faut ifconfig lo 127.0.0.1 pour accès pigpiod, et changer dans 
 * def __init__ --> address=0x77)
 * 
 * 
 * exemple avec tools/i2cget: # i2cget 1 0x77 0x89
 * 
 * 
 * 
 */
#include <stdio.h>
#include <stdint.h>
#include <sys/ioctl.h>

#include <stdlib.h>
#include <linux/i2c.h>
#include <linux/i2c-dev.h>
#include "i2cbusses.h"
#include <i2c/smbus.h>

int32_t t_fine;

//https://www.raspberrypi.org/forums/viewtopic.php?t=147350
int conversion_temp(int t_msb, int t_lsb, int t_xlsb) {
	uint16_t dig_T1;
	int16_t  dig_T2;
	int16_t  dig_T3;	
	int32_t adc_T; //Analog to Digital Converter temp 
	int32_t var1, var2, t_final;
	
	adc_T = (t_msb << 12) + (t_lsb << 4) + (t_xlsb >> 4);
	
	//fixes, à récupérer avec i2cget -y 1 0x77 0x88... tableau page 21 de la datasheet
	dig_T1 = 0xec + (0x6b << 8); //LSB + (MSB << 8);
	dig_T2 = 0x66 + (0x64 << 8); 
	dig_T3 = 0x32 + (0x00 << 8); 

	
	var1  = ((((adc_T >> 3) - (dig_T1 << 1)) * dig_T2)) >> 11;	
	var2  = ((((adc_T >> 4) - dig_T1) * ((adc_T >> 4) - dig_T1)) >> 12) *  dig_T3 >> 14;
	
	t_fine = var1 + var2;
	
	
	t_final  = (t_fine * 5 + 128) >> 8;
	
	return t_final;
}

int conversion_press(int p_msb, int p_lsb, int p_xlsb) {
	uint16_t dig_P1;
	int16_t  dig_P2, dig_P3, dig_P4, dig_P5, dig_P6, dig_P7, dig_P8, dig_P9;
	int64_t dig_P4_64, dig_P1_64, one;
	one = 1;

	int32_t	adc_P; //Analog to Digital Converter Press 
	long long int var1, var2, p_final;
	
	adc_P = (p_msb << 12) + (p_lsb << 4) + (p_xlsb >> 4);
	
	
	//fixes, à récupérer avec i2cget -y 1 0x77 0x88... tableau page 21 de la datasheet	
	dig_P1 = 0xa4 + (0x94 << 8); //LSB + (MSB << 8);
	dig_P2 = 0x68 + (0xd6 << 8); 
	dig_P3 = 0xd0 + (0x0b << 8); 
	dig_P4 = 0x90 + (0x24 << 8); 
	dig_P5 = 0xfa + (0xfe << 8); 
	dig_P6 = 0xf9 + (0xff << 8); 
	dig_P7 = 0x8c + (0x3c << 8); 
	dig_P8 = 0xf8 + (0xc6 << 8); 
	dig_P9 = 0x70 + (0x17 << 8);
	
	printf("t_fine=%i\n", t_fine);
	
	var1 = t_fine - 128000;
	var2 = var1 * var1 * dig_P6;
	var2 = var2 + ((var1*dig_P5)<<17);
	dig_P4_64 = (int64_t)dig_P4; //you cannot cast the left operand of the assignment operator in c
	var2 = var2 + ((dig_P4_64)<<35); //problème ici
	var1 = ((var1 * var1 * dig_P3)>>8) + ((var1 * dig_P2)<<12);
	var1 = (((((one)<<47)+var1))*(dig_P1))>>33; 

	if (var1 == 0)
		return 0;
	p_final = 1048576 - adc_P;
	p_final = (((p_final<<31)-var2)*3125)/var1;
	var1 = ((dig_P9) * (p_final>>13) * (p_final>>13)) >> 25;
	var2 = ((dig_P8) * p_final) >> 19;
	p_final = ((p_final + var1 + var2) >> 8) + ((dig_P7)<<4);

	return p_final / 256;
}

int main(int argc, char *argv[])
{
	char *end;
	int i2cbus, address, file, res, addr_reg, value, t_msb, t_lsb, t_xlsb, T, p_msb, p_lsb, p_xlsb, P;
	char filename[20];
	unsigned long funcs;
	
	printf("i2c a la vvnx, sources git dans ks:/home/temperature/i2c/bmp280\n");
		
	/**Ouverture du bus**/	
	i2cbus = lookup_i2c_bus("1");
	if (i2cbus < 0)
		printf("Erreur lookup_i2c_bus \n");

	address = parse_i2c_address("0x77");
	if (address < 0)
		printf("Erreur parse \n");
		
	file = open_i2c_dev(i2cbus, filename, sizeof(filename), 0); // "/dev/i2c-1"
		if (file < 0)
		printf("Erreur file \n");
		
	set_slave_addr(file, address, 0);
	
	/**Ecriture dans le register Ctrl Measure, 0x25 = 001 001 01**/
	addr_reg = strtol("0xf4", NULL, 0);
	value = strtol("0x25", NULL, 0);
	res = i2c_smbus_write_byte_data(file, addr_reg, value);
	
	if (res < 0) {
		fprintf(stderr, "Error: Write failed\n");
		close(file);
		exit(1);
	}
	
	/**Lecture F3 (status) pour savoir si on est encore en train de measure*/
	addr_reg = strtol("0xf3", NULL, 0);		
	while (1) {
		res = i2c_smbus_read_byte_data(file, addr_reg);
		printf("F3 (status) -> 0x%02x\n", res);
		if (res < 10) //bit 3 "00001000" = 8 en hexa ou int
			break;
		usleep(500000); //microsecondes
	}	
	printf("le bmp280 a fini de measurer\n");
	

	/**Récupération des valeurs dans les registers, datasheet page 24**/
	addr_reg = strtol("0xfa", NULL, 0);		
	t_msb = i2c_smbus_read_byte_data(file, addr_reg);	
	addr_reg = strtol("0xfb", NULL, 0);		
	t_lsb = i2c_smbus_read_byte_data(file, addr_reg);
	addr_reg = strtol("0xfc", NULL, 0);		
	t_xlsb = i2c_smbus_read_byte_data(file, addr_reg);
	addr_reg = strtol("0xf7", NULL, 0);		
	p_msb = i2c_smbus_read_byte_data(file, addr_reg);	
	addr_reg = strtol("0xf8", NULL, 0);		
	p_lsb = i2c_smbus_read_byte_data(file, addr_reg);
	addr_reg = strtol("0xf9", NULL, 0);		
	p_xlsb = i2c_smbus_read_byte_data(file, addr_reg);
		
	T = conversion_temp(t_msb, t_lsb, t_xlsb);
	P = conversion_press(p_msb, p_lsb, p_xlsb);
		
	printf("Temperature = %i\n", T); 
	printf("Pression = %i\n", P); //à diviser par 100 pour avoir des hPa
    close(file);	

}
