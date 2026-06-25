import sqlite3

conn = sqlite3.connect("resume_analyzer.db")

cursor = conn.cursor()

cursor.execute(
    "SELECT * FROM analysis_history"
)

rows = cursor.fetchall()

print("Total Records:", len(rows))

for row in rows:
    print(row)

conn.close()