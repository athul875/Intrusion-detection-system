from collections import defaultdict
from database import save_alert

ip_ports = defaultdict(set)

def detect_port_scan(src_ip, dst_port):

    ip_ports[src_ip].add(dst_port)

    port_count = len(ip_ports[src_ip])

    if port_count >= 3:

        if port_count >= 10:
            risk = "HIGH"
        elif port_count >= 5:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        save_alert(src_ip, sorted(ip_ports[src_ip]), risk)

        print("\n" + "=" * 50)
        print("[ALERT] Possible Port Scan Detected!")
        print(f"Source IP: {src_ip}")
        print(f"Ports Accessed: {sorted(ip_ports[src_ip])}")
        print(f"Risk Level: {risk}")
        print("=" * 50 + "\n")