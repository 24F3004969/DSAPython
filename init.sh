#!/usr/bin/env bash
# Generate Python src layout INSIDE current directory (DSAPython)

set -euo pipefail

# Detect current folder name and convert to python package name
CURRENT_DIR="$(basename "$PWD")"
PACKAGE_NAME="$(echo "$CURRENT_DIR" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '_' | sed 's/^_*//; s/_*$//')"

echo "Initializing Python project in: $CURRENT_DIR"
echo "Package name: $PACKAGE_NAME"

# Create folders
mkdir -p src/$PACKAGE_NAME
mkdir -p tests

# Create package files
cat > src/$PACKAGE_NAME/__init__.py <<EOF
\"\"\"$CURRENT_DIR package initialization.\"\"\"

__version__ = "0.1.0"
EOF

cat > src/$PACKAGE_NAME/core.py <<'EOF'
"""Core module."""

def greet(name: str) -> str:
    return f"Hello, {name}! Welcome to DSAPython."
EOF

cat > src/$PACKAGE_NAME/utils.py <<'EOF'
"""Utility helpers."""

def add(a, b):
    return a + b
EOF

# Create test files
cat > tests/test_core.py <<EOF
import $PACKAGE_NAME.core as core

def test_greet():
    assert "Hello" in core.greet("Test")
EOF

cat > tests/test_utils.py <<EOF
import $PACKAGE_NAME.utils as utils

def test_add():
    assert utils.add(2, 3) == 5
EOF

# Create pyproject.toml
cat > pyproject.toml <<EOF
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "$PACKAGE_NAME"
version = "0.1.0"
description = "A Python project using src layout."
readme = "README.md"
requires-python = ">=3.10"
dependencies = []

[tool.setuptools.packages.find]
where = ["src"]
EOF

# Create .gitignore
cat > .gitignore <<'EOF'
__pycache__/
*.py[cod]
.venv/
build/
dist/
*.egg-info/
EOF

# Create README
cat > README.md <<EOF
# $CURRENT_DIR

Project initialized with Python src layout.

## Install & Test

\`\`\`bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools wheel pytest
pytest -q
\`\`\`
EOF

echo "Done! Project initialized successfully."
