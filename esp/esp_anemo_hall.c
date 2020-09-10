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

int count;

static void task_time_counter(void* arg)
{
    while (1) {
        vTaskDelay(5000 / portTICK_PERIOD_MS);
        printf("count = %i\n", count);
        count = 0;
    }
}



static void task_hall(void* arg)
{
    while (1) {
		int hall = hall_sensor_read();
		if(hall>85) count++;
        //printf("%i\n", hall);
        vTaskDelay(10 / portTICK_PERIOD_MS);
    }
}


void app_main(void)
{
    count = 0;
    //adc1_config_width(ADC_WIDTH_BIT_12);
    
    xTaskCreate(task_hall, "task_hall", 2048, NULL, 10, NULL);
    xTaskCreate(task_time_counter, "task_time_counter", 2048, NULL, 10, NULL);
    

}
