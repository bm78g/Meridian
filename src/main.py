from scapy.all import *
import os
from dotenv import load_dotenv
from vendor_lookup import lookup_vendors
from reverse_dns import *

load_dotenv()
target_subnet = os.getenv("TARGET_SUBNET")

def main():
    arp = ARP(pdst=target_subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    packet = ether / arp

    res = srp(packet, timeout=2, verbose=1)[0]

    print()

    hosts = []
    for _, received in res:
        hosts.append(received)

    vendors = lookup_vendors(hosts)
    dns = search_hosts(hosts)
        
    print(vendors)
    print(dns)

if __name__ == "__main__":
    main()