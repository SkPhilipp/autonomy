import sys
import subprocess
import json
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("formatter")


def format_with_black(config) -> str:
    project_dir = config.project_dir
    cmd = [sys.executable, "-m", "black", project_dir]
    try:
        logger.info(f"Running: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=project_dir,
        )
        return json.dumps(
            {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
            }
        )
    except Exception as e:
        return json.dumps({"error": str(e)})
