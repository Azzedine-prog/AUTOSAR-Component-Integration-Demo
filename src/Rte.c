#include <stddef.h>
#include "Rte.h"

static Rte_SensorSignalsType sensor_signals;
static Rte_ControllerSignalsType controller_signals;

void Rte_Init(void)
{
    sensor_signals.temperature_celsius = 0.0f;
    controller_signals.overheat_flag = false;
}

void Rte_Write_Sensor_Temperature(float temperature_celsius)
{
    sensor_signals.temperature_celsius = temperature_celsius;
}

bool Rte_Read_Controller_Temperature(float *temperature_celsius)
{
    if (temperature_celsius == NULL)
    {
        return false;
    }

    *temperature_celsius = sensor_signals.temperature_celsius;
    return true;
}

void Rte_Write_Controller_OverheatFlag(bool flag)
{
    controller_signals.overheat_flag = flag;
}

bool Rte_Read_Controller_OverheatFlag(bool *flag)
{
    if (flag == NULL)
    {
        return false;
    }

    *flag = controller_signals.overheat_flag;
    return true;
}
