from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP
from scapy.packet import Raw # Import Raw layer for payloads

def process_packet(packet):
    if packet.haslayer(IP):
        ip_layer = packet[IP]
        src_ip = ip_layer.src
        dst_ip = ip_layer.dst
        
        protocol = "IP"
        src_port = ""
        dst_port = ""
        
        if packet.haslayer(TCP):
            tcp_layer = packet[TCP]
            protocol = "TCP"
            src_port = tcp_layer.sport
            dst_port = tcp_layer.dport
        elif packet.haslayer(UDP):
            udp_layer = packet[UDP]
            protocol = "UDP"
            src_port = udp_layer.sport
            dst_port = udp_layer.dport

        # Check if the packet contains a RAW payload (the data layer)
        if packet.haslayer(Raw):
            # Extract and decode the payload bytes to a string safely
            payload = packet[Raw].load.decode('utf-8', errors='ignore')
            
            # Keywords to search for (typical form field names for credentials)
            keywords = ["username=", "password=", "login=", "passwd="]
            
            # Check if any keyword exists in the payload
            if any(keyword in payload.lower() for keyword in keywords):
                print("\n" + "!" * 60)
                print("[⚠️] SECURITY WARNING: Plaintext credentials detected over the network!")
                print(f"[*] Route: {src_ip}:{src_port} -> {dst_ip}:{dst_port}")
                print(f"[*] Intercepted Payload Data: {payload.strip()}")
                print("!" * 60 + "\n")
            else:
                # Print normal traffic
                if src_port and dst_port:
                    print(f"[{protocol}] {src_ip}:{src_port} -> {dst_ip}:{dst_port}")

print("[*] Starting Parsed Sniffer with Security Audit Mode...")
print("[*] Monitoring network... (Press Ctrl+C to stop)")

# Sniff specifically on the Realtek adapter (Index 17)
sniff(prn=process_packet, store=False, iface="Software Loopback Interface 1")