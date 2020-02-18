#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "lora.h"

uint8_t buf[32];
char string2send[20];
int i = 0;

void task_tx(void *p)
{
   printf("task_tx avant boucle\n");
   for(;;) {
      vTaskDelay(5000 / portTICK_PERIOD_MS);
	  i++;	
      sprintf(string2send, "vvnx %d", i);
      
      
      //lora_send_packet((uint8_t*)"hello_vvnx_au_thor", 18);
      
      lora_send_packet((uint8_t*)string2send, 20);
      
      
      printf("packet sent: %s\n", string2send);
   }
}

void task_rx(void *p)
{
   int x;
   for(;;) {
      lora_receive();    // put into receive mode
      while(lora_received()) {
         x = lora_receive_packet(buf, sizeof(buf));
         buf[x] = 0;
         printf("Received: %s\n", buf);
         lora_receive();
      }
      vTaskDelay(1);
   }
}

void app_main()
{
   printf("Démarrage...\n");
   lora_init();
   lora_set_frequency(868e6);
   lora_enable_crc();
   xTaskCreate(&task_tx, "task_tx", 2048, NULL, 5, NULL);
}
