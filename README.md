# Intrusion Detection System (IDS)

A Python-based Intrusion Detection System that monitors network traffic, detects potential port scanning activities, stores alerts in SQLite, and visualizes incidents through a Streamlit dashboard.

## Features
- Real-time Packet Monitoring
- Port Scan Detection
- Risk Classification (Low, Medium, High)
- SQLite Alert Logging
- Interactive Streamlit Dashboard
- Risk Distribution Analytics
- Top Source IP Analysis

## Technologies Used
- Python
- Scapy
- Streamlit
- Plotly
- SQLite
- Npcap

## Run

pip install -r requirements.txt

python sniffer.py

streamlit run app.py
