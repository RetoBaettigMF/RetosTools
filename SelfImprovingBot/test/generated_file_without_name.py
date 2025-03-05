# filename: config.py
import os

# Version information
VERSION = "0.2.0"

# File paths
HISTORY_FILE = "history.md"
TEST_DIR = "test"
VERSIONS_DIR = "versions"

# Claude API settings - should be set in environment variables
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY", "your-api-key")
CLAUDE_API_URL = os.environ.get("CLAUDE_API_URL", "https://api.anthropic.com/v1/messages")

# Development information
CURRENT_PHASE = "setup"
DEVELOPMENT_PLAN = "No plan yet"