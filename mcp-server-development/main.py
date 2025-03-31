from mcp.server.fastmcp import FastMCP
import subprocess
import logging
import os

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("development")

mcp = FastMCP("DevelopmentMCP")

def run_command(cmd: list[str], cwd: str | None = None) -> str:
    """
    Run a command and return its output with stdout and stderr merged.
    
    :param cmd: The command to run as a list of strings
    :param cwd: Optional working directory for the command
    :return: The combined stdout/stderr output
    """
    logger.info(f"Running command: {' '.join(cmd)}")
    try:
        env = os.environ.copy()
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=cwd,
            env=env
        )
        return result.stdout
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def test() -> str:
    """
    Run tests for the given project. 
    """
    project_dir = "/project"
    venv_dir = os.path.join(project_dir, ".venv")
    venv_python = os.path.join(venv_dir, "bin", "python")
    requirements_file = os.path.join(project_dir, "requirements.txt")

    if not os.path.exists(venv_dir):
        run_command(["python3", "-m", "venv", ".venv"], cwd=project_dir)
    
    if os.path.exists(requirements_file):
        run_command([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], cwd=project_dir)

    if "pytest" not in requirements_file:
        run_command([venv_python, "-m", "pip", "install", "pytest"], cwd=project_dir)

    return run_command([venv_python, "-m", "pytest"], cwd=project_dir)

@mcp.tool()
def build() -> str:
    """
    Build the current project.
    """
    project_dir = "/project"
    venv_dir = os.path.join(project_dir, ".venv")
    venv_python = os.path.join(venv_dir, "bin", "python")
    requirements_file = os.path.join(project_dir, "requirements.txt")
    
    if not os.path.exists(venv_dir):
        run_command(["python3", "-m", "venv", ".venv"], cwd=project_dir)
    
    if os.path.exists(requirements_file):
        run_command([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], cwd=project_dir)

    return "Project built"
