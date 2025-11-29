# db.py
import sqlite3, json, datetime
DB="fuzzy_runs.db"

def init_db(path=DB):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT,
        sludge REAL,
        grease REAL,
        method TEXT,
        mf_kind TEXT,
        defuzz TEXT,
        result REAL,
        firing TEXT
    )''')
    conn.commit(); conn.close()

def save_run(sludge, grease, method, mf_kind, defuzz, result, firings, path=DB):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("INSERT INTO runs (ts,sludge,grease,method,mf_kind,defuzz,result,firing) VALUES (?,?,?,?,?,?,?,?)",
              (datetime.datetime.now().isoformat(), sludge, grease, method, mf_kind, defuzz, result, json.dumps(firings)))
    conn.commit(); conn.close()

def list_runs(limit=50, path=DB):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("SELECT id,ts,sludge,grease,method,mf_kind,defuzz,result FROM runs ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall(); conn.close(); return rows

def get_run(run_id, path=DB):
    conn = sqlite3.connect(path); c=conn.cursor()
    c.execute("SELECT * FROM runs WHERE id=?", (run_id,))
    r = c.fetchone(); conn.close(); return r

def delete_run(run_id, path=DB):
    conn = sqlite3.connect(path); c=conn.cursor()
    c.execute("DELETE FROM runs WHERE id=?", (run_id,)); conn.commit(); conn.close()
