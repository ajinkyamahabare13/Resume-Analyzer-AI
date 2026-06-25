import sqlite3

conn = sqlite3.connect("resume_analyzer.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE analysis_history (
id INTEGER PRIMARY KEY AUTOINCREMENT,
filename TEXT,
match_score INTEGER,
skills TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")
