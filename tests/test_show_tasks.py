import pytest
import tempfile
from pathlib import Path
from database import init_db, add_task, get_all_tasks, DB_PATH

def test_show_empty_tasks(monkeypatch):
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    monkeypatch.setattr("database.DB_PATH", tmp_path)
    init_db()
    tasks = get_all_tasks()
    assert tasks == []
    tmp_path.unlink()

def test_show_multiple_tasks(monkeypatch):
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    monkeypatch.setattr("database.DB_PATH", tmp_path)
    init_db()
    add_task("Görev 1")
    add_task("Görev 2")
    tasks = get_all_tasks()
    assert len(tasks) == 2
    assert tasks[0]["description"] == "Görev 1"
    assert tasks[1]["description"] == "Görev 2"
    tmp_path.unlink()