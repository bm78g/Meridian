import sqlite3

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

compare_db("data/2026-5-17_15-26-6.db", "data/2026-5-17_15-14-6.db")