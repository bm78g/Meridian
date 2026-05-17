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

    print("Discovered hosts:\n")

    hosts = []
    for _, received in res:
        hosts.append(received)
        print(f"IP: {received.psrc}\tMAC: {received.hwsrc}")

    mac_addrs = []
    for host in hosts:
        parsed_hwsrc = host.hwsrc.replace(":", "-")
        mac_addrs.append(parsed_hwsrc)

    with open(os.getenv("MAC_LOOKUP_DIR"), "r") as lookup_file:
        lookup_data = lookup_file.read()
        mac_dict = parse_lookup(lookup_data)

    mac_vendors = []
    for addr in mac_addrs:
        try:
            vendor = mac_dict[addr[0:8].upper()]
            mac_vendors.append((addr, vendor))
        except KeyError:
            mac_vendors.append((addr, "Unknown"))
        
    for mac_vendor in mac_vendors:
        print(mac_vendor)

if __name__ == "__main__":
    main()