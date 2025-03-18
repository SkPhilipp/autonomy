# Autonomy

A workflow automation tool for managing GitHub issues and project tasks with integrated web capabilities.

## Features

- **Issue Management**: Streamlined workflow for handling GitHub issues
- **Web Capabilities**: Built-in tools for web browsing, searching, and screenshotting
- **Automated Workflow**: Simplified commands for common development tasks
- **CI/CD Integration**: Built-in monitoring of pull request checks

## Prerequisites

- [GitHub CLI (gh)](https://cli.github.com/manual/installation)
- Node.js (for screenshot functionality)
- Lynx (for web browsing)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SkPhilipp/autonomy.git
   cd autonomy
   ```

2. Install dependencies:
   ```bash
   cd scripts
   npm install
   ```

3. Authenticate with GitHub:
   ```bash
   gh auth login
   ```

4. Add commands to PATH:
   ```bash
   # Add this to your ~/.bashrc or ~/.zshrc
   export PATH="/path/to/autonomy:$PATH"
   ```
   Replace `/path/to/autonomy` with the actual path where you cloned the repository.
   After adding this line, either:
   - Start a new terminal session, or
   - Run `source ~/.bashrc` (or `source ~/.zshrc`) to apply changes immediately
