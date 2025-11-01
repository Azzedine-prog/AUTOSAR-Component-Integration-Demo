#ifndef RTE_H
#define RTE_H

#include <stdbool.h>

typedef struct
{
    float temperature_celsius;
} Rte_SensorSignalsType;

typedef struct
{
    bool overheat_flag;
} Rte_ControllerSignalsType;

void Rte_Init(void);

void Rte_Write_Sensor_Temperature(float temperature_celsius);

bool Rte_Read_Controller_Temperature(float *temperature_celsius);

void Rte_Write_Controller_OverheatFlag(bool flag);

bool Rte_Read_Controller_OverheatFlag(bool *flag);

#endif /* RTE_H */
