import pytest
import tempfile
from pathlib import Path
from database import init_db, add_task, get_all_tasks, DB_PATH

def test_add_valid_task(monkeypatch):
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    monkeypatch.setattr("database.DB_PATH", tmp_path)
    init_db()
    task_id = add_task("Test görevi")
    tasks = get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0]["description"] == "Test görevi"
    assert tasks[0]["completed"] is False
    assert tasks[0]["id"] == task_id
    tmp_path.unlink()

def test_add_empty_task_description(monkeypatch):
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    monkeypatch.setattr("database.DB_PATH", tmp_path)
    init_db()
    task_id = add_task("")
    tasks = get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0]["description"] == ""
    tmp_path.unlink()