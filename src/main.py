from scapy.all import *
import os
from dotenv import load_dotenv
import re

load_dotenv()
target_subnet = os.getenv("TARGET_SUBNET")

def parse_lookup(lookup_data):
    pattern = r"[a-zA-Z0-9]{2}-[a-zA-Z0-9]{2}-[a-zA-Z0-9]{2}"
    split_data = lookup_data.replace("\n", "\t").split("\t")
    parsed = {}

    for i in range(len(split_data)):
        matched = bool(re.search(pattern, split_data[i]))
        if matched:
            parsed[split_data[i][0:8]] = split_data[i + 2]

    return parsed

def main():
    arp = ARP(pdst=target_subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    packet = ether / arp

    res = srp(packet, timeout=2, verbose=1)[0]

    print()

    # Discovered hosts
    hosts = []
    for _, received in res:
        hosts.append(received)

    # Parse vendor lookup data into a dict
    with open(os.getenv("MAC_LOOKUP_DIR"), "r") as lookup_file:
        lookup_data = lookup_file.read()
        mac_dict = parse_lookup(lookup_data)

    # Compile host data
    host_data = []
    for host in hosts:
        f_mac = host.hwsrc.replace(":", "-")
        try:
            vendor = mac_dict[f_mac.upper()[0:8]]
        except KeyError:
            vendor = "Unknown"
        host_data.append((host.psrc, host.hwsrc, vendor))
        
    for data in host_data:
        print(data)

if __name__ == "__main__":
    main()