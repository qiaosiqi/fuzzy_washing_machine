# db.py
# SQLite 数据库读写模块
import sqlite3
from datetime import datetime

DB_FILE = 'fuzzy_washer.db'

def get_conn():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS records (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      sludge REAL NOT NULL,
      grease REAL NOT NULL,
      algorithm TEXT NOT NULL,
      defuzz TEXT NOT NULL,
      result_time REAL NOT NULL,
      linguistic TEXT NOT NULL,
      created_at TEXT NOT NULL
    );
    ''')
    conn.commit()
    conn.close()

def insert_record(sludge, grease, algorithm, defuzz, result_time, linguistic):
    conn = get_conn()
    c = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    c.execute('''
      INSERT INTO records (sludge, grease, algorithm, defuzz, result_time, linguistic, created_at)
      VALUES (?, ?, ?, ?, ?, ?, ?);
    ''', (sludge, grease, algorithm, defuzz, result_time, linguistic, created_at))
    conn.commit()
    lid = c.lastrowid
    conn.close()
    return lid

def query_all(limit=200):
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT id, sludge, grease, algorithm, defuzz, result_time, linguistic, created_at FROM records ORDER BY created_at DESC LIMIT ?;', (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def delete_record(record_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute('DELETE FROM records WHERE id = ?;', (record_id,))
    conn.commit()
    conn.close()

def update_record(record_id, sludge, grease, algorithm, defuzz, result_time, linguistic):
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
      UPDATE records SET sludge=?, grease=?, algorithm=?, defuzz=?, result_time=?, linguistic=? WHERE id=?;
    ''', (sludge, grease, algorithm, defuzz, result_time, linguistic, record_id))
    conn.commit()
    conn.close()
