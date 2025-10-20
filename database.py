# database.py
import sqlite3
from pathlib import Path

DB_PATH = Path("tasks.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def add_task(description):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (description, completed) VALUES (?, ?)", (description, False))
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id

def delete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    changed = cursor.rowcount
    conn.commit()
    conn.close()
    return changed > 0

def get_all_tasks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, completed FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "description": r[1], "completed": bool(r[2])} for r in rows]

def complete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ? AND completed = 0", (task_id,))
    changed = cursor.rowcount
    conn.commit()
    conn.close()
    return changed > 0

def is_task_completed(task_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT completed FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    return bool(row[0]) if row else False