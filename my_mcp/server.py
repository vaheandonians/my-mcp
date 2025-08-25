from typing import Annotated, Callable
import functools
import os
import sys

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from my_mcp.config.config_manager import ConfigManager


ConfigManager().configure()

def handle_errors(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise ToolError(f"Error in {func.__name__}: {e}")
    return wrapper


# Initialize FastMCP based on how the script is being run
# Check if we're running via the SSE entry point
if os.path.basename(sys.argv[0]).endswith('my-mcp-sse') or 'sse' in sys.argv[0]:
    # Running in SSE mode - bind to 0.0.0.0 for Docker compatibility
    mcp = FastMCP("my-mcp", host="0.0.0.0")
else:
    # Running in STDIO mode or during import/testing
    mcp = FastMCP("my-mcp")

@mcp.prompt()
def summarize_text(text_to_summarize: str) -> str:
    """Creates a prompt asking the LLM to summarize the provided text."""
    return (
        "Summarize the following text in one concise paragraph focusing on the key ideas and outcomes:\n\n"
        f"{text_to_summarize}"
    )

@mcp.tool()
@handle_errors
def get_fibonacci_sequence(
    n: Annotated[int, "The length of the Fibonacci sequence to get"]
) -> str:
    """Gets the Fibonacci sequence up to the nth number."""
    def build_sequence(count):
        if count <= 0:
            return []
        elif count == 1:
            return [0]
        elif count == 2:
            return [0, 1]
        else:
            prev_sequence = build_sequence(count - 1)
            next_value = prev_sequence[-1] + prev_sequence[-2]
            return prev_sequence + [next_value]
    
    return str(build_sequence(n))


def sse():
    """Run the MCP server in SSE mode."""
    mcp.run(transport="sse")


def stdio():
    """Run the MCP server in STDIO mode."""
    mcp.run(transport="stdio")
