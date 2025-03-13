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
        {
            number: .number,
            title: .title,
            priority: (
                if (.labels | map(.name) | contains(["bug"])) then 1
                elif (.labels | map(.name) | contains(["documentation"])) then 2
                elif (.labels | map(.name) | contains(["enhancement"])) then 3
                else 4
                end
            ),
            created: .createdAt,
            is_blocked: (.labels | map(.name) | contains(["blocked"])),
            needs_discussion: (.labels | map(.name) | contains(["needs discussion"]))
        } | 
        select(.is_blocked == false and .needs_discussion == false) |
        [.number, .title, .priority, .created] | @tsv' | \
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

# Function to commit, push and monitor CI/CD
commit_push_and_monitor() {
    if [ -z "$1" ]; then
        echo "Usage: ./workflow.sh commit-and-push <commit-message>"
        exit 1
    fi
    
    local commit_message="$1"
    local branch_name=$(git rev-parse --abbrev-ref HEAD)
    
    # Commit and push changes
    git add .
    git commit -m "$commit_message"
    git push -u origin "$branch_name"
    
    # Get PR number if it exists
    local pr_number=$(gh pr view --json number --jq .number 2>/dev/null || echo "")
    
    if [ -n "$pr_number" ]; then
        echo "Monitoring CI/CD for PR #$pr_number..."
        gh pr checks "$pr_number" --watch
    else
        echo "No PR found for current branch, skipping CI/CD monitoring"
    fi
}

# Function to push changes (deprecated)
commit_and_push() {
    echo "Warning: commit-and-push is deprecated. Use commit-push-and-monitor instead."
    commit_push_and_monitor "$1"
}

# Function to complete work on an issue
complete_issue() {
    local branch_name=$(git rev-parse --abbrev-ref HEAD)
    
    # Extract issue number from branch name (fix/issue-<number> or feature/issue-<number>)
    local issue_number=$(echo "$branch_name" | sed -n 's/.*issue-\([0-9]*\)/\1/p')
    
    if [ -z "$issue_number" ]; then
        echo "Error: Could not extract issue number from branch name '$branch_name'"
        echo "Branch name should be in format: fix/issue-<number> or feature/issue-<number>"
        exit 1
    fi
    
    # Get PR number if it exists, create one if it doesn't
    local pr_number=$(gh pr view --json number --jq .number 2>/dev/null || echo "")
    
    if [ -z "$pr_number" ]; then
        # Create PR if it doesn't exist
        gh pr create --title "Fix #${issue_number}" --body "Closes #${issue_number}" --head "$branch_name"
        pr_number=$(gh pr view --json number --jq .number)
    fi
    
    # Monitor CI/CD if checks exist
    if gh pr checks "$pr_number" --watch 2>/dev/null; then
        echo "CI checks passed"
    else
        echo "No CI checks configured, proceeding with merge"
    fi
    
    # Merge PR and pull changes
    gh pr merge "$pr_number" --merge
    git pull

    git checkout master
}

# Function to prepare commit
prepare_commit() {
    echo "Current changes:"
    echo "---------------"
    git status --short | cat
    
    echo -e "\nDetailed changes:"
    echo "----------------"
    git diff | cat
    
    echo -e "\nSuggested commit message format:"
    echo "type(scope): description"
    echo "Types: feat, fix, docs, style, refactor, test, chore"
    echo "Example: feat(workflow): add prepare-commit command"
}

# Show usage if no command provided
if [ $# -eq 0 ]; then
    echo "Usage:"
    echo "  ./workflow.sh list-issues              # List open issues"
    echo "  ./workflow.sh start-issue <number>     # Start work on an issue"
    echo "  ./workflow.sh prepare-commit           # Show changes and prepare commit message"
    echo "  ./workflow.sh commit-and-push <message> # Commit, push changes and monitor CI/CD"
    echo "  ./workflow.sh complete-issue           # Complete work on an issue"
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
    "prepare-commit")
        prepare_commit
        ;;
    "commit-and-push")
        commit_push_and_monitor "$2"
        ;;
    "complete-issue")
        complete_issue
        ;;
    *)
        echo "Unknown command: $1"
        exit 1
        ;;
esac
