from scapy.all import ARP, Ether, srp

target_subnet = "11.30.0.0/21"

arp = ARP(pdst=target_subnet)
ether = Ether(dst="ff:ff:ff:ff:ff:ff")

packet = ether / arp

res = srp(packet, timeout=2, verbose=1)[0]

print("Discovered hosts:\n")

for sent, received in res:
    print(f"IP: {received.psrc}\tMAC: {received.hwsrc}")