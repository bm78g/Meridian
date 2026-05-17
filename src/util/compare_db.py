import sqlite3
from pathlib import Path

def compare_db(file1, file2):
    conn = sqlite3.connect(file1)
    cursor = conn.cursor()

    cursor.execute(f"ATTACH DATABASE '{file2}' AS old")

    cursor.execute("SELECT * FROM main.hosts EXCEPT SELECT * FROM old.hosts")
    host_added = cursor.fetchall()
    cursor.execute("SELECT * FROM old.hosts EXCEPT SELECT * FROM main.hosts")
    host_removed = cursor.fetchall()

    cursor.execute("SELECT * FROM main.ports EXCEPT SELECT * FROM old.ports")
    port_diff = cursor.fetchall()

    print(host_added)
    print(host_removed)
    print(port_diff)

    conn.close()

def get_prev(current):
    files = [f for f in Path('./data/network_snapshot').iterdir() if f.is_file()]
    files.sort()
    for i in range(len(files)):
        if files[i].name == current:
            if i == 0:
                return ""
            else:
                return files[i - 1]
    return ""

# compare_db("data/2026-5-17_15-30-33.db", "data/2026-5-17_15-14-6.db")
print(get_prev("2026-05-17_15-38-42.db"))