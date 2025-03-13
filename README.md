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

## Usage

### Issue Management

List open issues:
```bash
./workflow.sh list-issues
```

Start working on an issue:
```bash
./workflow.sh start-issue <issue-number>
```

Prepare a commit:
```bash
./workflow.sh prepare-commit
```

Commit and push changes:
```bash
./workflow.sh commit-and-push "<commit-message>"
```

Complete an issue:
```bash
./workflow.sh complete-issue
```

### Web Capabilities

Browse a URL:
```bash
./capability.sh browse <url>
```

Search the web:
```bash
./capability.sh search "<query>"
```

Take a screenshot:
```bash
./capability.sh screenshot <url> [output-path]
```

## Workflow

1. List and select an unblocked issue
2. Start work on the issue
3. Implement changes
4. Test locally
5. Prepare and commit changes
6. Complete the issue

## Commit Message Format

Follow the conventional commit format:
```
type(scope): description
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

Example:
```
feat(workflow): add prepare-commit command
```

## Error Handling

If you encounter issues:
1. Note the blocking issue and solutions tried
2. Reset to last successful commit
3. Try a new approach
4. If stuck after 3 attempts, mark as blocked and move on

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

ISC 