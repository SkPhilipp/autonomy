import tool.browse
import subprocess
import pytest


class DummyResult:
    def __init__(self):
        self.stdout = "output"
        self.stderr = ""
        self.returncode = 0


def dummy_run(*args, **kwargs):
    return DummyResult()


def test_search_and_fetch():
    assert isinstance(tool.browse.search("test", runner=dummy_run), str)
    assert isinstance(tool.browse.fetch("http://example.com", runner=dummy_run), str)
