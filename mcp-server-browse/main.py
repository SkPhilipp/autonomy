from mcp.server.fastmcp import FastMCP
import json
import subprocess
import logging
import shlex

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("browser")

mcp = FastMCP("BrowserMCP")

@mcp.tool()
def web_search(search_term: str) -> str:
    """
    Search the web for real-time information about any topic

    :param search_term: The search query to look up on the web
    """
    # Use DuckDuckGo as the search engine with Lynx
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
        return json.dumps(
            {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
            }
        )
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def browse_url(url: str) -> str:
    """
    Retrieve and parse content from a specific URL

    :param url: The full URL to browse and retrieve content from
    """
    # Sanitize URL input
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
        return json.dumps(
            {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
            }
        )
    except Exception as e:
        return json.dumps({"error": str(e)})
