from scapy.all import ARP, Ether, srp
import os
from dotenv import load_dotenv
from util.vendor_lookup import lookup_vendors
from util.reverse_dns import *
from util.port_scan import scan_hosts, scan_hosts_legacy
from models import Host
from datetime import datetime

load_dotenv()
target_subnet = os.getenv("TARGET_SUBNET")

def get_scan_time(legacy=False, hosts=[]):
    start_time = datetime.now()
    if legacy:
        scan_hosts_legacy(hosts)
        print("Legacy scan ", end="")
    else:
        scan_hosts(hosts)
        print("Concurrent scan ", end="")
    end_time = datetime.now()
    delta = end_time - start_time
    print(f"elapsed {delta}")

def main():
    # Send ARP broadcast
    arp = ARP(pdst=target_subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    packet = ether / arp

    res = srp(packet, timeout=2, verbose=1)[0]

    print()
    for _, received in res:
        print(f"IP: {received.psrc}, MAC: {received.hwsrc}")

    nodes = []
    for _, received in res:
        nodes.append(received)

    # Node information aggregation
    vendors = lookup_vendors(nodes)
    dns = search_hosts(nodes)

    get_scan_time(True, nodes)
    get_scan_time(False, nodes)
        
    # assert len(vendors) == len(dns) == len(scan_result)

    # hosts = []
    # for i in range(len(nodes)):
    #     host = Host(nodes[i].psrc, nodes[i].hwsrc)
    #     host.vendor = vendors[i]
    #     host.domain = dns[i]
    #     host.port_scan = scan_result[i]
    #     hosts.append(host)

    # for host in hosts:
    #     print(vars(host))

if __name__ == "__main__":
    main()