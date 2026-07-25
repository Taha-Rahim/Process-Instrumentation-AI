# ⚙️ AI-Driven Process Instrumentation & Fault-Tolerant Control HMI

## Project Overview
This project simulates an industrial thermal process (e.g., a chemical reactor) and implements a modern AI-driven control system. It bridges traditional Electrical Engineering control logic with Machine Learning to identify mechanical degradation and seamlessly trigger redundant hardware systems before a catastrophic failure occurs.

## Core Engineering Concepts Demonstrated
*   **Process Simulation:** Generated synthetic Process Variables (PV) with real-world sensor noise and simulated mechanical drift (a sticking cooling valve).
*   **Machine Learning (Isolation Forest):** Replaced hard-coded, static alarm thresholds with an unsupervised AI model. The AI was trained on a healthy baseline to dynamically detect multi-dimensional anomalies in the data stream.
*   **Safety Interlocks & Debouncing:** Engineered a fail-safe logic controller that requires consecutive AI flags to trigger an action, preventing false trips from random sensor noise.
*   **Closed-Loop PI Control:** Implemented a software-based Proportional-Integral controller to dynamically modulate primary heater power in response to the detected mechanical drift.
*   **Fault-Tolerant Redundant Logic:** Developed a supervisor interlock that monitors actuator saturation. If the primary heater is heavily throttled (<20%) or a critical temperature threshold is breached (>186°C), a secondary redundant cooling pump is instantly engaged.
*   **HMI Dashboard Design:** Built a live, animated Human-Machine Interface using Python, featuring dynamic status indicators, active state coloring, and real-time visualization of the control loop overrides.

## How It Works
1.  **The Nominal State:** The system runs at a setpoint of 180°C, balancing heater output with natural ambient heat loss.
2.  **The Failure:** At t = 60s, a mechanical failure is introduced, causing process temperatures to rise abnormally.
3.  **The Detection:** The AI (Isolation Forest) detects the data profile shifting away from the trained baseline.
4.  **The Mitigation (PI Control):** After 5 consecutive AI fault flags, control is handed to a Proportional-Integral (PI) loop, which dynamically throttles down the heater power to fight the rising temperature.
5.  **The Escalation (Redundant Override):** When the supervisor logic detects that the PI controller is struggling (heater output drops below 20%) or the temperature hits the critical 186°C limit, it instantly engages the backup cooling pump, successfully wrestling the process back into the safe operating band.

## Simulation Results
*(Insert your successful graph image here: `![Phase 3 Simulation](image_e3bc7e.jpg)`)*

## Technologies Used
*   Python (Simulation & Control Logic)
*   Scikit-Learn (Machine Learning / Isolation Forest)
*   Matplotlib & ipywidgets (Live HMI Visualization)
