/*
 * Anémo 2020
 * 
 * Lecture built-in hall sensor
 * https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/adc.html
 * 
 * visualisation gnuplot: printf("%i\n", hall); en monitor: ctrl-T + ctrl-L (log to file)
 * puis gnuplot> plot 'log.anemo.20200910095412.txt'
 * 
 * 
 * 
 * 
 * 
 * */


#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "driver/adc.h"

int tours;
#define THRESHOLD     85



static void task_time_counter(void* arg)
{
    while (1) {
        vTaskDelay(5000 / portTICK_PERIOD_MS);
        printf("tours = %i\n", tours);
        tours = 0;
    }
}



static void task_hall(void* arg)
{
	bool sup_thrshld = false;
	
	
    while (1) {
		int hall = hall_sensor_read();
		//printf("hall:%i tours:%i\n", hall, tours);
		
		//on ne count++ que si on on passe au dessus du seuil puis en dessous
		if(hall > THRESHOLD) {
			//printf("debug: hall > THRESHOLD\n");
			sup_thrshld = true;
		} else {
			if (sup_thrshld) {
					//printf("debug: dans if (sup_threshld)\n");
					tours++;
					sup_thrshld = false;
				}
		}
		
        
        vTaskDelay(10 / portTICK_PERIOD_MS);
    }
}


void app_main(void)
{
    tours = 0;
    //adc1_config_width(ADC_WIDTH_BIT_12);
    
    xTaskCreate(task_hall, "task_hall", 2048, NULL, 10, NULL);
    xTaskCreate(task_time_counter, "task_time_counter", 2048, NULL, 10, NULL);
    

}
