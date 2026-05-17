import sqlite3

def store_host(host):
    conn = sqlite3.connect("data/network_topology.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS HOSTS (mac CHAR(17), ipv4 VARCHAR(15), vendor VARCHAR(64))")

store_host(None)