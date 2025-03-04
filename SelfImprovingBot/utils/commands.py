import os
import subprocess
import shutil
import json

class Commands:
    @staticmethod
    def read_file(file_path):
        """Read a file and return its contents."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            return f"Error reading file {file_path}: {str(e)}"
        
    @staticmethod
    def write_file(file_path, content):
        """Write content to a file."""
        try:
            # Create directories if they don't exist
            os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
            
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            return f"Successfully wrote to {file_path}"
        except Exception as e:
            return f"Error writing to file {file_path}: {str(e)}"

    @staticmethod
    def append_file(file_path, content):
        """Append content to a file."""
        try:
            # Create directories if they don't exist
            os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
            
            with open(file_path, "a", encoding="utf-8") as file:
                file.write(content)
            return f"Successfully appended to {file_path}"
        except Exception as e:
            return f"Error appending to file {file_path}: {str(e)}"

    @staticmethod
    def list_files(directory="."):
        """List files in the specified directory."""
        try:
            return os.listdir(directory)
        except Exception as e:
            return f"Error listing files in {directory}: {str(e)}"

    @staticmethod
    def create_directory(directory_path):
        """Create a directory if it doesn't exist."""
        try:
            os.makedirs(directory_path, exist_ok=True)
            return f"Created directory: {directory_path}"
        except Exception as e:
            return f"Error creating directory {directory_path}: {str(e)}"

    @staticmethod
    def copy_file(source, destination):
        """Copy a file from source to destination."""
        try:
            # Ensure destination directory exists
            dest_dir = os.path.dirname(destination)
            if dest_dir:
                os.makedirs(dest_dir, exist_ok=True)
                
            shutil.copy2(source, destination)
            return f"Copied {source} to {destination}"
        except Exception as e:
            return f"Error copying file: {str(e)}"
            
    @staticmethod
    def backup_file(file_path, backup_dir, version=None):
        """Create a backup of a file in the specified directory."""
        try:
            base_name = os.path.basename(file_path)
            if version:
                backup_path = os.path.join(backup_dir, f"{base_name}.{version}")
            else:
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                backup_path = os.path.join(backup_dir, f"{base_name}.{timestamp}")
            
            # Create the backup directory if it doesn't exist
            os.makedirs(backup_dir, exist_ok=True)
            
            # Copy the file
            shutil.copy2(file_path, backup_path)
            return f"Backed up {file_path} to {backup_path}"
        except Exception as e:
            return f"Error backing up file: {str(e)}"

    @staticmethod
    def execute_command(command):
        """Execute a shell command and return the output."""
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.stdout.decode('utf-8')  # Return the output as a string
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr.decode('utf-8')}"  # Return the error message
            
    @staticmethod
    def run_python_file(file_path, args=""):
        """Run a Python file and return the output."""
        try:
            command = f"python {file_path} {args}"
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.stdout.decode('utf-8')
        except subprocess.CalledProcessError as e:
            return f"Error running Python file: {e.stderr.decode('utf-8')}"