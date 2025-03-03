import os
import re
import sys
import subprocess
import logging
from typing import Dict, List, Tuple, Optional
from config import Config
from readarchitecture import ReadArchitecture

logger = logging.getLogger("self-improving-chatbot.codemanager")

class CodeManager:
    """Manages code files and updates for the self-improving chatbot"""
    
    def __init__(self, code_dir: str = Config.CODE_DIR):
        self.code_dir = code_dir
        self._ensure_code_dir()
        
    def _ensure_code_dir(self) -> None:
        """Ensure the code directory exists"""
        if not os.path.exists(self.code_dir):
            os.makedirs(self.code_dir)
            
    def get_current_code(self, filename: str) -> str:
        """Get the contents of a specific code file"""
        filepath = os.path.join(self.code_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        return f"# {filename} does not exist yet"
    
    def list_code_files(self) -> List[str]:
        """List all code files in the code directory"""
        return [f for f in os.listdir(self.code_dir) 
                if f.endswith('.py') and os.path.isfile(os.path.join(self.code_dir, f))]
    
    def update_code(self, code: str, filename: str = "main.py") -> bool:
        """Update a specific code file with new content"""
        try:
            # Create backup
            self._backup_file(filename)
            
            # Write the new code
            filepath = os.path.join(self.code_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
                
            return True
        except Exception as e:
            logger.error(f"Error updating code: {str(e)}")
            return False
    
    def update_multiple_files(self, file_contents: Dict[str, str]) -> Dict[str, bool]:
        """Update multiple files at once
        
        Args:
            file_contents: Dictionary mapping filenames to their new content
            
        Returns:
            Dictionary mapping filenames to success status
        """
        results = {}
        for filename, content in file_contents.items():
            results[filename] = self.update_code(content, filename)
        
        # After updating all files, generate an updated architecture description
        self._update_architecture_description()
        
        return results
    
    def extract_code_blocks(self, response: str) -> Dict[str, str]:
        """Extract code blocks for multiple files from a response
        
        Looks for patterns like:
        ```python filename.py
        code here
        ```
        
        or
        
        File: filename.py
        ```python
        code here
        ```
        """
        # Pattern 1: ```python filename.py
        pattern1 = r'```python\s+([a-zA-Z0-9_\.]+)\n(.*?)\n```'
        matches1 = re.findall(pattern1, response, re.DOTALL)
        
        # Pattern 2: File: filename.py\n```python
        pattern2 = r'File:\s+([a-zA-Z0-9_\.]+)\n```python\n(.*?)\n```'
        matches2 = re.findall(pattern2, response, re.DOTALL)
        
        # Combine matches
        file_contents = {}
        for filename, content in matches1 + matches2:
            if filename.endswith('.py'):
                file_contents[filename] = content
            else:
                file_contents[f"{filename}.py"] = content
                
        # If no specific files found but there's a Python code block, assume it's for main.py
        if not file_contents:
            general_pattern = r'```python\n(.*?)\n```'
            general_matches = re.findall(general_pattern, response, re.DOTALL)
            if general_matches:
                file_contents["main.py"] = general_matches[0]
                
        return file_contents
    
    def _backup_file(self, filename: str) -> None:
        """Create a backup of the specified file"""
        filepath = os.path.join(self.code_dir, filename)
        if os.path.exists(filepath):
            backup_dir = os.path.join(self.code_dir, "backups")
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
                
            import time
            timestamp = int(time.time())
            backup_filename = f"{filename}.{timestamp}.bak"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            with open(filepath, 'r', encoding='utf-8') as src, \
                 open(backup_path, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
    
    def _update_architecture_description(self) -> None:
        """Update the architecture description based on the current code"""
        ra = ReadArchitecture()
        ra.update_architecture_description()
        
    def test_code(self) -> Tuple[bool, str]:
        """Test if the code is valid Python"""
        try:
            files = self.list_code_files()
            for filename in files:
                if filename.startswith('_'):  # Skip files starting with underscore
                    continue
                    
                filepath = os.path.join(self.code_dir, filename)
                result = subprocess.run(
                    [sys.executable, '-m', 'py_compile', filepath],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    return False, f"Syntax error in {filename}: {result.stderr}"
            
            return True, "All code files are valid Python"
        except Exception as e:
            return False, str(e)
    
    def run_new_version(self) -> Tuple[bool, str]:
        """Run the new version of the code"""
        try:
            main_file = os.path.join(self.code_dir, "main.py")
            if not os.path.exists(main_file):
                return False, "main.py does not exist"
                
            # First check if the code is valid
            is_valid, message = self.test_code()
            if not is_valid:
                return False, f"Cannot run invalid code: {message}"
                
            # Run the new version in a new process
            subprocess.Popen([sys.executable, main_file])
            return True, "Started new version of the chatbot"
        except Exception as e:
            return False, f"Error running new version: {str(e)}"