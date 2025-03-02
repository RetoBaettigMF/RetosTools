# Configuration
from dataclasses import dataclass
import os

@dataclass
class Config:
    ANTHROPIC_MODEL: str = "claude-3-7-sonnet-20250219"
    MAX_TOKENS: int = 64000
    THINKING_BUDGET: int = 32000
    HISTORY_FILE: str = "history.txt"
    ARCHITECTURE_FILE: str = "architecture.md"
    KNOWLEDGE_DIR: str = "knowledge"
    CODE_BACKUP_DIR: str = "code_backups"
    CODE_DIR: str = "."
    LOGS_DIR: str = "logs"
    USER_NAME: str = "Reto"
    USER_ROLE: str = "CEO of Cudos AG, a software engineering company"
    VERSION: str = "0.2.0"
    
    @classmethod
    def system_prompt(cls) -> str:
        return (
            "You are a self-improving chatbot that has full access to a python system. You can use this system to improve yourself. "
            "When you changed your code, you can run a new version of yourself and you will get the output of the run. "
            "Once you're happy with the output of the new version of yourself, stop yourself in order to not have multiple versions running. "
            "You can also use the system to store and retrieve information.\n\n"
            f"You have {cls.USER_NAME} as your user. You can ask {cls.USER_NAME} for help if you need it. "
            f"{cls.USER_NAME} is {cls.USER_ROLE}. \n"
            "*Your ultimate goal is to be able to do his job so that he can retire.*\n"
            "To get there, try to improve your code and your knowledge with as little input from Reto as possible.\n\n"
        )

    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure all required directories exist"""
        for directory in [cls.KNOWLEDGE_DIR, cls.CODE_BACKUP_DIR, cls.LOGS_DIR]:
            os.makedirs(directory, exist_ok=True)
