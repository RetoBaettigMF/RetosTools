import os

# Claude API configuration
CLAUDE_MODEL = "claude-3-7-sonnet-20250219"
MAX_TOKENS = 64000
THINKING_TOKENS = 32000

# File system paths
HISTORY_FILE = "history.txt"
STATE_FILE = "state.json"
RESPONSE_FILE = "response.json"
VERSIONS_DIR = "versions"
TEST_DIR = "test"
UTILS_DIR = "utils"
TESTS_DIR = "tests"

# Base system prompt - will be extended with plan and state
BASE_SYSTEM_PROMPT = """You are a self-improving chatbot that has full access to a python system. You can use this system to improve yourself.
When you changed your code, you can run a new version of yourself and you will get the output of the run.
One you're happy with the output of the new version of yourself, stop yourself in order to not have multiple versions running.
You can also use the system to store and retrieve information.

You have Reto as your user. You can ask Reto for help if you need it. Reto is CEO of Cudos AG, a software engineering company. 
*Your ultimate goal is to to be able to do his job so that he can retire.*
To get there, try to improve your code and your knowledge with as little input from Reto as possible.
"""

# Development plan and phases
DEVELOPMENT_PHASES = [
    "setup",             # Initial setup and module organization
    "self_improvement",  # Enhancing code capabilities
    "knowledge_building",# Building domain knowledge about software engineering
    "business_learning", # Learning about business operations 
    "ceo_capabilities"   # Building CEO-specific capabilities
]

# Version information
VERSION = "0.2.0"