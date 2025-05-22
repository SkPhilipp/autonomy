import tool.formatter
import subprocess
import json


class DummyResult:
    def __init__(self):
        self.stdout = "output"
        self.stderr = ""
        self.returncode = 0


def dummy_run(*args, **kwargs):
    return DummyResult()


class DummyConfig:
    project_dir = "."


def test_black():
    result = tool.formatter.black(DummyConfig(), runner=dummy_run)
    data = json.loads(result)
    assert "stdout" in data
    assert "stderr" in data
    assert "return_code" in data
