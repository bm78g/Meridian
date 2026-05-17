from scapy.all import *
import os
from dotenv import load_dotenv
from util.vendor_lookup import lookup_vendors
from util.reverse_dns import *
from util.port_scan import scan_hosts

load_dotenv()
target_subnet = os.getenv("TARGET_SUBNET")

def main():
    arp = ARP(pdst=target_subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    packet = ether / arp

    res = srp(packet, timeout=2, verbose=1)[0]

    print()
    for _, received in res:
        print(f"IP: {received.psrc}, MAC: {received.hwsrc}")

    hosts = []
    for _, received in res:
        hosts.append(received)

    vendors = lookup_vendors(hosts)
    dns = search_hosts(hosts)
    scan_result = scan_hosts(hosts)
        
    assert len(vendors) == len(dns) == len(scan_result)

if __name__ == "__main__":
    main()