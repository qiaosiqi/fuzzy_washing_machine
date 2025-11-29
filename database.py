# database.py
import sqlite3

DB_NAME = "washing_records.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS records(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sludge REAL,
            grease REAL,
            result REAL
        )
    """)
    conn.commit()
    conn.close()


def insert_record(sludge, grease, result):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO records(sludge, grease, result) VALUES (?, ?, ?)",
              (sludge, grease, result))
    conn.commit()
    conn.close()


def fetch_records():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM records")
    rows = c.fetchall()
    conn.close()
    return rows


def delete_record(record_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM records WHERE id=?", (record_id,))
    conn.commit()
    conn.close()
