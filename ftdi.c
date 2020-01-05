#include <unistd.h>
#include <stdio.h>
#include <ftdi.h>

#define LED 0x08  /* CTS (brown wire on FTDI cable) */

int main()
{
    unsigned char c = 0;
    int i;
    struct ftdi_context *ftdi;

    /* Initialize context for subsequent function calls */
    ftdi = ftdi_new();

    /* Open FTDI device based on FT232R vendor & product IDs */
    if(ftdi_usb_open(ftdi, 0x0403, 0x6001) < 0) {
        puts("Can't open device");
        return 1;
    }

    /* Enable bitbang mode with a single output line */
    //ftdi_enable_bitbang(&ftdic, LED);
    
    printf("enabling bitbang mode\n");
    ftdi_set_bitmode(ftdi, LED, BITMODE_BITBANG);

    /* Endless loop: invert LED state, write output, pause 1 second */
    for(i = 0; i < 10; i++) {
        printf("passage n° %i\n", i);
        c ^= LED;
        ftdi_write_data(ftdi, &c, 1);
        sleep(1);
    }
    
    printf("disabling bitbang mode\n");
    ftdi_disable_bitbang(ftdi);
    
    
    ftdi_usb_close(ftdi);
	done:
    ftdi_free(ftdi);
}
