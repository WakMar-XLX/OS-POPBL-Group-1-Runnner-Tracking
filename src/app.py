"""app.py - WaveFlow dashboard (Streamlit).

Run with:  streamlit run src/app.py
"""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from scheduler import ALGOS, Wave, runners_released, schedule, state_at

st.set_page_config(page_title="WaveFlow", layout="wide")
st.title("WaveFlow: Wave Start Scheduler and Runner Tracker")
st.caption("Each wave is a process and the start line is the CPU.")

# ---- sidebar settings ----------------------------------------------------
algo = st.sidebar.radio("Algorithm", ALGOS, index=1)
quantum = st.sidebar.number_input("Time quantum (min)", 1, 20, 5, disabled=algo != "Round Robin")
switch = st.sidebar.number_input("Line clearing between waves (min)", 0, 5, 1)

# ---- editable wave table -------------------------------------------------
default = pd.DataFrame([
    ["21K Elite", 0, 8, 1, 40],
    ["10K", 2, 10, 2, 120],
    ["5K", 4, 6, 3, 200],
    ["Family fun run", 6, 12, 4, 150],
    ["OKU wave", 0, 5, 1, 15],
], columns=["name", "arrival", "burst", "priority", "runners"])
df = st.data_editor(default, num_rows="dynamic", use_container_width=True)
df = df.dropna()
if df.empty:
    st.warning("Add at least one wave.")
    st.stop()
waves = [Wave(r.name, int(r.arrival), int(r.burst), int(r.priority), int(r.runners))
         for r in df.itertuples()]

result = schedule(waves, algo, quantum, switch)

# ---- Gantt chart ---------------------------------------------------------
fig = go.Figure()
for s in result["slices"]:
    label = "Line clearing" if s["type"] == "switch" else waves[s["wave"]].name
    fig.add_trace(go.Bar(
        x=[s["end"] - s["start"]], base=[s["start"]], y=["Start line"],
        orientation="h", name=label, text=label if s["type"] == "run" else "",
        textposition="inside", insidetextanchor="middle",
        marker_color="#94A3B8" if s["type"] == "switch" else None, showlegend=False))
fig.update_layout(barmode="overlay", height=200, xaxis_title="Minutes")
st.plotly_chart(fig, use_container_width=True)

# ---- runner state tracker ------------------------------------------------
clock = st.slider("Clock (min)", 0, int(result["end"]), 0)
rows = [{"PID": f"P{k + 1:03d}", "Wave": w.name,
         "State": state_at(waves, result, k, clock),
         "Runners released": f"{runners_released(waves, result, k, clock)} / {w.runners}"}
        for k, w in enumerate(waves)]
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ---- algorithm comparison ------------------------------------------------
comp = []
for a in ALGOS:
    r = schedule(waves, a, quantum, switch)
    comp.append({"Algorithm": a, "Avg waiting": round(r["avg_waiting"], 1),
                 "Avg turnaround": round(r["avg_turnaround"], 1),
                 "Avg response": round(r["avg_response"], 1)})
st.subheader("Algorithm comparison (minutes)")
st.dataframe(pd.DataFrame(comp), use_container_width=True, hide_index=True)
