import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import IsolationForest
import time

# --- PAGE SETUP & UI THEMING ---
st.set_page_config(page_title="Process Control Simulator", layout="wide")

# Injecting CSS for a sleek industrial gradient background
page_bg_css = """
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
}
</style>
"""
st.markdown(page_bg_css, unsafe_allow_html=True)

# --- CACHE THE AI MODEL ---
@st.cache_resource
def load_ai_model():
    np.random.seed(42)
    normal_temps = np.random.normal(loc=75.0, scale=2.0, size=1000)
    normal_variances = np.random.uniform(0.0, 3.0, size=1000)
    normal_kps = np.random.uniform(0.5, 2.5, size=1000)
    X_train = np.column_stack((normal_temps, normal_variances, normal_kps))
    
    model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
    model.fit(X_train)
    return model

iso_model = load_ai_model()

# --- SESSION STATE INITIALIZATION ---
if 'kp_slider' not in st.session_state: st.session_state.kp_slider = 1.0
if 'kp_num' not in st.session_state: st.session_state.kp_num = 1.0
if 'ki_slider' not in st.session_state: st.session_state.ki_slider = 0.1
if 'ki_num' not in st.session_state: st.session_state.ki_num = 0.1
if 'kd_slider' not in st.session_state: st.session_state.kd_slider = 0.05
if 'kd_num' not in st.session_state: st.session_state.kd_num = 0.05
if 'run_state' not in st.session_state: st.session_state.run_state = 'paused'
if 'current_time' not in st.session_state: st.session_state.current_time = 0
if 'pv' not in st.session_state: st.session_state.pv = 25.0
if 'integral_error' not in st.session_state: st.session_state.integral_error = 0.0
if 'prev_error' not in st.session_state: st.session_state.prev_error = 0.0
if 'disturbance' not in st.session_state: st.session_state.disturbance = False
if 'glitch_ticks' not in st.session_state: st.session_state.glitch_ticks = 0
if 'anomaly_count' not in st.session_state: st.session_state.anomaly_count = 0
if 'system_tripped' not in st.session_state: st.session_state.system_tripped = False
if 'trip_time' not in st.session_state: st.session_state.trip_time = None
if 'history_time' not in st.session_state: st.session_state.history_time = []
if 'history_pv' not in st.session_state: st.session_state.history_pv = []
if 'history_sp' not in st.session_state: st.session_state.history_sp = []
if 'history_ai' not in st.session_state: st.session_state.history_ai = []
if 'fault_counts' not in st.session_state: st.session_state.fault_counts = {"Warnings": 0, "Criticals": 0}

# --- CONTROL CALLBACKS ---
def play_sim(): st.session_state.run_state = 'running'
def pause_sim(): st.session_state.run_state = 'paused'
def stop_sim(): st.session_state.run_state = 'stopped'
def inject_fault(): st.session_state.disturbance = True
def inject_glitch(): 
    st.session_state.glitch_ticks = 2
    st.session_state.fault_counts["Warnings"] += 1

def reset_env():
    st.session_state.run_state = 'paused'
    st.session_state.current_time = 0
    st.session_state.pv = 25.0
    st.session_state.integral_error = 0.0
    st.session_state.prev_error = 0.0
    st.session_state.disturbance = False
    st.session_state.glitch_ticks = 0
    st.session_state.anomaly_count = 0
    st.session_state.system_tripped = False
    st.session_state.trip_time = None
    st.session_state.history_time = []
    st.session_state.history_pv = []
    st.session_state.history_sp = []
    st.session_state.history_ai = []
    st.session_state.fault_counts = {"Warnings": 0, "Criticals": 0}
    
def reset_tunings():
    st.session_state.kp_slider = 1.0
    st.session_state.kp_num = 1.0
    st.session_state.ki_slider = 0.1
    st.session_state.ki_num = 0.1
    st.session_state.kd_slider = 0.05
    st.session_state.kd_num = 0.05

def sync_kp_slider(): st.session_state.kp_num = st.session_state.kp_slider
def sync_kp_num(): st.session_state.kp_slider = st.session_state.kp_num
def sync_ki_slider(): st.session_state.ki_num = st.session_state.ki_slider
def sync_ki_num(): st.session_state.ki_slider = st.session_state.ki_num
def sync_kd_slider(): st.session_state.kd_num = st.session_state.kd_slider
def sync_kd_num(): st.session_state.kd_slider = st.session_state.kd_num

# --- SIDEBAR: PID CONTROL SETTINGS ---
is_stopped = (st.session_state.run_state == 'stopped')

st.sidebar.header("🎛️ PID Tuning")
st.sidebar.button("🔄 Reset Parameters", on_click=reset_tunings, disabled=is_stopped)
st.sidebar.divider()

st.sidebar.write("**Proportional (Kp)**")
st.sidebar.slider("Kp Slider", 0.0, 50.0, key="kp_slider", on_change=sync_kp_slider, label_visibility="collapsed", disabled=is_stopped)
st.sidebar.number_input("Kp Input", 0.0, 50.0, step=0.1, key="kp_num", on_change=sync_kp_num, label_visibility="collapsed", disabled=is_stopped)

st.sidebar.write("**Integral (Ki)**")
st.sidebar.slider("Ki Slider", 0.0, 10.0, key="ki_slider", on_change=sync_ki_slider, label_visibility="collapsed", disabled=is_stopped)
st.sidebar.number_input("Ki Input", 0.0, 10.0, step=0.05, key="ki_num", on_change=sync_ki_num, label_visibility="collapsed", disabled=is_stopped)

st.sidebar.write("**Derivative (Kd)**")
st.sidebar.slider("Kd Slider", 0.0, 10.0, key="kd_slider", on_change=sync_kd_slider, label_visibility="collapsed", disabled=is_stopped)
st.sidebar.number_input("Kd Input", 0.0, 10.0, step=0.01, key="kd_num", on_change=sync_kd_num, label_visibility="collapsed", disabled=is_stopped)

kp, ki, kd = st.session_state.kp_slider, st.session_state.ki_slider, st.session_state.kd_slider

# --- MAIN UI: HEADER & CONTROL DECK ---
st.title("⚙️ Industrial Process & PID Control Simulator")

col1, col2, col3, col4, col5, col6, col7 = st.columns([1.2, 1.2, 1.2, 1.8, 2.0, 1.5, 3.5])
col1.button("▶️ Play", on_click=play_sim, disabled=(st.session_state.run_state == 'running' or is_stopped), use_container_width=True)
col2.button("⏸️ Pause", on_click=pause_sim, disabled=(st.session_state.run_state == 'paused' or is_stopped), use_container_width=True)
col3.button("⏹️ Stop", on_click=stop_sim, disabled=is_stopped, use_container_width=True)
col4.button("⚡ Thermal Runaway", on_click=inject_fault, disabled=is_stopped, help="Physical heat spike", use_container_width=True)
col5.button("📡 Sensor Glitch", on_click=inject_glitch, disabled=is_stopped, help="Transient noise spike", use_container_width=True)
col6.button("♻️ Reset Env", on_click=reset_env, use_container_width=True)

with col7:
    if st.session_state.system_tripped:
        st.error("🚨 **AI INTERLOCK: TRIPPED**")
    elif st.session_state.run_state == 'running':
        st.success("🟢 **SYSTEM: RUNNING**")
    elif st.session_state.run_state == 'paused':
        st.warning("🟡 **SYSTEM: PAUSED**")
    else:
        st.error("🔴 **SYSTEM: STOPPED**")

st.divider()

# --- ENGINE LOGIC ---
setpoint = 75.0
dt = 1.0
output = 0.0 

if st.session_state.run_state == 'running':
    # Automated Cooldown Shutdown
    if st.session_state.system_tripped and st.session_state.trip_time is not None:
        if st.session_state.current_time - st.session_state.trip_time >= 50:
            st.session_state.run_state = 'stopped'
            st.rerun()

    # 1. True Physical Temperature (pv)
    if st.session_state.disturbance:
        st.session_state.pv += 50.0 
        st.session_state.disturbance = False
        
    # 2. Sensor Reading (What the PID and AI actually see)
    sensor_reading = st.session_state.pv
    
    if st.session_state.glitch_ticks > 0:
        sensor_reading += 85.0 # Massive fake spike
        st.session_state.glitch_ticks -= 1
        
    # PID Math uses the sensor reading
    error = setpoint - sensor_reading
    
    P_out = kp * error
    derivative_error = (error - st.session_state.prev_error) / dt
    D_out = kd * derivative_error
    
    MAX_POWER = 1000.0  
    MIN_POWER = 0.0     
    
    tentative_I_out = ki * (st.session_state.integral_error + error * dt)
    tentative_output = P_out + tentative_I_out + D_out
    
    if MIN_POWER <= tentative_output <= MAX_POWER:
        st.session_state.integral_error += error * dt
        
    I_out = ki * st.session_state.integral_error
    
    if st.session_state.system_tripped:
        output = 0.0 
    else:
        raw_output = P_out + I_out + D_out
        output = np.clip(raw_output, MIN_POWER, MAX_POWER)
    
    # Physics updates the true physical temperature (pv)
    process_gain, time_constant, ambient_temp = 0.8, 12.0, 25.0
    st.session_state.pv += ((process_gain * output - (st.session_state.pv - ambient_temp)) / time_constant) * dt
    st.session_state.pv = np.clip(st.session_state.pv, ambient_temp, 2000.0)
    
    st.session_state.current_time += 1
    st.session_state.prev_error = error
    
    # We log the sensor_reading so the graph reflects what the HMI screens show
    st.session_state.history_time.append(st.session_state.current_time)
    st.session_state.history_pv.append(sensor_reading)
    st.session_state.history_sp.append(setpoint)
    
    # --- AI ANOMALY DETECTION & DEBOUNCING ---
    hist_array = np.array(st.session_state.history_pv)
    recent_variance = np.var(hist_array[-20:]) if len(hist_array) > 20 else 0.0
    current_features = np.array([[sensor_reading, recent_variance, kp]])
    
    prediction = iso_model.predict(current_features)[0]
    GRACE_PERIOD = 30 
    
    # 1. Ground-Truth Override: Check the actual physical mass of the tank (pv), 
    # not the raw noisy sensor data, to confirm physical stability.
    is_physically_stable = abs(st.session_state.pv - setpoint) < 5.0
    
    if prediction == -1 and st.session_state.current_time > GRACE_PERIOD:
        if is_physically_stable:
            # The AI sees high variance, but the physical tank is fine. Ignore the ghost.
            st.session_state.anomaly_count = 0
        else:
            # The physical temperature is actually out of bounds. Increment counter.
            st.session_state.anomaly_count += 1
    else:
        st.session_state.anomaly_count = 0 
        
    # 2. Debounce: Trip only if a genuine physical anomaly persists for 4 seconds
    if st.session_state.anomaly_count >= 4 and not st.session_state.system_tripped:
        st.session_state.system_tripped = True
        st.session_state.trip_time = st.session_state.current_time 
        st.session_state.history_ai.append("Critical Fault Confirmed")
        st.session_state.fault_counts["Criticals"] += 1
    else:
        if st.session_state.system_tripped:
            st.session_state.history_ai.append("Interlock Active")
        elif st.session_state.anomaly_count > 0 or st.session_state.glitch_ticks > 0:
            st.session_state.history_ai.append("Warning: Transient Noise")
        elif st.session_state.current_time <= GRACE_PERIOD:
            st.session_state.history_ai.append("Startup Warming")
        else:
            st.session_state.history_ai.append("Normal")

# --- VISUALIZATION (HMI & Rolling Graph) ---
if len(st.session_state.history_time) > 0:
    col_hmi, col_graph = st.columns([1.5, 3.5])
    
    with col_hmi:
        st.subheader("🏭 Boiler HMI")
        
        # Display the sensor reading to the operator
        current_temp = st.session_state.history_pv[-1]
        
        if current_temp < 40: glow_color = "#3182ce" 
        elif current_temp < 85: glow_color = "#d69e2e" 
        elif current_temp < 120: glow_color = "#ed8936" 
        else: glow_color = "#e53e3e" 
        
        if st.session_state.system_tripped:
            heater_state = "🔴 INTERLOCK ENGAGED"
            heater_color = "#ff4b4b"
            flame_opacity = 0.0
        elif output == 0.0:
            heater_state = "⚪ BURNER OFF"
            heater_color = "gray"
            flame_opacity = 0.0
        else:
            power_percent = int((output/1000)*100)
            heater_state = f"🔥 BURNER ({power_percent}%)"
            heater_color = "#a6e22e"
            flame_opacity = 1.0

        # Bulletproof HTML string formatting
        hmi_html = (
            f"<div style='background-color: rgba(26, 28, 35, 0.85); padding: 20px; border-radius: 12px; border: 1px solid #3d404b; text-align: center; box-shadow: 0px 8px 16px rgba(0,0,0,0.4); backdrop-filter: blur(10px);'>"
            f"<h4 style='color: #e2e8f0; margin-bottom: 15px; font-family: monospace;'>High-Pressure Boiler</h4>"
            f"<div style='width: 130px; height: 180px; border: 4px solid #4a5568; border-radius: 60px 60px 10px 10px; margin: 0 auto; position: relative; background: linear-gradient(to right, #2d3748, #4a5568, #2d3748); overflow: hidden; box-shadow: inset 0px 5px 15px rgba(0,0,0,0.5);'>"
            f"<div style='position: absolute; bottom: 0; width: 100%; height: 100%; background: radial-gradient(circle at bottom, {glow_color} 0%, transparent 80%); opacity: 0.85; transition: all 0.3s ease;'></div>"
            f"<div style='position: absolute; bottom: 0; left: 50%; transform: translateX(-50%); width: {max(30, (output/1000)*100)}%; height: {min(60, (output/1000)*60)}%; background: linear-gradient(to top, #ed8936, #ecc94b, transparent); border-radius: 50% 50% 0 0; opacity: {flame_opacity}; transition: all 0.1s ease;'></div>"
            f"<div style='position: absolute; top: 35%; width: 100%; text-align: center; color: white; font-weight: 900; font-size: 1.4rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.8); font-family: monospace;'>{int(current_temp)} &deg;C</div>"
            f"</div>"
            f"<hr style='border-color: #3d404b; margin: 15px 0;'>"
            f"<div style='text-align: left; font-size: 0.95rem; color: #cbd5e0; font-family: monospace; line-height: 1.6;'>"
            f"<div style='display: flex; justify-content: space-between;'><span>Target SP:</span> <span style='color: #63b3ed;'>{setpoint} &deg;C</span></div>"
            f"<div style='display: flex; justify-content: space-between;'><span>State:</span> <span style='color: {heater_color}; font-weight: bold;'>{heater_state}</span></div>"
            f"<div style='display: flex; justify-content: space-between;'><span>AI Vision:</span> <span>{st.session_state.history_ai[-1]}</span></div>"
            f"</div></div>"
        )
        st.markdown(hmi_html, unsafe_allow_html=True)
        
    with col_graph:
        st.subheader("📈 Real-Time Thermal Response")
        window_time = st.session_state.history_time[-150:]
        window_pv = st.session_state.history_pv[-150:]
        window_sp = st.session_state.history_sp[-150:]
        
        fig, ax = plt.subplots(figsize=(10, 4.5))
        # Making the plot background slightly transparent to blend with gradient
        fig.patch.set_alpha(0.0)
        ax.set_facecolor((14/255, 17/255, 23/255, 0.6))
        ax.tick_params(colors='lightgray')
        for spine in ax.spines.values(): spine.set_color('#333333')
        ax.grid(color='#333333', linestyle='--', linewidth=1, alpha=0.5)

        Y_MAX = 150.0
        clipped_pv = np.clip(window_pv, 0, Y_MAX)

        ax.plot(window_time, window_sp, color="#ff4b4b", linestyle="--", linewidth=2.5, label="Target Setpoint")
        
        line_color = "#ff4b4b" if st.session_state.system_tripped else "#00f2fe"
        ax.plot(window_time, clipped_pv, color=line_color, linewidth=3, label="Sensor Reading")
        ax.fill_between(window_time, clipped_pv, color=line_color, alpha=0.15)
        
        out_of_bounds_indices = np.where(np.array(window_pv) > Y_MAX)[0]
        
        if len(out_of_bounds_indices) > 0:
            oob_times = np.array(window_time)[out_of_bounds_indices]
            oob_y = np.full(len(oob_times), Y_MAX)
            ax.scatter(oob_times, oob_y, color="#a6e22e", s=40, zorder=5) 
            
            max_idx = np.argmax(window_pv)
            max_time = window_time[max_idx]
            max_val = window_pv[max_idx]
            
            if max_val > Y_MAX:
                ax.annotate(f"{int(max_val):,}",
                            xy=(max_time, Y_MAX),
                            xytext=(0, 12),
                            textcoords="offset points",
                            color="#a6e22e",
                            fontweight="bold",
                            fontsize=12,
                            ha="center")
        
        ax.set_xlim(max(0, st.session_state.current_time - 150), max(150, st.session_state.current_time))
        ax.set_ylim(0, Y_MAX)

        ax.set_xlabel("Time (Seconds)", color='lightgray')
        ax.set_ylabel("Temperature (°C)", color='lightgray')
        legend = ax.legend(loc="lower right", facecolor="#0E1117", edgecolor="#333333")
        for text in legend.get_texts(): text.set_color("white")
            
        st.pyplot(fig)
else:
    st.info("System is ready. Press 'Play' to begin simulation.")

# --- POST-SIMULATION ANALYTICS REPORT ---
if st.session_state.run_state == 'stopped' and len(st.session_state.history_pv) > 0:
    st.divider()
    st.header("📊 Advanced Post-Simulation Analytics")
    
    pv_array = np.array(st.session_state.history_pv)
    sp_array = np.array(st.session_state.history_sp)
    
    max_temp = np.max(pv_array)
    min_temp = np.min(pv_array)
    mean_temp = np.mean(pv_array)
    total_variance = np.var(pv_array)
    total_time = st.session_state.current_time
    max_overshoot = np.max(pv_array - sp_array) if np.max(pv_array) > setpoint else 0.0
    mae = np.mean(np.abs(pv_array - sp_array)) 
    
    colA, colB, colC = st.columns(3)
    
    with colA:
        st.metric("Total Run Time", f"{total_time} s")
        st.metric("Max System Temp", f"{round(max_temp, 2)} °C")
        st.metric("Min System Temp", f"{round(min_temp, 2)} °C")
        
    with colB:
        st.metric("Mean Absolute Error (MAE)", f"{round(mae, 2)} °C")
        st.metric("Max Overshoot", f"+{round(max_overshoot, 2)} °C")
        st.metric("Average Temperature", f"{round(mean_temp, 2)} °C")
        
    with colC:
        st.metric("Confirmed Faults (Trips)", st.session_state.fault_counts['Criticals'])
        st.metric("Transient Glitches Detected", st.session_state.fault_counts['Warnings'])
        if st.session_state.system_tripped and st.session_state.trip_time:
            st.metric("Time to Failure (TTF)", f"{st.session_state.trip_time} s")
        else:
            st.metric("System Health", "Optimal")

    st.divider()
    
    if st.session_state.system_tripped:
        st.error(f"🔒 **Safety Status:** System interlock was automatically engaged at **{st.session_state.trip_time}s** to prevent thermal runaway. Simulation terminated after safe cooldown sequence.")
    else:
        st.success("✅ **Safety Status:** Simulation completed successfully with no critical safety interventions.")
    
    export_df = pd.DataFrame({
        "Time (s)": st.session_state.history_time,
        "Sensor Temp (C)": st.session_state.history_pv,
        "Setpoint (C)": st.session_state.history_sp,
        "AI Status": st.session_state.history_ai
    })
    csv = export_df.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Download Advanced Run Data (CSV)", data=csv, file_name='simulation_report_advanced.csv', mime='text/csv')

# --- TRIGGER THE RERUN LOOP ---
if st.session_state.run_state == 'running':
    time.sleep(0.05)
    st.rerun()