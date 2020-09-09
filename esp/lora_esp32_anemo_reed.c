/**Lora + readGpio (anémo)
 * 
 * anémo: brancher 3v3 et le GPIO_INPUT_IO_0 (define) 
 * 
 * 
 * 
 * 
 * 
 * 
 */

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "lora.h"

#include "driver/gpio.h"

//Lecture GPIO (anémo)
#define GPIO_INPUT_IO_0     23
#define GPIO_INPUT_IO_1     5 //on s'en sert pas, je laisse au cas où tu veuilles plusieurs GPIO, mask ci dessous, pour exple)
#define GPIO_INPUT_PIN_SEL  ((1ULL<<GPIO_INPUT_IO_0) | (1ULL<<GPIO_INPUT_IO_1))
#define ESP_INTR_FLAG_DEFAULT 0

uint8_t buf[32];
char string2send[2];
int intrpt_cnt;

//readGPIO
static xQueueHandle gpio_evt_queue = NULL;

static void IRAM_ATTR gpio_isr_handler(void* arg)
{
    uint32_t gpio_num = (uint32_t) arg;
    xQueueSendFromISR(gpio_evt_queue, &gpio_num, NULL);
}

static void gpio_task_example(void* arg)
{
    uint32_t io_num;
    for(;;) {
        if(xQueueReceive(gpio_evt_queue, &io_num, portMAX_DELAY)) {
           // ESP_LOGW(TAG, "GPIO[%d] intr, val: %d\n", io_num, gpio_get_level(io_num));
            intrpt_cnt++;
        }
    }
}

//Tx Lora
void task_tx(void *p)
{
   printf("task_tx avant boucle\n");
   for(;;) {
      vTaskDelay(20000 / portTICK_PERIOD_MS);
	  
      //sprintf(string2send, "vvnx %d", intrpt_cnt); 
      string2send[0] = (int)((intrpt_cnt >> 8) & 0xff);
      string2send[1] = (int)(intrpt_cnt & 0xff);
      
      lora_send_packet((uint8_t*)string2send, 2);      
      
      printf("count = %i, bytes sent: %02x - %02x\n", intrpt_cnt, string2send[0], string2send[1]);
      
      intrpt_cnt=0;//remise à zero du compteur
   }
}

//Rx Lora
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
   
	//GPIO: configuration 
	gpio_config_t io_conf;
	io_conf.intr_type = GPIO_PIN_INTR_POSEDGE;
	io_conf.mode = GPIO_MODE_INPUT;
	io_conf.pin_bit_mask = GPIO_INPUT_PIN_SEL;
	io_conf.pull_down_en = GPIO_PULLDOWN_ENABLE;
	io_conf.pull_up_en = GPIO_PULLUP_DISABLE;
	gpio_config(&io_conf);
	
	//GPIO: create a queue to handle gpio event from isr
	gpio_evt_queue = xQueueCreate(10, sizeof(uint32_t));
	//GPIO: start gpio task
	xTaskCreate(gpio_task_example, "gpio_task_example", 2048, NULL, 10, NULL);
	
	//GPIO: install gpio isr service
	gpio_install_isr_service(ESP_INTR_FLAG_DEFAULT);
	//GPIO: hook isr handler for specific gpio pin
	gpio_isr_handler_add(GPIO_INPUT_IO_0, gpio_isr_handler, (void*) GPIO_INPUT_IO_0);
   
	lora_init();
	lora_set_frequency(868e6);
	lora_enable_crc();
	xTaskCreate(&task_tx, "task_tx", 2048, NULL, 5, NULL);
}
