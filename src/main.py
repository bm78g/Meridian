from scapy.all import arping

def arp_scan():
    arping("11.30.0.0/21", iface="en0", verbose=True)

def main():
    arp_scan()

if __name__ == "__main__":
    main()