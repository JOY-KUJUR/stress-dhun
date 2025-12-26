import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date
import os

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Stress Sense",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= DARK FUTURISTIC UI =================
st.markdown("""
<style>
.stApp { background-color: #05070a; color: #e5e7eb; }
.metric-card {
    background: rgba(17,24,39,0.75);
    border: 1px solid #374151;
    border-radius: 16px;
    padding: 20px;
}
.metric-card:hover { border-color: #38bdf8; }
.block {
    height: 38px;
    border-radius: 10px;
    font-weight: 600;
    text-align: center;
    line-height: 38px;
}
.rest { background: #10b981; color: white; }
.study { background: #ef4444; color: white; }
.game { background: #6366f1; color: white; }
.other { background: #f59e0b; color: #111; }
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ================= DATA =================
DATA_FILE = "stress_data.csv"
if not os.path.exists(DATA_FILE):
    pd.DataFrame(
        columns=["date","rest","study","game","other","stress","status","summary"]
    ).to_csv(DATA_FILE, index=False)

df = pd.read_csv(DATA_FILE)

# ================= SESSION STATE =================
if "hours" not in st.session_state:
    st.session_state.hours = ["rest"] * 24

# ================= HEADER =================
st.title("🧠 AI Stress Analyzer")
st.caption("Dark • Futuristic • Hour-wise Behavioral Intelligence")

# ================= ACTIVITY SELECT =================
activity_map = {
    "Rest / Sleep": "rest",
    "Study / Work": "study",
    "Gaming": "game",
    "Other": "other"
}

selected = st.segmented_control(
    "Activity Tool",
    options=list(activity_map.keys()),
    default="Rest / Sleep"
)
current_activity = activity_map[selected]

# ================= HOUR GRID =================
st.markdown("### ⏱ Map Your Day (24 Hours)")
cols = st.columns(12)
for i in range(24):
    with cols[i % 12]:
        if st.button(f"{i}:00", key=f"h{i}", use_container_width=True):
            st.session_state.hours[i] = current_activity
            st.rerun()
        st.markdown(
            f"<div class='block {st.session_state.hours[i]}'></div>",
            unsafe_allow_html=True
        )

# ================= STRESS CALC =================
stress = 0
trend = []
counts = {"rest":0,"study":0,"game":0,"other":0}

for h in st.session_state.hours:
    counts[h] += 1
    if h == "study": stress += 8
    elif h == "game": stress += 2
    elif h == "other": stress += 4
    elif h == "rest": stress -= 6
    stress = max(0, min(100, stress))
    trend.append(stress)

# ================= ADVANCED AI ENGINE =================
def get_ai_advice(c, s, trend):
    total = sum(c.values())
    rest_ratio = c["rest"] / max(1, total)
    study_ratio = c["study"] / max(1, total)
    peak = max(trend)
    evening_avg = sum(trend[18:]) / max(1, len(trend[18:]))

    # Continuous study streak
    streak = cur = 0
    for h in st.session_state.hours:
        if h == "study":
            cur += 1
            streak = max(streak, cur)
        else:
            cur = 0

    if s > 85 or peak > 90:
        return ("🚨 CRITICAL BURNOUT\nStop work immediately. Sleep 8+ hrs.\nTomorrow risk: VERY HIGH", "Danger")

    if streak >= 5:
        return (f"🧠 FATIGUE ALERT\n{streak} hrs continuous study.\nInsert long break.\nTomorrow risk: Focus drop", "Warning")

    if c["study"] > 10:
        return ("📚 ACADEMIC OVERLOAD\nReduce study by 1–2 hrs.\nUse active recall.", "Warning")

    if c["rest"] < 6:
        return ("😴 SLEEP DEBT\nRecovery insufficient.\nStress will compound tomorrow.", "Urgent")

    if rest_ratio > 0.6 and c["study"] < 3:
        return ("🧘 UNDER-STIMULATION\nToo much rest.\nConvert rest → study.", "Balanced")

    if c["game"] > 6:
        return ("🎮 DOPAMINE FATIGUE\nGaming too high.\nReduce by 1–2 hrs.", "Caution")

    if evening_avg > 60:
        return ("🌙 LATE-DAY OVERLOAD\nStop heavy tasks after 8 PM.", "Caution")

    if s < 30 and study_ratio > 0.2:
        return ("✨ FLOW STATE\nLow stress + productivity.\nProtect this rhythm.", "Healthy")

    return ("✅ STABLE BALANCE\nRoutine is sustainable.", "Healthy")

ai_text, status = get_ai_advice(counts, stress, trend)

# ================= DASHBOARD =================
st.markdown("---")
c1, c2, c3 = st.columns([1,1,2])

with c1:
    st.markdown(f"""
    <div class="metric-card">
    <p>STRESS SCORE</p>
    <h1 style="color:#38bdf8">{stress}%</h1>
    <small>Status: {status}</small>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
    <p>AI COACH</p>
    <p style="font-size:0.9rem">{ai_text}</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    pie = px.pie(
        values=list(counts.values()),
        names=list(counts.keys()),
        hole=0.6,
        color=list(counts.keys()),
        color_discrete_map={
            "rest":"#10b981",
            "study":"#ef4444",
            "game":"#6366f1",
            "other":"#f59e0b"
        }
    )
    pie.update_layout(template="plotly_dark", height=220, showlegend=False)
    st.plotly_chart(pie, use_container_width=True)

# ================= LIVE GRAPH =================
st.markdown("### 📈 Live Stress Progression")
fig = go.Figure()
fig.add_trace(go.Scatter(
    y=trend,
    mode="lines",
    fill="tozeroy",
    line=dict(color="#38bdf8", width=3)
))
fig.update_layout(
    template="plotly_dark",
    height=300,
    yaxis=dict(range=[0,100]),
    xaxis_title="Hour",
    yaxis_title="Stress"
)
st.plotly_chart(fig, use_container_width=True)

# ================= SAVE =================
if st.button("💾 Save Today", use_container_width=True):
    new = pd.DataFrame([{
        "date": str(date.today()),
        "rest": counts["rest"],
        "study": counts["study"],
        "game": counts["game"],
        "other": counts["other"],
        "stress": stress,
        "status": status,
        "summary": ai_text
    }])
    df = pd.concat([df, new], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.toast("Daily metrics saved!", icon="✅")

# ================= HISTORY =================
st.markdown("---")
st.markdown("### 📊 Historical Analytics")

if not df.empty:
    fig_h = px.line(
        df, x="date", y="stress",
        markers=True,
        color_discrete_sequence=["#38bdf8"]
    )
    fig_h.update_layout(template="plotly_dark", yaxis=dict(range=[0,100]))
    st.plotly_chart(fig_h, use_container_width=True)

    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No historical data yet.")
