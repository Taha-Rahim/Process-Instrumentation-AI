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
1. **The Nominal State:** The system runs at a setpoint of 180°C. 
2. **The Failure:** At t = 60s, a mechanical failure is introduced. 
3. **The Detection:** The Isolation Forest detects the data profile shifting away from the trained baseline and begins throwing flags.
4. **The Action:** Once 5 consecutive faults are recorded, the safety interlock overrides the system, cutting power and forcing an emergency cooling sequence to protect the simulated equipment. 

### Technologies Used
* Python (Simulation & Control Logic)
* Scikit-Learn (Machine Learning / Isolation Forest)
* Matplotlib & ipywidgets (Live HMI Visualization)
