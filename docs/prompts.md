# Prompts

In the context of an MCP (Model Context Protocol) server, a prompt is a set of instructions or guidance that the server can provide to the AI model to help it understand how to properly use the server's tools and resources.

Here are the key aspects of MCP server prompts:

## Purpose
The prompt serves as documentation and behavioral guidance that tells the AI model:

- What the server's tools do and when to use them
- Best practices for using the tools effectively
- Any specific constraints or requirements
- Context about the data or services the server provides

## How It Works
When an MCP server is connected, it can expose a prompt through the protocol that gets incorporated into the model's context. This prompt essentially becomes part of the system instructions that guide the model's behavior when interacting with that particular server.

## Example
For instance, if you had an MCP server that provides access to a company's internal database, its prompt might include:

- Instructions on which tables contain what type of data
- Guidelines on respecting data privacy
- Specific query patterns that work best with the database
- When to use certain tools versus others

## Benefits

- Better tool usage: The model understands the nuances of when and how to use each tool
- Reduced errors: Clear instructions help prevent misuse of the tools
- Context awareness: The model can make more informed decisions about which tools to use for specific tasks

The prompt essentially acts as a bridge between the MCP server's capabilities and the AI model's understanding, ensuring more effective and appropriate use of the server's resources.

## How to Add a Prompt

1. Similar to tools prompts are declared as a function with explanatory parameters.
2. Prompts are annotated with `@mcp.prompt`.
3. Return a string with the entire prompt to use.

Here is an example of a prompt that summarizes a text.

```
@mcp.prompt
def summarize_text(text_to_summarize: str) -> str:
    """Creates a prompt asking the LLM to summarize the provided text."""
    return (
        "Summarize the following text in one concise paragraph focusing on the key ideas and outcomes:\n\n"
        f"{text_to_summarize}"
    )
```
