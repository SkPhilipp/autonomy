from core.config import get_required_env, Config


def test_config_from_env(monkeypatch, tmp_path):
    monkeypatch.setenv("JIRA_URL", "url")
    monkeypatch.setenv("JIRA_USERNAME", "user")
    monkeypatch.setenv("JIRA_API_TOKEN", "token")
    monkeypatch.setenv("JIRA_IS_CLOUD", "cloud")
    monkeypatch.setenv("GH_TOKEN", "ghtoken")
    monkeypatch.setenv("PROJECT_DIR", str(tmp_path))
    monkeypatch.setenv("JIRA_BASE_ISSUE", "ISSUE-1")

    class Args:
        env = None
        project_path = None

    c = Config.from_env(Args())
    assert c.jira_url == "url"
    assert c.jira_username == "user"
    assert c.jira_api_token == "token"
    assert c.jira_is_cloud == "cloud"
    assert c.gh_token == "ghtoken"
    assert c.project_dir == str(tmp_path)
    assert c.jira_base_issue == "ISSUE-1"
