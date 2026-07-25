# AI-Supervised Active 3D Closed-Loop Control System

An intelligent process control and safety interlock simulation designed to monitor and protect a dynamic reactor system against thermal and flow-based anomalies.

## System Architecture & Engineering Logic

In industrial and electrical engineering, combining Machine Learning with automated control loops requires robust fail-safe mechanisms to handle sensor noise and prevent catastrophic failures. This project implements a three-tier defense architecture:

### 1. The ML Anomaly Detector
* **Model:** Isolation Forest / ML classifier evaluating real-time multivariate states (Process Temperature, Flow Rate, Pressure).
* **Function:** Continuously inspects the process trajectory for subtle operational drift or sudden faults.

### 2. The 3-Frame Debouncer
* **The Problem:** Raw sensor noise and transient spikes can trigger false-positive AI flags, causing erratic system panic.
* **The Solution:** A sequential counter requirement. The system demands **3 consecutive anomaly flags** before acknowledging a valid fault, successfully filtering out transient noise while maintaining a rapid response window (triggering within 3 seconds of a true fault).

### 3. The Safety Latch (Latching Relay Interlock)
* **The Problem:** Once an automated emergency shutdown cuts the heater and activates backup cooling, the process temperature eventually drops back toward the setpoint. A naive system would experience a false negative and blindly restart the heater, leading to dangerous limit-cycling.
* **The Solution:** Implemented a software-based **latching safety relay**. Once tripped, the emergency shutdown state *locks permanently*, requiring explicit manual intervention/reset regardless of temporary symptom improvement.

## Live HMI Visualization
The system features a custom real-time HMI built with Matplotlib and IPython widgets (`ipywidgets`), rendering smooth, flicker-free updates across three synchronized monitoring channels:
1. **Process Temperature & Safety Interlock:** Tracks live temperature against setpoints ($180^\circ\text{C}$) and critical limits ($186^\circ\text{C}$), dynamically shading active emergency states in red.
2. **Process Hydraulics:** Monitors live Flow ($\text{L/min}$) and Pressure ($\text{PSI}$).
3. **Control Action:** Visualizes PI controller output and emergency power cuts to the heater.
