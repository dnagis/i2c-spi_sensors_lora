/*
parler au MCP3008
gcc -I/usr/include/libftdi1 spi_mpsse.c -o vvnx -lmpsse
scp spi_mpsse.c ks:/home/lora/
*/
#include <stdio.h>
#include <stdlib.h>
#include <mpsse.h>
#include <unistd.h>
#include <time.h>


#define channel 1

int main(void)
{
	struct mpsse_context *monspi = NULL;
	unsigned char *data = NULL;
	int i, result;
	clock_t t;
	
	int res[1000];
	char cmd[3] = {0x01, 0x00, 0x00}; //start bit dans le premier byte, dummy byte pour recevoir config, et null pour Rx (car on va Tx)
	
	cmd[1] = 0x80 | (channel <<4); //single/diff bit et channel selection dans le byte 2
	
	monspi = MPSSE(SPI0, ONE_MHZ, MSB);	
	
	t = clock();
	
	for ( i = 0; i < 500; i++) {
		
		
		
		Start(monspi);	
		data = Transfer(monspi, cmd, sizeof(cmd));	
		//printf("byte 1 = 0x%02x\n", data[1]); //voir un des bytes	
		result = ((data[1]&3) << 8) + data[2];	
		res[i] = result;
		//printf("result ch. %i = %i\n", channel, result);			
		Stop(monspi);
		//usleep(10000);	
	}
	
	
	t = clock() - t;	
	printf("time=%f\n", ((double)t)/CLOCKS_PER_SEC);
	
	printf("juste pour rire le 453ème measurement=%i\n", res[453]); 
		
	Close(monspi);

	
	
	return 0;
}
