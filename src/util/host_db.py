import sqlite3

def store_host(host):
    conn = sqlite3.connect("data/network_topology.db", timeout=5)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS hosts (mac CHAR(17) PRIMARY KEY, ipv4 VARCHAR(15), vendor VARCHAR(64))")
    cursor.execute("INSERT INTO hosts (mac, ipv4, vendor) VALUES (?, ?, ?)", (host.mac, host.ip, host.vendor))

    conn.commit()
    conn.close()

def store_hosts(hosts):
    for host in hosts:
        store_host(host)