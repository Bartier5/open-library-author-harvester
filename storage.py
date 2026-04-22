import sqlite3
from config import DB_FILE

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn
def initialize_db():
    conn = get_connection()
    with conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS books(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         title TEXT NOT NULL,
                         author TEXT,
                         publish_year INTEGER,
                         subject TEXT,
                         isbn TEXT,
                         UNIQUE(title, author)
                         )
                         """)
        conn.execute("""CREATE TABLE IF NOT EXISTS progress (
                subject     TEXT PRIMARY KEY,
                last_page   INTEGER DEFAULT 0,
                completed   INTEGER DEFAULT 0 
                )
                """)
    conn.close()
    print("Database ready")
def save_books(records: list[dict]):
    conn = get_connection()
    with conn:
        conn.executemany("""INSERT OR IGNORE INTO books
                    (title, author, publish_year, subject, isbn)
            VALUES
                (:title, :author, :publish_year, :subject, :isbn)
        """, records)
    conn.close()
def save_checkpoint(subject: str, page:int ):
    conn = get_connection()
    with conn:
        conn.execute("""INSERT INTO progress (subject, last_page, completed)
                     VALUES (?,?,0)
                     ON CONFLICT(subject) DO NOT UPDATE SET last_page = ?""",
                     (subject, page, page))
    conn.close()
def mark_subject_complete(subject:str):
    conn = get_connection()
    with conn:
        conn.execute("""UPDATE progress SET completed = 1 WHERE subject = ? 
                     """,(subject,))
    conn.close()
def get_checkpoint(subject: str) -> int:
    conn = get_connection()
    with conn:
       row = conn.execute("""SELECT last_page, completed FROM progress WHERE subject = ?
                     """,(subject,)).fetchone()
    conn.close()
    if row is None:
        return 0
    if row["completed"]:
        return -1
    return row["last_page"]
def get_total_records() -> int:
    conn = get_connection()
    count = conn.execute("SELET COUNT(*) FROM books").fetchone()[0]
    conn.close()
    return count