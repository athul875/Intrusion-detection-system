from scapy.all import sniff, IP, TCP
from detector import detect_port_scan

def packet_callback(packet):
    if packet.haslayer(IP) and packet.haslayer(TCP):

        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport

        print(
            f"[TCP] {src_ip}:{src_port} --> "
            f"{dst_ip}:{dst_port}"
        )

        detect_port_scan(src_ip, dst_port)

print("=" * 50)
print("      IDS Started")
print("=" * 50)

sniff(prn=packet_callback, store=False)