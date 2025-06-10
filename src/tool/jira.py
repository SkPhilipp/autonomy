import os
from atlassian import Jira


def get_jira(config):
    return Jira(url=config.jira_url, token=config.jira_api_token)


def get_required_fields(jira, project_key, issue_type_id):
    meta_endpoint = (
        f"rest/api/2/issue/createmeta/{project_key}/issuetypes/{issue_type_id}"
    )
    meta_response = jira.get(meta_endpoint)
    return [
        field["fieldId"]
        for field in meta_response.get("values", [])
        if field.get("required", False)
    ]


def get_base_issue(config, jira_factory=get_jira) -> dict:
    jira = jira_factory(config)
    issue = jira.issue(config.jira_base_issue)
    return {
        "title": issue["fields"]["summary"],
        "description": issue["fields"]["description"],
    }


def create_issue_from_base(
    title: str, description: str, config, jira_factory=get_jira
) -> dict:
    jira = jira_factory(config)
    base_issue = jira.issue(config.jira_base_issue)
    project_key = base_issue["fields"]["project"]["key"]
    issue_type_id = base_issue["fields"]["issuetype"]["id"]
    required_fields = get_required_fields(jira, project_key, issue_type_id)
    new_issue_data = {
        "fields": {
            "project": {"key": project_key},
            "issuetype": {"id": issue_type_id},
            "summary": title,
            "description": description,
        }
    }
    for field_id in required_fields:
        if (
            field_id not in new_issue_data["fields"]
            and field_id in base_issue["fields"]
        ):
            new_issue_data["fields"][field_id] = base_issue["fields"][field_id]
    try:
        new_issue = jira.post("rest/api/2/issue", data=new_issue_data)
        return {
            "success": True,
            "issue_key": new_issue["key"],
            "issue_id": new_issue["id"],
        }
    except Exception as e:
        return {"success": False, "error": f"Failed to create issue: {str(e)}"}


def get_epic_stories(epic_key: str, config, jira_factory=get_jira) -> dict:
    """Retrieve all Issues in an Epic."""
    jira = jira_factory(config)
    try:
        # Search for all issues that belong to this epic
        jql = f'"Epic Link" = {epic_key}'
        issues = jira.jql(jql)

        stories = []
        for issue in issues.get("issues", []):
            stories.append(
                {
                    "key": issue["key"],
                    "title": issue["fields"]["summary"],
                    "status": issue["fields"]["status"]["name"],
                    "issue_type": issue["fields"]["issuetype"]["name"],
                }
            )

        return {
            "success": True,
            "epic_key": epic_key,
            "total_issues": len(stories),
            "stories": stories,
        }
    except Exception as e:
        return {"success": False, "error": f"Failed to retrieve epic stories: {str(e)}"}


def get_story_content(story_key: str, config, jira_factory=get_jira) -> dict:
    """Retrieve the description, title and comments for a story."""
    jira = jira_factory(config)
    try:
        issue = jira.issue(story_key)

        comment_list = []
        try:
            # Attempt to get comments
            comments_data = jira.issue_get_comments(story_key)
            for comment in comments_data.get("comments", []):
                comment_list.append(
                    {
                        "author": comment["author"]["displayName"],
                        "created": comment["created"],
                        "body": comment["body"],
                    }
                )
        except AttributeError:
            # If comment retrieval fails, proceed without them.
            pass

        return {
            "success": True,
            "key": story_key,
            "title": issue["fields"]["summary"],
            "description": issue["fields"]["description"] or "",
            "status": issue["fields"]["status"]["name"],
            "issue_type": issue["fields"]["issuetype"]["name"],
            "comments": comment_list,
        }
    except Exception as e:
        import traceback

        error_details = traceback.format_exc()
        return {
            "success": False,
            "error": f"Failed to retrieve story content: {str(e)}",
            "details": error_details,
        }
