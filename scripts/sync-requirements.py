#!/usr/bin/env python3
"""
Generate requirements.txt from pyproject.toml dependencies.
This ensures Docker builds use the same dependencies as defined in pyproject.toml.
"""

import tomllib
from pathlib import Path

def extract_dependencies():
    """Extract dependencies from pyproject.toml and write to requirements.txt"""
    
    project_root = Path(__file__).parent.parent
    pyproject_path = project_root / "pyproject.toml"
    requirements_path = project_root / "requirements.txt"
    
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
    
    dependencies = data.get("project", {}).get("dependencies", [])
    
    with open(requirements_path, "w") as f:
        for dep in dependencies:
            f.write(f"{dep}\n")
    
    print(f"✓ Generated requirements.txt with {len(dependencies)} dependencies")
    print(f"  Dependencies: {', '.join(dependencies)}")

if __name__ == "__main__":
    extract_dependencies()
