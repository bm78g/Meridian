import nmap
from concurrent.futures import ThreadPoolExecutor

ports = [21, 22, 25, 53, 80, 443, 3306, 3389, 5432, 8080]

def scan_ports(target):
    port_str = ','.join(str(p) for p in ports)
    scanner = nmap.PortScanner()
    res = scanner.scan(target, port_str, arguments='-sV')
    
    result = []
    tcp_data = res['scan'].get(target, {}).get('tcp', {})
    for port in ports:
        info = tcp_data.get(port, {})
        result.append({
            "port": port,
            "state": info.get('state', 'unknown'),
            "name": info.get('name', ''),
            "product": info.get('product', ''),
            "version": info.get('version', '')
        })
    return result

def scan_hosts(hosts):
    hosts = [host.psrc for host in hosts]
    with ThreadPoolExecutor(len(hosts)) as exec:
        scan_results = list(exec.map(scan_ports, hosts))
        return scan_results
    return []

def scan_hosts_legacy(hosts):
    return [scan_ports(host.psrc) for host in hosts]