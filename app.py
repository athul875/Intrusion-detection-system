import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="IDS Dashboard",
    page_icon="🛡️",
    layout="wide"
)
st_autorefresh(interval=5000, key="ids_refresh")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
    color: white;
}

div[data-testid="metric-container"] {
    background-color: #1E1E1E;
    border: 1px solid #00BFFF;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}

h1, h2, h3 {
    color: white;
}

[data-testid="stDataFrame"] {
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- DATABASE ----------------
conn = sqlite3.connect("logs.db")
df = pd.read_sql_query("SELECT * FROM alerts", conn)


# Clear Logs Button
if st.button("🗑️ Clear All Logs"):
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM alerts")

    conn.commit()
    conn.close()

    st.success("Logs Cleared!")
    st.rerun()
# ---------------- HEADER ----------------
st.title("🛡️ Intrusion Detection System Dashboard")
st.markdown("---")

# ---------------- METRICS ----------------
total_alerts = len(df)

unique_ips = (
    df["source_ip"].nunique()
    if len(df) > 0 else 0
)

high_alerts = (
    len(df[df["risk_level"] == "HIGH"])
    if len(df) > 0 else 0
)

latest_ip = (
    df.iloc[-1]["source_ip"]
    if len(df) > 0 else "N/A"
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🚨 Total Alerts", total_alerts)

with col2:
    st.metric("🌐 Unique IPs", unique_ips)

with col3:
    st.metric("⚠️ High Risk", high_alerts)

with col4:
    st.metric("📍 Latest IP", latest_ip)

st.markdown("---")

# ---------------- CHARTS ----------------
col1, col2 = st.columns(2)

import plotly.express as px

with col1:
    st.subheader("📊 Risk Distribution")

    if len(df) > 0:
        risk_counts = df["risk_level"].value_counts()

        fig = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            hole=0.5
        )

        fig.update_layout(
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font_color="white",
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig, width="stretch")

with col2:
    st.subheader("🔵 Top Source IPs")

    if len(df) > 0:
        ip_counts = df["source_ip"].value_counts().head(10)

        fig_ip = px.bar(
            x=ip_counts.index,
            y=ip_counts.values,
            color=ip_counts.index,
            color_discrete_sequence=[
                "#FF4B4B",
                "#FFA500",
                "#FFD700",
                "#00FF7F",
                "#00E5FF",
                "#1E90FF",
                "#9D4EDD",
                "#FF69B4",
                "#7FFF00",
                "#FF6347"
            ]
        )

        fig_ip.update_layout(
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font_color="white",
            showlegend=False
        )

        st.plotly_chart(fig_ip, width="stretch")

st.markdown("---")

import plotly.express as px

if len(df) > 0:
    risk_counts = df["risk_level"].value_counts()

    fig = px.pie(
        values=risk_counts.values,
        names=risk_counts.index,
        title="Risk Level Distribution",
        hole=0.4
    )

    st.plotly_chart(fig, width="stretch")

# ---------------- RECENT ALERTS ----------------
st.subheader("🚨 Recent Alerts")

if len(df) > 0:
    st.dataframe(
        df.tail(10),
        use_container_width=True
    )
else:
    st.info("No alerts recorded yet.")

st.markdown("---")

# ---------------- FULL LOGS ----------------
with st.expander("📜 View Full Alert Logs"):
    if len(df) > 0:
        st.dataframe(
            df,
            use_container_width=True
        )

# ---------------- FOOTER ----------------
st.markdown("""
---
### 🔒 IDS Status: Active
Real-time packet monitoring | Port Scan Detection | SQLite Logging
""")
