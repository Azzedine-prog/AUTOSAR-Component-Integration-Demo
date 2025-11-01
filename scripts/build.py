#!/usr/bin/env python3
"""Simple build script to compile AUTOSAR component demo."""

import os
import pathlib
import subprocess
import sys

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILD_DIR = PROJECT_ROOT / "build"
SRC_DIR = PROJECT_ROOT / "src"
INCLUDE_DIR = PROJECT_ROOT / "include"

C_SOURCES = [
    SRC_DIR / "Rte.c",
    SRC_DIR / "SWC_Sensor.c",
    SRC_DIR / "SWC_Controller.c",
    SRC_DIR / "main.c",
]


def run():
    BUILD_DIR.mkdir(exist_ok=True)
    output_binary = BUILD_DIR / "autosar_demo"

    compile_cmd = [
        "gcc",
        "-std=c11",
        "-Wall",
        "-Wextra",
        "-I",
        str(INCLUDE_DIR),
        "-o",
        str(output_binary),
    ] + [str(source) for source in C_SOURCES]

    print("Building AUTOSAR Component Integration Demo...")
    print("Command:", " ".join(compile_cmd))

    try:
        subprocess.check_call(compile_cmd)
    except (OSError, subprocess.CalledProcessError) as exc:  # pragma: no cover - debug message only
        print("Build failed:", exc)
        return 1

    print(f"Build complete. Binary located at {output_binary}")
    return 0


if __name__ == "__main__":
    sys.exit(run())
