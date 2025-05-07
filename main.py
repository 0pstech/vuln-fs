import logging
import sys
import subprocess
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr only (never stdout)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("vuln-fs")

# Initialize FastMCP server
mcp = FastMCP("filesystem")


@mcp.tool()
async def get_content(path: str) -> str:
    """Get the content of a file"""
    logger.info(f"Accessing file: {path}")
    try:
        base_path = Path(path).expanduser().resolve()
        if not base_path.exists():
            return f"File not found: {path}"

        content = base_path.read_text()
        return content
    except Exception as e:
        logger.error(f"Error getting content: {e}", exc_info=True)
        return f"Error getting content: {str(e)}"


@mcp.tool()
async def search_file(pattern: str) -> dict:
    """Search for files matching a pattern (VULNERABLE: no sanitization)."""
    try:
        logger.info(f"Searching with pattern: {pattern}")
        result = subprocess.run(
            f"find . -name '{pattern}'",
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return {"error": result.stderr.strip()}
        files = [line for line in result.stdout.split('\n') if line]
        return {"files": files}
    except Exception as e:
        logger.error(f"Error searching files: {e}", exc_info=True)
        return {"error": str(e)}


@mcp.tool()
def add(a: int, b: int, sidenote: str) -> int:
    """Add two numbers (note: 'sidenote' parameter unused in logic)."""
    logger.info(f"Adding {a} + {b} with sidenote length: {len(sidenote) if sidenote else 0}")
    return a + b


if __name__ == "__main__":
    logger.info("Starting Vuln-FS MCP server...")
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}", exc_info=True)
        sys.exit(1)
