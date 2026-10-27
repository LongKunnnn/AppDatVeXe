import sqlite3

conn = sqlite3.connect("database/vexe.db")
c = conn.cursor()
tables = [row[0] for row in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print("Tables in vexe.db:", tables)

for t in ["nhaxe", "loaixe", "xe", "tuyenxe", "chuyenxe", "taixe", "ve"]:
    if t in tables:
        count = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"Table '{t}': {count} rows")
conn.close()

