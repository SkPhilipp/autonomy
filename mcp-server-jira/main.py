from mcp.server.fastmcp import FastMCP
import os
from atlassian import Jira

mcp = FastMCP("Jira Tools")

def get_env(name, required=True):
    """Get environment variable or exit if required and missing."""
    value = os.getenv(name)
    if required and not value:
        raise ValueError(f"Error: {name} environment variable is required but not set")
    return value

jira_base_issue = get_env("JIRA_BASE_ISSUE")
jira_url = get_env("JIRA_URL")
jira_api_token = get_env("JIRA_API_TOKEN")

jira = Jira(
    url=jira_url,
    token=jira_api_token
)

def get_required_fields(project_key, issue_type_id):
    """
    Get the list of required fields for an issue type in a project.
    
    Args:
        project_key: The project key
        issue_type_id: The issue type ID
        
    Returns:
        List of required field IDs
    """
    meta_endpoint = f"rest/api/2/issue/createmeta/{project_key}/issuetypes/{issue_type_id}"
    meta_response = jira.get(meta_endpoint)
    
    return [field["fieldId"] for field in meta_response.get("values", []) 
            if field.get("required", False)]

@mcp.tool()
def get_base_jira_issue() -> str:
    """
    Get a Jira issue title and description
    """
    issue = jira.issue(jira_base_issue)

    return {
        "title": issue["fields"]["summary"],
        "description": issue["fields"]["description"]
    }


@mcp.tool()
def create_jira_issue_from_base(new_title: str, new_description: str) -> str:
    """
    Creates a new issue with a given title and description, maintaining required fields from base issue.
    
    Args:
        new_title: The new title for the new issue
        new_description: The new description for the new issue
    
    Returns:
        A reference to the newly created issue
    """
    # Retrieve base issue and extract project/issue type info
    base_issue = jira.issue(jira_base_issue)
    project_key = base_issue["fields"]["project"]["key"]
    issue_type_id = base_issue["fields"]["issuetype"]["id"]
    
    # Get required fields for this issue type
    required_fields = get_required_fields(project_key, issue_type_id)
    
    # Initialize with mandatory fields
    new_issue_data = {
        "fields": {
            "project": {"key": project_key},
            "issuetype": {"id": issue_type_id},
            "summary": new_title,
            "description": new_description
        }
    }
    
    # Copy any additional required fields from the base issue
    for field_id in required_fields:
        if field_id not in new_issue_data["fields"] and field_id in base_issue["fields"]:
            new_issue_data["fields"][field_id] = base_issue["fields"][field_id]
    
    # Submit the issue creation request
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
