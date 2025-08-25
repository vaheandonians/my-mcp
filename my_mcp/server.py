from typing import Annotated, Callable
import functools

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
    mcp.run(transport="sse")


def stdio():
    mcp.run(transport="stdio")
