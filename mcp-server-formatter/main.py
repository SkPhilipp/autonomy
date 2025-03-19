from mcp.server.fastmcp import FastMCP
import json
import os
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("formatter")

mcp = FastMCP("FormatterMCP")

def get_project_dir(project_name=None):
    if not project_name:
        raise ValueError("Project name must be specified")
    return os.path.join("/project", project_name)

@mcp.tool()
def format_with_black(project_name: str) -> str:
    """
    Format Python code using Black
    
    :param project_name: The basename of the project's root directory.
    """
    project_dir = get_project_dir(project_name)
    cmd = ["black", project_dir]
    try:
        logger.info(f"Running: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=project_dir
        )
        return json.dumps({
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        })
    except Exception as e:
        return json.dumps({
            "error": str(e)
        })
