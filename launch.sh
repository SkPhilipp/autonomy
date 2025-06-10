#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Activate the virtual environment
source "$SCRIPT_DIR/.venv/bin/activate"

# Check if an argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 {browse|jira|workflow} [args...]"
    exit 1
fi

COMMAND=$1
shift

# Run the selected main script
case "$COMMAND" in
    browse)
        python "$SCRIPT_DIR/src/browse_main.py" "$@"
        ;;
    jira)
        python "$SCRIPT_DIR/src/jira_main.py" "$@"
        ;;
    workflow)
        python "$SCRIPT_DIR/src/workflow_main.py" "$@"
        ;;
    *)
        echo "Invalid argument. Usage: $0 {browse|jira|workflow} [args...]"
        exit 1
        ;;
esac 