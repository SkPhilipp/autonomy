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

# Show usage if no command provided
if [ $# -eq 0 ]; then
    echo "Usage:"
    echo "  ./capability.sh browse <url>    # Browse a URL"
    echo "  ./capability.sh search <query>  # Search the web"
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
    *)
        echo "Unknown command: $1"
        exit 1
        ;;
esac 