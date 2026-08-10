# ⚙️ Industrial Process & PID Control Simulator

An interactive, real-time simulator demonstrating **Supervisory Control** in industrial automation. This project pairs a traditional PID controller (the "muscle") with an Isolation Forest Machine Learning model (the "brain") to enforce automated fault tolerance and thermal fail-safes.

## 🚀 Features

*   **Real-Time Thermal Physics Engine:** Simulates the heating and cooling dynamics of a high-pressure industrial boiler.
*   **Interactive PID Tuning:** Live adjustments for Proportional (Kp), Integral (Ki), and Derivative (Kd) gains.
*   **Supervisory ML Control:** An Unsupervised Anomaly Detection model (`IsolationForest`) trained on synthetic thermodynamic data constantly monitors the PID controller's behavior.
*   **Advanced Signal Processing:** Built-in debouncing logic to differentiate between transient signal noise (sensor glitches) and genuine physical thermal runaway.
*   **Dynamic HMI Dashboard:** A custom-built HTML/CSS Human-Machine Interface featuring animated burner states, dynamic temperature glows, and live AI vision readouts.

## 🧠 The Architecture: Why ML + PID?

Standard PID controllers are "blind." If a sensor breaks and reads an impossibly high temperature, the PID controller will blindly attempt to correct it, potentially ruining product or causing a catastrophic failure. 

This architecture introduces an AI layer that monitors the physical bounds of the system. 
* If a **Sensor Glitch** occurs (a massive spike lasting < 4 seconds), the system's debouncing logic flags a transient noise warning but allows the system to recover. 
* If a **Thermal Runaway** occurs (a massive spike that persists), the AI recognizes the physical state violation, overrides the PID controller, and permanently trips the safety interlock.

## 🛠️ Installation & Usage

1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/Industrial-Fault-Simulator.git](https://github.com/yourusername/Industrial-Fault-Simulator.git)
   cd Industrial-Fault-Simulator
2. Install the required dependencies:
    pip install -r requirements.txt
3. Launch the simulator:
    streamlit run app.py
