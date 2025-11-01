# AUTOSAR Component Integration Demo

This repository showcases how two simplified AUTOSAR application software components interact via a hand-written Runtime Environment (RTE) abstraction.

## Components

- **SWC_Sensor** (`src/SWC_Sensor.c`) – publishes a simulated temperature signal through the RTE.
- **SWC_Controller** (`src/SWC_Controller.c`) – consumes the temperature signal and toggles an overheat flag when the value exceeds 50 °C.
- **RTE** (`src/Rte.c`) – mediates data exchange between SWCs and exposes initialization/read/write APIs, mimicking an AUTOSAR configuration.
- **Integration harness** (`src/main.c`) – executes both SWCs across several cycles and prints the resulting signal values.

## Build

Use the provided Python build script to compile and link all modules:

```bash
./scripts/build.py
```

The script invokes `gcc` with the appropriate include paths and places the resulting binary at `build/autosar_demo`.

## Run

```bash
./build/autosar_demo
```

Expected output resembles:

```
Cycle 0: Temp = 25.50 C, Overheat flag = OFF
Cycle 1: Temp = 26.00 C, Overheat flag = OFF
...
```

## Dashboard GUI

Launch a minimal Tkinter dashboard to run the demo binary and visualise the
temperature signal together with the controller flag:

```bash
python3 scripts/gui_dashboard.py
```

The dashboard will build the project on demand (if `build/autosar_demo` is
missing), stream the execution log, and update indicator labels for each RTE
cycle.

Additional details about the RTE mapping and integration steps are documented in [`docs/INTEGRATION_STEPS.md`](docs/INTEGRATION_STEPS.md).
