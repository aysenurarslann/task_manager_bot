import pytest
import tempfile
from pathlib import Path
from database import init_db, add_task, delete_task, get_all_tasks, DB_PATH

def test_delete_existing_task(monkeypatch):
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    monkeypatch.setattr("database.DB_PATH", tmp_path)
    init_db()
    tid = add_task("Silinmeye aday görev")
    assert delete_task(tid) is True
    assert len(get_all_tasks()) == 0
    tmp_path.unlink()

def test_delete_nonexistent_task(monkeypatch):
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    monkeypatch.setattr("database.DB_PATH", tmp_path)
    init_db()
    assert delete_task(99999) is False
    tmp_path.unlink()