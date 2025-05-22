import tool.workflow
import types


class DummyResult:
    def __init__(self):
        self.stdout = "{}"
        self.stderr = ""
        self.returncode = 0


def dummy_runner(*args, **kwargs):
    return DummyResult()


def dummy_which(*args, **kwargs):
    return 0


def test_list():
    config = types.SimpleNamespace(project_dir=".")
    wf = tool.workflow.Workflow(
        config.project_dir, runner=dummy_runner, which=dummy_which
    )
    result = wf.run(["echo", "foo"])
    assert isinstance(result, str)
