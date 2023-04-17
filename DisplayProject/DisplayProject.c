#include <stdio.h>
#include "pico/stdlib.h"
#include "lib/OLED/OLED_2in23.h"
#include "lib/Config/DEV_Config.h"



int main()
{
    stdio_init_all();

    const uint LED_PIN = 25;
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);


    DEV_Delay_ms(20);
    if(DEV_Module_Init()!=0){
        while(1){
            printf("END\r\n");
        }
    }


    OLED_2in23_Init(); 
    // printf("OELD_test Demo\r\n");
    // if(DEV_Module_Init()!=0){
    //     while(1){
    //         printf("END\r\n");
    //     }
    // }
    // UBYTE *BlackImage;
    // OLED_2in23_draw_bitmap(0,0,&BlackImage[0],128,32); 
    // OLED_2in23_draw_point(10,10,1);
    OLED_2in23_draw_point(1,5,1);
    DEV_Delay_ms(100);
    OLED_2in23_refresh_gram();  
    OLED_2in23_draw_point(1,5,1);
    DEV_Delay_ms(1500);
    OLED_2in23_refresh_gram();  


    while (true){
        gpio_put(LED_PIN,1);
        sleep_ms(300);
        gpio_put(LED_PIN,0);
        sleep_ms(300);
    }
    return 0;
}
