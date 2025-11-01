# Integration Steps

This demo provides a simplified AUTOSAR-like environment consisting of:

- **SWC_Sensor** – simulates an application software component that publishes a temperature signal.
- **SWC_Controller** – simulates an application software component that reads the temperature signal and toggles an overheat flag.
- **RTE (Runtime Environment)** – provides the port interface between the two SWCs through simple read/write APIs.
- **Build Automation Script** – compiles and links all C modules to produce a runnable example.

## Runtime Environment Mapping

The minimal `Rte.c` implementation models the RTE data buffers:

| Provider Component | RTE API | Consumer Component |
| ------------------ | ------- | ------------------ |
| `SWC_Sensor` | `Rte_Write_Sensor_Temperature(float temperature_celsius)` | `SWC_Controller` via `Rte_Read_Controller_Temperature(float *temperature_celsius)` |
| `SWC_Controller` | `Rte_Write_Controller_OverheatFlag(bool flag)` | External diagnostic/monitoring via `Rte_Read_Controller_OverheatFlag(bool *flag)` |

`Rte_Init` resets the backing buffers, imitating how the AUTOSAR RTE initializes internal data structures after startup.

## Software Component Behavior

1. `SWC_Sensor_Run`
   - Samples a simulated ADC count.
   - Converts the sample to degrees Celsius using a constant scale factor.
   - Publishes the temperature value to the RTE.
2. `SWC_Controller_Run`
   - Pulls the latest temperature from the RTE.
   - Compares the value against a configurable overheat threshold (50 °C).
   - Updates the RTE overheat flag to share the result with other components.

A simple `main.c` ties everything together by running both SWCs over several cycles and printing the results.

## Build and Execution

1. Ensure the required toolchain is available (the script assumes `gcc`).
2. Run the build script:

   ```bash
   ./scripts/build.py
   ```

   This compiles all C sources under `src/` with the headers in `include/` and produces `build/autosar_demo`.

3. Execute the built binary:

   ```bash
   ./build/autosar_demo
   ```

   The console output shows the temperature signal and overheat flag across several RTE cycles.

4. (Optional) Start the Tkinter dashboard for a graphical view of the same
   simulation:

   ```bash
   python3 scripts/gui_dashboard.py
   ```

   The GUI triggers the build step on demand and streams the program output
   while updating labels and a progress bar for each cycle.

## Extending the Demo

- Add more SWCs and signals to illustrate additional RTE communication patterns (sender/receiver, client/server).
- Replace the simulated ADC logic with actual hardware drivers from the AUTOSAR BSW layer.
- Introduce configuration files (e.g., AUTOSAR XML/ARXML) and code generation to mirror production RTE workflows.
