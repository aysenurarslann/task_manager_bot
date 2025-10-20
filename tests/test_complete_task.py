import pytest
import tempfile
from pathlib import Path
from database import init_db, add_task, complete_task, is_task_completed, get_all_tasks, DB_PATH

def test_complete_valid_task(monkeypatch):
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    monkeypatch.setattr("database.DB_PATH", tmp_path)
    init_db()
    tid = add_task("Tamamlanacak görev")
    assert complete_task(tid) is True
    assert is_task_completed(tid) is True
    tmp_path.unlink()

def test_complete_already_completed_task(monkeypatch):
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    monkeypatch.setattr("database.DB_PATH", tmp_path)
    init_db()
    tid = add_task("Zaten tamamlanmış görev")
    complete_task(tid)
    assert complete_task(tid) is False
    tmp_path.unlink()

def test_complete_nonexistent_task(monkeypatch):
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    monkeypatch.setattr("database.DB_PATH", tmp_path)
    init_db()
    assert complete_task(99999) is False
    tmp_path.unlink()