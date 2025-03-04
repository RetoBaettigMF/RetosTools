# config.py
import os

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, "history.md")
STATE_FILE = os.path.join(BASE_DIR, "state.json")
SYSTEM_PROMPT_FILE = os.path.join(BASE_DIR, "system_prompt.txt")

# Version information
VERSION = "0.3.0"
DEVELOPMENT_PHASE = "knowledge_acquisition"
DEVELOPMENT_PLAN = "Build knowledge base on CEO responsibilities and Cudos AG"

def next_version():
    """Calculate the next version based on the current version."""
    if not VERSION:
        return "0.1.0"
        
    major, minor, patch = VERSION.split(".")
    
    # For now, just increment the patch version
    patch = str(int(patch) + 1)
    
    return f"{major}.{minor}.{patch}"