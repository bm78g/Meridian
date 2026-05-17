from scapy.all import ARP, Ether, srp
import os
import sys
import pyfiglet
from pathlib import Path

from dotenv import load_dotenv
from util.vendor_lookup import lookup_vendors
from util.reverse_dns import search_hosts
from util.port_scan import scan_hosts
from util.host_db import store_hosts
from util.compare_db import get_diff

from models import Host

load_dotenv()
target_subnet = os.getenv("TARGET_SUBNET")

def monitor_network():
    # Send ARP broadcast
    arp = ARP(pdst=target_subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    packet = ether / arp

    while True:
        res = srp(packet, timeout=2, verbose=1)[0]

        print("\nDiscovered hosts:")
        for _, received in res:
            print(f"IP: {received.psrc}, MAC: {received.hwsrc}")

        print()

        nodes = []
        for _, received in res:
            nodes.append(received)

        # Node information aggregation
        vendors = lookup_vendors(nodes)
        dns = search_hosts(nodes)
        scan_result = scan_hosts(nodes)
            
        assert len(vendors) == len(dns) == len(scan_result)

        hosts = []
        for i in range(len(nodes)):
            host = Host(nodes[i].psrc, nodes[i].hwsrc)
            host.vendor = vendors[i]
            host.domain = dns[i]
            host.port_scan = scan_result[i]
            hosts.append(host)

        db_file = store_hosts(hosts)
        get_diff(db_file)

        # Remove old overflowing snapshots
        files = [f for f in Path(os.getenv("SNAPSHOT_DIR")).iterdir() if f.is_file()]
        max_count = os.getenv("MAX_SNAPSHOTS")
        if len(files) > int(max_count):
            files.sort()
            for i in range(len(files)):
                if len(files) - i > int(max_count):
                    os.remove(files[i])

        # Free memory after each scan
        for host in hosts:
            del host

def main():
    banner = pyfiglet.figlet_format("Meridian")
    print(banner)

    while True:
        choice = input("Select an operation:\n1) Monitor network\n2) Exit program\n")
        match choice:
            case "1":
                monitor_network()
                break
            case "2":
                print("Exiting program...")
                sys.exit(0)
            case _:
                print("Please enter a valid choice")

if __name__ == "__main__":
    main()