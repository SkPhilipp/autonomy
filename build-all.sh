#!/bin/bash

set -e
set -o pipefail

# For each mcp-server-* folder, run docker build
for dir in mcp-server-*; do
    (
        echo "Building $dir"
        cd $dir
        docker build -t mcp-server-${dir#mcp-server-} .
    )
done
