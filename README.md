# ⚙️ AI-Driven Process Instrumentation & Fault-Tolerant Control HMI

## Project Overview

This project simulates an industrial thermal process (e.g., a chemical reactor) and implements a modern AI-driven control system. It bridges traditional Electrical Engineering control logic with Machine Learning to monitor interconnected physical variables, identify mechanical degradation, and seamlessly trigger redundant hardware systems before a catastrophic failure occurs.

## Core Engineering Concepts Demonstrated

* **Multi-Variable Process Simulation:** Engineered a physics engine that generates synthetic Process Variables (Temperature, Fluid Flow, and Pressure) with real-world sensor noise and simulated interconnected mechanical drift (e.g., a blockage causing flow drops, pressure spikes, and subsequent thermal runaway).
* **Multi-Dimensional Machine Learning (Isolation Forest):** Replaced hard-coded, static alarm thresholds with an unsupervised AI model evaluating a 3D data matrix in real-time. The AI was trained on a healthy baseline to dynamically detect complex anomalies in the data stream.
* **Safety Interlocks & Debouncing:** Engineered a fail-safe logic controller that requires consecutive AI flags to trigger an action, preventing false trips from random sensor noise.
* **Closed-Loop PI Control:** Implemented a software-based Proportional-Integral (PI) controller to dynamically modulate primary heater power in response to thermal drift.
* **Fault-Tolerant Redundant Logic:** Developed a supervisor interlock that monitors actuator saturation. If the primary heater is heavily throttled (<20%) or a critical temperature threshold is breached (>186°C), a secondary redundant cooling pump is instantly engaged.
* **HMI Dashboard Design:** Built a live, animated Human-Machine Interface using Python, featuring dynamic status indicators, multi-axis graphing, and real-time visualization of the control loop overrides.

## Project Progression & Architecture

### ✅ Phase 1: Baseline Anomaly Detection & Control
Established the core control loop. Successfully implemented active PI control and fault-tolerant redundant supervisor logic based on single-variable (Temperature) anomaly detection.

### ✅ Phase 2: Multi-Variable System Expansion (Passive Monitoring)
Real-world systems are interconnected. In this phase, the system was expanded to process multiple data streams simultaneously.
* **The Physics:** Introduced Pressure and Fluid Flow Rate into the simulation, writing logic where variables directly affect one another.
* **The Detection:** Upgraded the AI to evaluate a 3D matrix. At `t = 60s`, a mechanical degradation fault is introduced. The unsupervised AI successfully recognizes the abnormal correlation between dropping flow and spiking pressure, flagging the fault instantly—long before the temperature crosses critical thresholds.

### 🔄 Phase 3: Active 3D Closed-Loop Control (In Progress)
Wiring the multi-dimensional AI anomaly output (Phase 2) directly into the supervisor override logic (Phase 1) to automatically cut heater power and engage backup systems the moment a flow/pressure deviation is detected.

## Simulation Results

<img width="850" height="717" alt="Screenshot 2026-07-25 153312" src="https://github.com/user-attachments/assets/48de21c4-0f23-4e00-b2a1-a30351938024" />


## Technologies Used

* **Python** (Simulation & Control Logic)
* **Scikit-Learn** (Machine Learning / Isolation Forest)
* **Matplotlib & ipywidgets** (Live HMI Visualization)
