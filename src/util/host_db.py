import sqlite3

def store_host(host):
    conn = sqlite3.connect("data/network_topology.db", timeout=5)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS hosts (mac CHAR(17) PRIMARY KEY, ipv4 VARCHAR(15)," \
        "vendor VARCHAR(64), domain VARCHAR(64))")
    cursor.execute("CREATE TABLE IF NOT EXISTS ports (port INTEGER, mac CHAR(17)," \
        "state VARCHAR(16), name VARCHAR(16), product VARCHAR(32), version VARCHAR(16)," \
        "FOREIGN KEY (mac) REFERENCES hosts(mac))")
    
    cursor.execute("INSERT INTO hosts (mac, ipv4, vendor, domain) VALUES (?, ?, ?, ?)",
                   (host.mac, host.ip, host.vendor, host.domain))

    for port in host.port_scan:
        cursor.execute("INSERT INTO ports (port, mac, state, name, product, version) VALUES (?, ?, ?, ?, ?, ?)",
                       (port["port"], host.mac, port["state"], port["name"], port["product"], port["version"]))

    conn.commit()
    conn.close()

def store_hosts(hosts):
    for host in hosts:
        store_host(host)
    print("Data successfully stored")