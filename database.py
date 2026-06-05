import sqlite3

conn = sqlite3.connect("logs.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS alerts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_ip TEXT,
    ports TEXT,
    risk_level TEXT
)
""")

conn.commit()

def save_alert(source_ip, ports,risk):

    cursor.execute(
        "INSERT INTO alerts (source_ip, ports, risk_level) VALUES (?, ?, ?)",
        (source_ip, str(ports), risk)
    )
    conn.commit()