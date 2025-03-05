# filename: utils/code_manager.py
import os
import re
import shutil
import datetime
from config import TEST_DIR, VERSIONS_DIR
from utils.commands import Commands

class CodeManager:
    def __init__(self):
        """Initialize the CodeManager."""
        self.main_dir = "."
        self.test_dir = TEST_DIR
        self.backup_dir = VERSIONS_DIR
        
        # Ensure required directories exist
        Commands.create_directory(TEST_DIR)
        Commands.create_directory(VERSIONS_DIR)
        
    def get_file_content(self, filepath):
        """Read the content of a file if it exists."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file {filepath}: {str(e)}"
            
    def get_current_code(self, file_path="main.py"):
        """Get the contents of the specified file."""
        return self.get_file_content(file_path)
            
    def extract_code_from_response(self, response):
        """Extract code blocks from a Claude response."""
        if not isinstance(response, dict) or "response" not in response:
            return {}
            
        text = response["response"]
        code_files = {}
        
        # Pattern to match Python code blocks with filename indicators
        # Looks for: ```python (or ```), then captures the code content
        code_blocks = re.findall(r'```(?:python)?\s*\n(.*?)\n```', text, re.DOTALL)

        for i, block in enumerate(code_blocks):
            # Look for filename indicators in each code block
            filename_match = re.search(r'^\s*#\s*filename:\s*([^\n]+)', block, re.MULTILINE)
            if filename_match:
                filename = filename_match.group(1).strip()
                # Remove the filename line from the code
                code = re.sub(r'^\s*#\s*filename:\s*[^\n]+\n?', '', block, flags=re.MULTILINE)
                code_files[filename] = code.strip()
                continue
                
            # Alternative filename format
            filename_match = re.search(r'^\s*#\s*([a-zA-Z0-9_\/\\]+?\.[a-zA-Z0-9]+)', block, re.MULTILINE)
            if filename_match:
                filename = filename_match.group(1)
                code_files[filename] = block.strip()
                continue

            # Try to detect filenames from class definitions
            class_match = re.search(r"class\s+(\w+)", block)
            if class_match:
                class_name = class_match.group(1)
                # If it's the main assistant class
                if class_name == "SelfImprovingAssistant":
                    filename = "main.py"
                else:
                    # Convert CamelCase to snake_case for the filename
                    filename = ''.join(['_'+c.lower() if c.isupper() else c.lower() for c in class_name]).lstrip('_')
                    filename = f"utils/{filename}.py"
                
                # Check if this file already exists in the project
                existing_content = self.get_file_content(filename)
                if "Error reading file" not in str(existing_content):
                    print(f"Found existing file for class {class_name}: {filename}")
                    code_files[filename] = block.strip()
                    continue
            
            # Default case if no filename can be determined
            if len(code_blocks) == 1:
                # If only one code block, assume it's main.py
                filename = "main.py"
            else:
                # Generate a name based on block position
                filename = f"generated_code_{i+1}.py"
            
            code_files[filename] = block.strip()
        
        # Read the original content of each file to understand what we're modifying
        for filename in list(code_files.keys()):
            original_content = self.get_file_content(filename)
            if "Error reading file" not in str(original_content):
                print(f"Reading original file before modification: {filename}")
        
        return code_files
        
    def deploy_to_test(self, code_files):
        """Deploy code files to test environment, including unchanged files."""
        # Clear the test directory first
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir, exist_ok=True)
        
        # First, copy all existing project files to ensure all dependencies are available
        print("Copying all project files to test environment...")
        for root, dirs, files in os.walk(self.main_dir):
            # Skip directories we don't want to copy
            if any(excluded in root for excluded in [
                self.test_dir, ".git", "__pycache__", self.backup_dir
            ]):
                continue
                
            for file in files:
                # Skip non-Python files or specific files we don't want to copy
                if not file.endswith(".py"):
                    continue
                    
                # Get original file path and determine destination path
                src_path = os.path.join(root, file)
                # Maintain directory structure in test directory
                rel_path = os.path.relpath(src_path, self.main_dir)
                dst_path = os.path.join(self.test_dir, rel_path)
                
                # Create directories if needed
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                
                # Copy the file
                shutil.copy2(src_path, dst_path)
        
        # Now override with our new files
        print("Applying changes to test environment...")
        for filename, content in code_files.items():
            # Determine the destination path 
            dst_path = os.path.join(self.test_dir, filename)
            
            # Create directories if needed
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            
            # Write the new content
            with open(dst_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        return self.test_dir
        
    def test_new_code(self):
        """Run tests on the new code."""
        # Simple test: try to run main.py in test mode
        try:
            import subprocess
            
            # Navigate to test directory and run main.py with --test flag
            result = subprocess.run(
                ["python", "main.py", "--test"],
                cwd=self.test_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            success = result.returncode == 0
            output = result.stdout + "\n" + result.stderr
            
            return {
                "success": success,
                "output": output
            }
        except Exception as e:
            return {
                "success": False,
                "output": f"Error running tests: {str(e)}"
            }
            
    def deploy_to_production(self, code_files):
        """Deploy code files to production after testing."""
        # Create a backup of current code first
        backup_timestamp = self._create_backup()
        
        # Deploy each file
        deployed_files = []
        for filename, content in code_files.items():
            # Determine the destination path 
            dst_path = os.path.join(self.main_dir, filename)
            
            # Create directories if needed
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            
            # Write the new content
            with open(dst_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            deployed_files.append(filename)
            
        return {
            "success": True,
            "message": f"Successfully deployed {len(deployed_files)} files to production. Backup created at {backup_timestamp}.",
            "deployed_files": deployed_files,
            "backup": backup_timestamp
        }
        
    def _create_backup(self):
        """Create a backup of the current code."""
        from datetime import datetime
        
        # Create a timestamp for the backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(self.backup_dir, timestamp)
        
        # Create the backup directory
        os.makedirs(backup_dir, exist_ok=True)
        
        # Copy all Python files from the main directory to the backup
        for root, dirs, files in os.walk(self.main_dir):
            # Skip directories we don't want to backup
            if any(excluded in root for excluded in [
                self.test_dir, ".git", "__pycache__", self.backup_dir
            ]):
                continue
                
            for file in files:
                # Only backup Python files
                if not file.endswith(".py"):
                    continue
                    
                # Get original file path and determine destination path
                src_path = os.path.join(root, file)
                # Maintain directory structure in backup
                rel_path = os.path.relpath(src_path, self.main_dir)
                dst_path = os.path.join(backup_dir, rel_path)
                
                # Create directories if needed
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                
                # Copy the file
                shutil.copy2(src_path, dst_path)
                
        return timestamp