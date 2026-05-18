import sqlite3
import pprint
import os
from dotenv import load_dotenv
from util.fileio import get_files

load_dotenv()

def _compare_db(file1, file2):
    conn = sqlite3.connect(file1)
    cursor = conn.cursor()

    cursor.execute(f"ATTACH DATABASE '{file2}' AS old")

    cursor.execute("SELECT * FROM main.hosts EXCEPT SELECT * FROM old.hosts")
    host_added = cursor.fetchall()
    cursor.execute("SELECT * FROM old.hosts EXCEPT SELECT * FROM main.hosts")
    host_removed = cursor.fetchall()

    conn.close()
    return (host_added, host_removed)

def _fetch_pair(current):
    files = get_files(os.getenv("SNAPSHOT_DIR"))
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
        
        return diff
    else:
        print("Comparison failed")