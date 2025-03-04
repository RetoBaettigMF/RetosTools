import os
import datetime
import re
from config import TEST_DIR, VERSIONS_DIR
from utils.commands import Commands

class CodeManager:
    def __init__(self):
        # Ensure required directories exist
        Commands.create_directory(TEST_DIR)
        Commands.create_directory(VERSIONS_DIR)
        
    def backup_current_code(self):
        """Create a backup of all Python files in the current directory."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        backup_dir = os.path.join(VERSIONS_DIR, f"backup_{timestamp}")
        Commands.create_directory(backup_dir)
        
        # Backup all Python files, including those in subdirectories
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.py'):
                    source_path = os.path.join(root, file)
                    # Create relative path in backup dir
                    rel_path = os.path.relpath(source_path, '.')
                    target_path = os.path.join(backup_dir, rel_path)
                    Commands.copy_file(source_path, target_path)
                    
        return backup_dir
        
    def setup_test_environment(self):
        """Prepare the test environment for testing new code."""
        # Clear the test directory if it exists
        if os.path.exists(TEST_DIR):
            import shutil
            shutil.rmtree(TEST_DIR)
            
        # Create fresh test directory
        Commands.create_directory(TEST_DIR)
        
        return TEST_DIR
        
    def extract_code_from_response(self, response):
        """Extract code blocks from Claude's response."""
        if not isinstance(response, dict) or "response" not in response:
            return {}
            
        text = response["response"]
        code_files = {}
        
        # Pattern to match Python code blocks with filename indicators
        # Looks for: ```python (or ```), then captures the code content
        code_blocks = re.findall(r'```(?:python)?\s*\n(.*?)\n```', text, re.DOTALL)

        filenames = []
        for block in code_blocks:
            # Look for filename indicators in each code block
            filename_match = re.search(r'^\s*#\s*([a-zA-Z0-9_\/\\]+?\.[a-zA-Z0-9]+)', block, re.MULTILINE)
            if filename_match:
                filenames.append(filename_match.group(1))
                continue

            filename_match = re.search(r'^\s*```[a-zA-Z]*\s*([a-zA-Z0-9_\/\\]+?\.[a-zA-Z0-9]+)\s*\n', block, re.MULTILINE)
            if filename_match:
                filenames.append(filename_match.group(1))
                continue            
            else:
                if (len(code_blocks) == 1):
                    # If only one code block, assume it's main.py unless explicitly named
                    filenames.append("main.py")
                else:   
                    filenames.append("generated_file_without_name.py")
        
        
        for i, filename in enumerate(filenames):
            code_files[filename] = code_blocks[i]
        return code_files
        
    def deploy_to_test(self, code_files):
        """Deploy code to the test environment for validation."""
        # Set up a fresh test environment
        self.setup_test_environment()
        
        # Deploy each file to the test directory
        for filename, code in code_files.items():
            # Handle subdirectories in the filename
            file_path = os.path.join(TEST_DIR, filename)
            Commands.write_file(file_path, code)
            
        return TEST_DIR
        
    def test_new_code(self):
        """Run tests on the code in the test environment."""
        # Run main.py in the test environment with a --test flag
        test_main = os.path.join(TEST_DIR, "main.py")
        if os.path.exists(test_main):
            result = Commands.run_python_file(test_main, "--test")
            return {"success": "Error:" not in result, "output": result}
        else:
            return {"success": False, "output": "main.py not found in test environment"}
            
    def deploy_to_production(self, code_files):
        """Deploy code to production after backing up current code."""
        # First backup the current code
        backup_dir = self.backup_current_code()
        
        # Then deploy each file
        for filename, code in code_files.items():
            # Check if we need to create directories
            if '/' in filename:
                directory = os.path.dirname(filename)
                Commands.create_directory(directory)
                
            # Write the new code to the file
            Commands.write_file(filename, code)
            
        return {
            "success": True, 
            "message": f"Deployed {len(code_files)} files to production. Backup created at {backup_dir}"
        }
        
    def get_current_code(self, file_path="main.py"):
        """Get the contents of the specified file."""
        return Commands.read_file(file_path)