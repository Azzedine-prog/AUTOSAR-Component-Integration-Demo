#include "Rte.h"

#define SENSOR_SCALE_FACTOR 0.1f

static float sample_raw_temperature(void)
{
    static float simulated_adc_count = 250.0f;

    simulated_adc_count += 5.0f;
    if (simulated_adc_count > 600.0f)
    {
        simulated_adc_count = 250.0f;
    }

    return simulated_adc_count;
}

void SWC_Sensor_Run(void)
{
    float adc_value = sample_raw_temperature();
    float temperature_celsius = adc_value * SENSOR_SCALE_FACTOR;

    Rte_Write_Sensor_Temperature(temperature_celsius);
}
