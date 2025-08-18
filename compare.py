#!/usr/bin/python3

def load_db(filename):
    """Load GUID → line mapping from gamecontrollerdb.txt"""
    mapping = {}
    with open(filename, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            guid, *rest = line.split(",", 1)
            mapping[guid] = line
    return mapping

file1 = "gamecontrollerdb.txt"
file2 = "add_gamecontrollerdb.txt"

db1 = load_db(file1)
db2 = load_db(file2)

common = set(db1.keys()) & set(db2.keys())

print(f"Found {len(common)} duplicate GUIDs\n")

for guid in sorted(common):
    line1 = db1[guid]
    line2 = db2[guid]
    print(f"GUID {guid}: DIFFERENT")
    print(f"  {file1}: {line1}")
    print(f"  {file2}: {line2}")
    print()
