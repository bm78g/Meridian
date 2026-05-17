import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def _store_host(host, conn):
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

def store_hosts(hosts):
    now = datetime.now()
    timestamp = f"{now.year}-{now.month:02}-{now.day:02}_{now.hour:02}-{now.minute:02}-{now.second:02}"
    conn = sqlite3.connect(f"{os.getenv("SNAPSHOT_DIR")}/{timestamp}.db", timeout=5)

    for host in hosts:
        _store_host(host, conn)

    conn.commit()
    conn.close()
    print("Data successfully stored")
    return f"{timestamp}.db"