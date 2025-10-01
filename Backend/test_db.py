import sqlite3
import pickle  # For serializing vectors as binary

DB_FILE = 'green_jobs.db'  # File in backend folder

try:
    conn = sqlite3.connect(DB_FILE)
    print("Connected to SQLite!")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skills_vectors (
            id INTEGER PRIMARY KEY,
            skill_text TEXT,
            embedding BLOB
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs_vectors (
            id INTEGER PRIMARY KEY,
            job_title TEXT,
            job_description TEXT,
            embedding BLOB
        )
    """)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables:", tables)
    conn.close()
except Exception as e:
    print(f"Error: {e}")