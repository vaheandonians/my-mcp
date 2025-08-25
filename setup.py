from setuptools import setup, find_packages

setup(
    name="my-mcp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "mcp[cli]>=1.6.0",
        "python-dotenv",
        "typeguard",
    ],
    entry_points={
        "console_scripts": [
            "my-mcp-sse=mcp.server:sse",
            "my-mcp-stdio=mcp.server:stdio",
        ],
    },
)
