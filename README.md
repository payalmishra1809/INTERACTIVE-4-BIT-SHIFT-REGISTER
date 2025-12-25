# INTERACTIVE-4-BIT-SHIFT-REGISTER

# 4-bit PIPO Shift Register – Tkinter Visualizer

This project is a **4-bit PIPO (Parallel-In, Parallel-Out) shift register** visualizer built using Python's Tkinter GUI toolkit.  
It is designed for Digital Logic Design / DLD lab demonstrations and helps students understand how parallel inputs are latched into a parallel output word.

## Features

- Four clickable input toggles **D3..D0** (MSB to LSB) to set input bits.
- **Load (Latch)** button that captures D3..D0 into Q3..Q0 in a single parallel operation.
- Large colored output boxes for **Q3, Q2, Q1, Q0**.
- Big violet word box showing the current 4-bit output word \(Q3Q2Q1Q0\).
- **Reset** button to clear both the outputs and the load counter.
- Load counter showing how many times the register has been latched.

## How it works

- The internal model is a small `PIPO4` class that stores the 4-bit output as a list `[Q3, Q2, Q1, Q0]`.
- When you press **Load (Latch)**, the current inputs `[D3, D2, D1, D0]` are copied into `[Q3, Q2, Q1, Q0]` in one step (parallel load).
- The GUI updates:
  - The header shows `Loads: N`.
  - The word box shows the 4-bit word like `1010`.
  - The four big boxes display each bit of Q3..Q0.

This mimics the behavior of a real 4-bit PIPO register used in digital systems.

## Requirements

- Python 3.x
- Tkinter (usually comes bundled with standard Python on most platforms)

You can check Tkinter availability by running:

