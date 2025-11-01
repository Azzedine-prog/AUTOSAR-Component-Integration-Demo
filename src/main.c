#include <stdbool.h>
#include <stdio.h>
#include "Rte.h"
#include "SWC_Sensor.h"
#include "SWC_Controller.h"

int main(void)
{
    Rte_Init();

    for (int i = 0; i < 5; ++i)
    {
        SWC_Sensor_Run();
        SWC_Controller_Run();

        float temperature = 0.0f;
        bool flag = false;
        Rte_Read_Controller_Temperature(&temperature);
        Rte_Read_Controller_OverheatFlag(&flag);

        printf("Cycle %d: Temp = %.2f C, Overheat flag = %s\n", i, temperature, flag ? "ON" : "OFF");
    }

    return 0;
}
