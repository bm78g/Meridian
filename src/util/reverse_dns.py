import socket

def _reverse_dns(ip):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except socket.herror:
        return "Unknown"

def search_hosts(hosts):
    dns = []
    for host in hosts:
        dns.append(_reverse_dns(host.psrc))
    return dns