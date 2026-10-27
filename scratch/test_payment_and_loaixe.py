import urllib.request
import json
import sqlite3
import os

DB_PATH = "database/vexe.db"

# Direct DB test first
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Check tables
c.execute("SELECT count(*) FROM loaixe")
print(f"Total Loaixe in DB: {c.fetchone()[0]}")

c.execute("SELECT count(*) FROM ve")
print(f"Total Ve in DB: {c.fetchone()[0]}")

conn.close()
print("DB connection verified successfully!")

