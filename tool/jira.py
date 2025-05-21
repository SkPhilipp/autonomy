import os
from atlassian import Jira

def get_jira(config):
    return Jira(
        url=config.jira_url,
        token=config.jira_api_token
    )

def get_required_fields(jira, project_key, issue_type_id):
    meta_endpoint = f"rest/api/2/issue/createmeta/{project_key}/issuetypes/{issue_type_id}"
    meta_response = jira.get(meta_endpoint)
    return [field["fieldId"] for field in meta_response.get("values", []) 
            if field.get("required", False)]

def get_base_jira_issue(config) -> dict:
    jira = get_jira(config)
    issue = jira.issue(config.jira_base_issue)
    return {
        "title": issue["fields"]["summary"],
        "description": issue["fields"]["description"]
    }

def create_jira_issue_from_base(new_title: str, new_description: str, config) -> dict:
    jira = get_jira(config)
    base_issue = jira.issue(config.jira_base_issue)
    project_key = base_issue["fields"]["project"]["key"]
    issue_type_id = base_issue["fields"]["issuetype"]["id"]
    required_fields = get_required_fields(jira, project_key, issue_type_id)
    new_issue_data = {
        "fields": {
            "project": {"key": project_key},
            "issuetype": {"id": issue_type_id},
            "summary": new_title,
            "description": new_description
        }
    }
    for field_id in required_fields:
        if field_id not in new_issue_data["fields"] and field_id in base_issue["fields"]:
            new_issue_data["fields"][field_id] = base_issue["fields"][field_id]
    try:
        new_issue = jira.post("rest/api/2/issue", data=new_issue_data)
        return {
            "success": True,
            "issue_key": new_issue["key"],
            "issue_id": new_issue["id"]
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to create issue: {str(e)}"
        }
