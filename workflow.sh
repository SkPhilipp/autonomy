#!/bin/bash

# Exit on error
set -e

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if gh CLI is installed
if ! command_exists gh; then
    echo "GitHub CLI (gh) is not installed. Please install it first:"
    echo "https://cli.github.com/manual/installation"
    exit 1
fi

# Check if user is authenticated with GitHub
gh auth status >/dev/null 2>&1 || {
    echo "Please authenticate with GitHub first using: gh auth login"
    exit 1
}

# Function to list open issues
list_issues() {
    # Get open issues with basic information
    gh issue list --state open --json number,title,labels,createdAt --limit 100 | \
    jq -r '.[] | 
        select(.labels[].name != "blocked" and .labels[].name != "needs discussion") |
        {
            number: .number,
            title: .title,
            priority: (
                if (.labels[].name == "bug") then 1
                elif (.labels[].name == "documentation") then 2
                elif (.labels[].name == "enhancement") then 3
                else 4
                end
            ),
            created: .createdAt
        } | [.number, .title, .priority, .created] | @tsv' | \
    sort -t$'\t' -k3,3n -k4,4 | \
    cut -f1,2 | \
    sed 's/\t/ - /'
}

# Function to start work on an issue
start_issue() {
    if [ -z "$1" ]; then
        echo "Usage: ./workflow.sh start-issue <issue-number>"
        exit 1
    fi
    
    local issue_number=$1
    local issue_title=$(gh issue view "$issue_number" --json title --jq .title)
    local branch_type="fix"
    
    # Check if it's a feature issue
    if [[ "$issue_title" =~ ^\[feature\] ]]; then
        branch_type="feature"
    fi
    
    # Reset to clean state from origin/master
    git fetch origin
    git reset --hard origin/master
    git clean -fd
    
    local branch_name="${branch_type}/issue-${issue_number}"
    git checkout -b "$branch_name"
    git push -u origin "$branch_name"
}

# Function to push changes
commit_and_push() {
    if [ -z "$1" ]; then
        echo "Usage: ./workflow.sh commit-and-push <commit-message>"
        exit 1
    fi
    
    local commit_message="$1"
    local branch_name=$(git rev-parse --abbrev-ref HEAD)
    
    git add .
    git commit -m "$commit_message"
    git push -u origin "$branch_name"
}

# Function to monitor CI/CD
monitor_ci() {
    if [ -z "$1" ]; then
        echo "Usage: ./workflow.sh monitor-ci <pr-number>"
        exit 1
    fi
    
    local pr_number=$1
    gh pr checks "$pr_number" --watch
}

# Function to complete work on an issue
complete_issue() {
    if [ -z "$1" ] || [ -z "$2" ]; then
        echo "Usage: ./workflow.sh complete-issue <pr-number> <issue-number>"
        exit 1
    fi
    
    local pr_number=$1
    local issue_number=$2
    local branch_name=$(git rev-parse --abbrev-ref HEAD)
    
    # Create PR
    gh pr create --title "Fix #${issue_number}" --body "Closes #${issue_number}" --head "$branch_name"
    
    # Monitor CI/CD
    gh pr checks "$pr_number" --watch
    
    # TODO: Uncomment this when dry-run a few times.
    # gh pr merge "$pr_number" --merge
    # git pull

    git checkout master
}

# Function to add failure status to PR
add_failure_status() {
    if [ -z "$1" ] || [ -z "$2" ]; then
        echo "Usage: ./workflow.sh add-failure-status <pr-number> \"<failure-message>\""
        exit 1
    fi
    
    local pr_number=$1
    local failure_message="$2"
    local timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
    
    local comment="## Failure Status Report
**Timestamp:** $timestamp
**Status:** Blocked

### Attempted Approach
$failure_message"

    gh pr comment "$pr_number" --body "$comment"
}

# Show usage if no command provided
if [ $# -eq 0 ]; then
    echo "Usage:"
    echo "  ./workflow.sh list-issues              # List open issues"
    echo "  ./workflow.sh start-issue <number>     # Start work on an issue"
    echo "  ./workflow.sh commit-and-push <message> # Commit and push changes"
    echo "  ./workflow.sh monitor-ci <number>      # Monitor CI/CD for PR"
    echo "  ./workflow.sh complete-issue <pr> <issue> # Complete work on an issue"
    echo "  ./workflow.sh add-failure-status <pr> \"<message>\" # Add failure status to PR"
    exit 1
fi

# Handle commands
case "$1" in
    "list-issues")
        list_issues
        ;;
    "start-issue")
        start_issue "$2"
        ;;
    "commit-and-push")
        commit_and_push "$2"
        ;;
    "monitor-ci")
        monitor_ci "$2"
        ;;
    "complete-issue")
        complete_issue "$2" "$3"
        ;;
    "add-failure-status")
        add_failure_status "$2" "$3"
        ;;
    *)
        echo "Unknown command: $1"
        exit 1
        ;;
esac
