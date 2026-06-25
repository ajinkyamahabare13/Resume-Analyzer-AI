import sqlite3

conn = sqlite3.connect("resume_analyzer.db")

cursor = conn.cursor()

cursor.execute("PRAGMA table_info(analysis_history)")

for row in cursor.fetchall():
    print(row)

conn.close()