import sqlite3
from pathlib import Path
import pprint
import os
from dotenv import load_dotenv

load_dotenv()

def _compare_db(file1, file2):
    conn = sqlite3.connect(file1)
    cursor = conn.cursor()

    cursor.execute(f"ATTACH DATABASE '{file2}' AS old")

    cursor.execute("SELECT * FROM main.hosts EXCEPT SELECT * FROM old.hosts")
    host_added = cursor.fetchall()
    cursor.execute("SELECT * FROM old.hosts EXCEPT SELECT * FROM main.hosts")
    host_removed = cursor.fetchall()

    # cursor.execute("SELECT * FROM main.ports EXCEPT SELECT * FROM old.ports")
    # port_diff = cursor.fetchall()

    conn.close()
    return (host_added, host_removed)

def _fetch_pair(current):
    files = [f for f in Path(os.getenv("SNAPSHOT_DIR")).iterdir() if f.is_file()]
    files.sort()
    for i in range(len(files)):
        if files[i].name == current:
            if i == 0:
                return ("", "")
            else:
                return (str(files[i]), str(files[i - 1]))
    return ("", "")

def get_diff(filename):
    pair = _fetch_pair(filename)
    if pair[0] != "":
        diff = _compare_db(pair[0], pair[1])

        print("Host added: ")
        pprint.pprint(diff[0], width=20)

        print("Host removed: ")
        pprint.pprint(diff[1], width=20)

        print("")
    else:
        print("Comparison failed")