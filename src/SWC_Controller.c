#include "Rte.h"

#define OVERHEAT_THRESHOLD_C 50.0f

static bool overheat_flag = false;

bool SWC_Controller_GetFlag(void)
{
    return overheat_flag;
}

void SWC_Controller_Run(void)
{
    float temperature_celsius = 0.0f;
    if (!Rte_Read_Controller_Temperature(&temperature_celsius))
    {
        return;
    }

    overheat_flag = (temperature_celsius > OVERHEAT_THRESHOLD_C);
    Rte_Write_Controller_OverheatFlag(overheat_flag);
}
