from typing import Tuple
import os  
import datetime
import subprocess
import sys
import logging
from config import Config

logger = logging.getLogger("self-improving-chatbot")

# Code Management
class CodeManager:
    def __init__(self, backup_dir: str = Config.CODE_BACKUP_DIR):
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
        
    def get_current_code(self, filename="main.py") -> str:
        """Get the content of the current main.py file"""
        try:
            with open(filename, "r") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading current code: {str(e)}")
            return ""
            
    def backup_current_code(self, filename="main.py") -> bool:
        """Create a backup of the current code"""
        try:
            current_code = self.get_current_code(filename=filename)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(self.backup_dir, f"{filename}_{timestamp}")
            
            with open(backup_path, "w", encoding='utf-8') as f:
                f.write(current_code)
            return True
        except Exception as e:
            logger.error(f"Error backing up code: {str(e)}")
            return False
            
    def update_code(self, new_code: str, filename="main.py") -> bool:
        """Update the main.py file with new code"""
        try:
            # First backup the current code
            self.backup_current_code(filename=filename)
            
            # Then write the new code
            with open(filename, "w", encoding='utf-8') as f:
                f.write(new_code)
            return True
        except Exception as e:
            logger.error(f"Error updating code: {str(e)}")
            return False
            
    def test_code(self, filename="main.py") -> Tuple[bool, str]:
        """Test if the code is valid Python"""
        try:
            result = subprocess.run(
                [sys.executable, "-c", self.get_current_code(filename)],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return True, f"Code {filename} is valid Python."
            else:
                return False, f"Code {filename} has syntax errors: {result.stderr}"
        except Exception as e:
            return False, f"Error testing code {filename}: {str(e)}"
            
    def run_new_version(self) -> Tuple[bool, str]:
        """Run the new version of the code"""
        try:
            # Start the process but don't wait for it
            subprocess.Popen([sys.executable, "main.py"])
            return True, "New version started."
        except Exception as e:
            return False, f"Error running new version: {str(e)}"
