import subprocess
import logging
import shlex

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("browser")


def web_search(search_term: str) -> str:
    search_url = f"https://duckduckgo.com/html/?q={search_term}"
    cmd = ["lynx", "-dump", "-nolist", search_url]
    try:
        logger.info(f"Searching web for: {search_term}")
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return f"{result.stdout}\n{result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"


def browse_url(url: str) -> str:
    url = shlex.quote(url)
    cmd = ["lynx", "-dump", "-nolist", url]
    try:
        logger.info(f"Browsing URL: {url}")
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return f"{result.stdout}\n{result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"
