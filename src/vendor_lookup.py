import re
import os
from dotenv import load_dotenv

load_dotenv()

# Returns a dictionary of first 6 digits of MAC to vendor
def parse_lookup(lookup_data):
    pattern = r"[a-zA-Z0-9]{2}-[a-zA-Z0-9]{2}-[a-zA-Z0-9]{2}"
    split_data = lookup_data.replace("\n", "\t").split("\t")
    parsed = {}

    for i in range(len(split_data)):
        matched = bool(re.search(pattern, split_data[i]))
        if matched:
            parsed[split_data[i][0:8]] = split_data[i + 2]

    return parsed

def lookup_vendor(hosts):
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

    return host_data