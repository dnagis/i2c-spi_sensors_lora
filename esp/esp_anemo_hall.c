/*
 * Anémo 2020
 * 
 * Lecture built-in hall sensor
 * https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/adc.html
 * 
 * */


#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "driver/adc.h"


void app_main(void)
{
    
    //adc1_config_width(ADC_WIDTH_BIT_12);
    
    while (1) {
		int hall = hall_sensor_read();
        printf("hall: %i\n", hall);
        vTaskDelay(100 / portTICK_PERIOD_MS);
    }
}
