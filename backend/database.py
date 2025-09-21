import sqlite3
from sqlite3 import Connection

DB_NAME = "resumefilterer.db"

def get_connection() -> Connection:
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Resumes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT,
        raw_text TEXT,
        normalized_text TEXT,
        name TEXT,
        email TEXT,
        skills TEXT
    )
    """)

    # Job Descriptions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_descriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT,
        text_content TEXT,
        normalized_text TEXT
    )
    """)

    # Match Results table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resume_id INTEGER,
        jd_id INTEGER,
        hard_score REAL,
        soft_score REAL,
        verdict TEXT,
        FOREIGN KEY(resume_id) REFERENCES resumes(id),
        FOREIGN KEY(jd_id) REFERENCES job_descriptions(id)
    )
    """)

    conn.commit()
    conn.close()
