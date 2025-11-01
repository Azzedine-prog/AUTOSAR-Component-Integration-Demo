#!/usr/bin/env python3
"""Tkinter dashboard for the AUTOSAR component integration demo.

This lightweight GUI wraps the existing C demo binary so that users can
observe temperature values and the controller's overheat flag without
watching the console output in a terminal window.
"""

from __future__ import annotations

import pathlib
import queue
import re
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import messagebox, ttk

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILD_SCRIPT = PROJECT_ROOT / "scripts" / "build.py"
BINARY_PATH = PROJECT_ROOT / "build" / "autosar_demo"
OUTPUT_PATTERN = re.compile(
    r"Cycle\\s+(?P<cycle>\\d+):\\s+Temp\\s*=\\s*(?P<temp>[0-9]+(?:\\.[0-9]+)?)\\s*C,\\s+Overheat flag = (?P<flag>ON|OFF)")


class AutosarDashboard(tk.Tk):
    """Small dashboard that launches the compiled demo and visualises its output."""

    def __init__(self) -> None:
        super().__init__()
        self.title("AUTOSAR Demo Dashboard")
        self.geometry("560x360")
        self.resizable(False, False)

        self._log_queue: "queue.Queue[str]" = queue.Queue()
        self._reader_thread: threading.Thread | None = None
        self._process: subprocess.Popen[str] | None = None

        self._create_widgets()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(100, self._poll_log_queue)

    # ------------------------------------------------------------------
    # UI construction helpers
    # ------------------------------------------------------------------
    def _create_widgets(self) -> None:
        main = ttk.Frame(self, padding=12)
        main.pack(fill=tk.BOTH, expand=True)

        header = ttk.Label(
            main,
            text="AUTOSAR Component Integration Demo",
            font=("TkDefaultFont", 14, "bold"),
        )
        header.pack(anchor=tk.CENTER, pady=(0, 12))

        status_frame = ttk.Frame(main)
        status_frame.pack(fill=tk.X, pady=(0, 12))

        self.cycle_var = tk.StringVar(value="Cycle: -")
        ttk.Label(status_frame, textvariable=self.cycle_var).pack(side=tk.LEFT, padx=(0, 16))

        self.temp_var = tk.StringVar(value="Temperature: --.- °C")
        ttk.Label(status_frame, textvariable=self.temp_var).pack(side=tk.LEFT, padx=(0, 16))

        self.flag_var = tk.StringVar(value="Overheat flag: ---")
        self.flag_label = ttk.Label(status_frame, textvariable=self.flag_var)
        self.flag_label.pack(side=tk.LEFT)

        control_frame = ttk.Frame(main)
        control_frame.pack(fill=tk.X, pady=(0, 12))

        self.run_button = ttk.Button(control_frame, text="Run simulation", command=self._start_simulation)
        self.run_button.pack(side=tk.LEFT)

        self.progress = ttk.Progressbar(control_frame, length=180, mode="determinate", maximum=5)
        self.progress.pack(side=tk.LEFT, padx=(12, 0))

        self.log_widget = tk.Text(main, height=10, state=tk.DISABLED, wrap=tk.WORD)
        self.log_widget.pack(fill=tk.BOTH, expand=True)

    # ------------------------------------------------------------------
    # Simulation control
    # ------------------------------------------------------------------
    def _start_simulation(self) -> None:
        if self._reader_thread and self._reader_thread.is_alive():
            messagebox.showinfo("Simulation running", "The simulation is already in progress.")
            return

        if not self._ensure_build():
            return

        try:
            self._process = subprocess.Popen(
                [str(BINARY_PATH)],
                cwd=PROJECT_ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
            )
        except OSError as exc:
            messagebox.showerror("Launch failed", f"Failed to start demo binary: {exc}")
            self.run_button.configure(state=tk.NORMAL)
            return

        with self._log_queue.mutex:
            self._log_queue.queue.clear()
        self._reset_status()
        self._append_log("Simulation started...\n")

        self._reader_thread = threading.Thread(target=self._read_stdout, daemon=True)
        self._reader_thread.start()

    def _ensure_build(self) -> bool:
        if BINARY_PATH.exists():
            return True

        answer = messagebox.askyesno(
            "Build required",
            "The demo binary is missing. Would you like to build it now?",
        )
        if not answer:
            return False

        try:
            completed = subprocess.run(
                [sys.executable, str(BUILD_SCRIPT)],
                cwd=PROJECT_ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as exc:
            messagebox.showerror("Build failed", f"Build script exited with {exc.returncode}.")
            return False
        except OSError as exc:
            messagebox.showerror("Build failed", f"Unable to execute build script: {exc}")
            return False

        if completed.stdout:
            self._append_log(completed.stdout)
        if completed.stderr:
            self._append_log(completed.stderr)
        return True

    def _read_stdout(self) -> None:
        assert self._process is not None
        assert self._process.stdout is not None

        for raw_line in self._process.stdout:
            line = raw_line.strip()
            self._log_queue.put(line)

        self._process.wait()
        self._log_queue.put("__PROCESS_DONE__")

    # ------------------------------------------------------------------
    # Queue/Log handling
    # ------------------------------------------------------------------
    def _poll_log_queue(self) -> None:
        try:
            while True:
                line = self._log_queue.get_nowait()
                if line == "__PROCESS_DONE__":
                    self._append_log("Simulation finished.\n")
                    self.run_button.configure(state=tk.NORMAL)
                    self._process = None
                    self._reader_thread = None
                    break

                self._handle_log_line(line)
        except queue.Empty:
            pass

        self.after(100, self._poll_log_queue)

    def _handle_log_line(self, line: str) -> None:
        self._append_log(line + "\n")

        match = OUTPUT_PATTERN.search(line)
        if not match:
            return

        cycle = int(match.group("cycle"))
        temp = float(match.group("temp"))
        flag = match.group("flag")

        self.cycle_var.set(f"Cycle: {cycle}")
        self.temp_var.set(f"Temperature: {temp:.2f} °C")
        self.flag_var.set(f"Overheat flag: {flag}")

        if flag == "ON":
            self.flag_label.configure(foreground="red")
        else:
            self.flag_label.configure(foreground="green")

        max_value = float(self.progress.cget("maximum"))
        self.progress.configure(value=min(cycle + 1, max_value))

    def _append_log(self, text: str) -> None:
        self.log_widget.configure(state=tk.NORMAL)
        self.log_widget.insert(tk.END, text)
        self.log_widget.see(tk.END)
        self.log_widget.configure(state=tk.DISABLED)

    def _reset_status(self) -> None:
        self.cycle_var.set("Cycle: -")
        self.temp_var.set("Temperature: --.- °C")
        self.flag_var.set("Overheat flag: ---")
        self.flag_label.configure(foreground="black")
        self.progress.configure(value=0)
        self.run_button.configure(state=tk.DISABLED)

    # ------------------------------------------------------------------
    # Shutdown handling
    # ------------------------------------------------------------------
    def _on_close(self) -> None:
        if self._process and self._process.poll() is None:
            self._process.terminate()
        self.destroy()


def main() -> int:
    app = AutosarDashboard()
    app.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
