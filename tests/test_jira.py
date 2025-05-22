import tool.jira
import types


class DummyJira:
    def issue(self, key):
        return {
            "fields": {
                "summary": "s",
                "description": "d",
                "project": {"key": "P"},
                "issuetype": {"id": "1"},
            }
        }

    def get(self, endpoint):
        return {"values": []}

    def post(self, endpoint, data=None):
        return {"key": "P-1", "id": "1"}


def dummy_get_jira(config):
    return DummyJira()


def test_get_base_issue():
    config = types.SimpleNamespace(jira_base_issue="P-1")
    result = tool.jira.get_base_issue(config, jira_factory=dummy_get_jira)
    assert "title" in result and "description" in result


def test_create_issue_from_base():
    config = types.SimpleNamespace(jira_base_issue="P-1")
    result = tool.jira.create_issue_from_base(
        "t", "d", config, jira_factory=dummy_get_jira
    )
    assert result["success"] is True
    assert "issue_key" in result
