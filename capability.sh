#!/bin/bash

# Function to browse a URL
browse() {
    if [ -z "$1" ]; then
        echo "Usage: ./capability.sh browse <url>"
        exit 1
    fi
    
    lynx -dump "$1"
}

# Function to search the web
search() {
    if [ -z "$1" ]; then
        echo "Usage: ./capability.sh search <query>"
        exit 1
    fi
    
    local query=$(echo "$1" | sed 's/ /+/g')
    local url="https://www.google.com/search?q=${query}"
    browse "$url"
}

# Function to take a screenshot of a webpage
screenshot() {
    if [ -z "$1" ]; then
        echo "Usage: ./capability.sh screenshot <url> [output-path]"
        exit 1
    fi
    
    local url="$1"
    local output_path="${2:-screenshot.png}"
    
    # Ensure the scripts directory exists
    if [ ! -d "scripts" ]; then
        echo "Error: scripts directory not found"
        exit 1
    fi
    
    # Run the screenshot script
    node scripts/screenshot.js "$url" "$output_path"
}

# Show usage if no command provided
if [ $# -eq 0 ]; then
    echo "Usage:"
    echo "  ./capability.sh browse <url>    # Browse a URL"
    echo "  ./capability.sh search <query>  # Search the web"
    echo "  ./capability.sh screenshot <url> [output-path]  # Take a screenshot of a webpage"
    exit 1
fi

# Handle commands
case "$1" in
    "browse")
        browse "$2"
        ;;
    "search")
        search "$2"
        ;;
    "screenshot")
        screenshot "$2" "$3"
        ;;
    *)
        echo "Unknown command: $1"
        exit 1
        ;;
esac
