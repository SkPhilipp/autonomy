import subprocess
import logging
import shlex

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("browser")


def _run_command(cmd, **kwargs):
    return subprocess.run(cmd, **kwargs)


def search(term: str, runner=_run_command) -> str:
    search_url = f"https://duckduckgo.com/html/?q={term}"
    cmd = ["lynx", "-dump", "-nolist", search_url]
    try:
        logger.info(f"Searching web for: {term}")
        result = runner(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return f"{result.stdout}\n{result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"


def fetch(url: str, runner=_run_command) -> str:
    url = shlex.quote(url)
    cmd = ["lynx", "-dump", "-nolist", url]
    try:
        logger.info(f"Browsing URL: {url}")
        result = runner(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return f"{result.stdout}\n{result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"
