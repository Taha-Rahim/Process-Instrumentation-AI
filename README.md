# ⚙️ AI-Driven Process Instrumentation & Interlock HMI

### Project Overview
This project simulates an industrial thermal process (e.g., a chemical reactor) and implements a modern Predictive Maintenance system. It bridges traditional Electrical Engineering control logic with Machine Learning to identify mechanical degradation before a catastrophic failure occurs.

### Core Engineering Concepts Demonstrated
* **Process Simulation:** Generated synthetic Process Variables (PV) with real-world sensor noise and simulated mechanical drift (a sticking cooling valve).
* **Machine Learning (Isolation Forest):** Replaced hard-coded, static alarm thresholds with an unsupervised AI model. The AI was trained on a healthy baseline to dynamically detect multi-dimensional anomalies in the data stream.
* **Safety Interlocks & Debouncing:** Engineered a fail-safe logic controller that requires consecutive AI flags to trigger an action, preventing false trips from random sensor noise.
* **HMI Dashboard Design:** Built a live, animated Human-Machine Interface using Python, featuring dynamic status indicators, active state coloring, and automated emergency shutdown visualization.
* **Closed-Loop PI Control & Supervisor Logic:** Implemented a software-based Proportional-Integral controller to dynamically modulate heater power in response to mechanical drift, paired with a saturated interlock cascade for fail-safe emergency shutdowns.

### How It Works
1. **The Nominal State:** The system runs at a setpoint of 180°C, perfectly balancing heater output with natural heat loss.
2. **The Failure:** At t = 60s, a mechanical failure (cooling valve leak) is introduced, causing temperatures to rise.
3. **The Detection:** The AI (Isolation Forest) detects the data profile shifting away from the trained baseline.
4. **The Mitigation (PI Control):** After 5 consecutive AI fault flags, control is handed to a Proportional-Integral (PI) loop, which dynamically throttles down the heater power to fight the rising temperature.
5. **The Escalation:** If the heater drops to 0% power (actuator saturation) and the temperature still breaches 192°C, a supervisor logic interlock forces a critical emergency shutdown to protect the facility.
6. 
### Technologies Used
* Python (Simulation & Control Logic)
* Scikit-Learn (Machine Learning / Isolation Forest)
* Matplotlib & ipywidgets (Live HMI Visualization)
