#include <stdio.h>
#include "pico/stdlib.h"
#include "lib/OLED/OLED_2in23.h"
#include "lib/Config/DEV_Config.h"
#include "lib/UPS/Pico_UPS.h"



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
    getPercent();

    OLED_2in23_draw_point(1,5,1);
    OLED_2in23_draw_point(1,6,1);
    OLED_2in23_refresh_gram();  
    OLED_2in23_draw_point(5,1,1);
    OLED_2in23_refresh_gram();
    


    while (true){
        int pct=(int)(getPercent());
        OLED_2in23_draw_point(pct,1,1);
        OLED_2in23_draw_point(1,1,1);
        OLED_2in23_refresh_gram(); 
        gpio_put(LED_PIN,1);
        sleep_ms(300);
        OLED_2in23_draw_point(1,1,0);
        OLED_2in23_draw_point(pct,1,0);
        OLED_2in23_refresh_gram(); 
        gpio_put(LED_PIN,0);
        sleep_ms(300);
    }
    return 0;
}
