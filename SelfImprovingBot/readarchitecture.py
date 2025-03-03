import os
import re
from typing import Any, Dict, List, Optional
from config import Config
from codemanager import CodeManager
from knowledgebase import KnowledgeBase
import logging
logger = logging.getLogger("self-improving-chatbot")

"""
Architecture Documentation Generator

This module provides functionality to automatically generate architecture documentation
from Python source code. The ReadArchitecture class analyzes Python files in the code
directory, extracts class and function definitions, signatures, and docstrings, and compiles
them into a structured architecture overview document.

The generated architecture overview includes:
- High-level descriptions of each file based on their docstrings
- Class definitions with their public methods and signatures
- Top-level functions not belonging to any class

This module helps maintain up-to-date documentation that reflects the current state
of the codebase, ensuring that documentation stays synchronized with the actual
implementation as the system evolves.
"""

class ReadArchitecture:
    def __init__(self):
        self._code_manager = CodeManager()

    def update_architecture_description(self) -> None:
        """Update the architecture description based on the current code"""
        try:
            # Get all Python files in the code directory
            files = self._code_manager.list_code_files()
            
            # Generate a high-level description of each file
            architecture = "# Architecture Overview\n\n"
            for filename in sorted(files):
                if filename == Config.ARCHITECTURE_FILE:
                    continue
                    
                file_content = self._code_manager.get_current_code(filename)
                
                architecture += f"## {filename}\n\n"
                
                # Extract top-level docstring if available
                file_docstring = re.search(r'^"""(.*?)"""', file_content, re.DOTALL)
                if file_docstring:
                    doc = file_docstring.group(1).strip()
                    architecture += f"{doc}\n\n"
                
                # Extract classes with their methods
                class_matches = re.finditer(r'class\s+([a-zA-Z0-9_]+)(?:\(.*?\))?:\s*(?:""".*?""")?', file_content, re.DOTALL)
                
                # Track top-level functions (not inside any class)
                class_spans = []
                
                for class_match in class_matches:
                    class_name = class_match.group(1)
                    class_start = class_match.start()
                    
                    # Find the end of the class (next class or EOF)
                    next_class = re.search(r'class\s+[a-zA-Z0-9_]+', file_content[class_start + 1:])
                    class_end = next_class.start() + class_start + 1 if next_class else len(file_content)
                    class_spans.append((class_start, class_end))
                    
                    class_content = file_content[class_start:class_end]
                    
                    architecture += f"**Class: {class_name}**\n\n"
                    
                    # Find methods in this class
                    method_matches = re.finditer(r'    def\s+([a-zA-Z0-9_]+)\s*\((.*?)\)\s*(?:->|:)', class_content, re.DOTALL)
                    
                    for method_match in method_matches:
                        method_name = method_match.group(1)
                        
                        # Skip private methods
                        if method_name.startswith('_') and not method_name.startswith('__'):
                            continue
                        
                        method_params = method_match.group(2).strip()
                        
                        # Get return type if available
                        return_type_match = re.search(r'-> ?(.*?):', class_content[method_match.start():method_match.end() + 50])
                        return_type = return_type_match.group(1) if return_type_match else ""
                        
                        signature = f"{method_name}({method_params})"
                        if return_type:
                            signature += f" -> {return_type}"
                        
                        architecture += f"- {signature}\n"
                    
                    architecture += "\n"
                
                # Find top-level functions (not inside any class)
                top_functions = []
                function_matches = re.finditer(r'^def\s+([a-zA-Z0-9_]+)\s*\((.*?)\)\s*(?:->|:)', file_content, re.MULTILINE)
                
                for function_match in function_matches:
                    function_start = function_match.start()
                    
                    # Check if this function is outside any class
                    is_outside_class = True
                    for start, end in class_spans:
                        if start <= function_start <= end:
                            is_outside_class = False
                            break
                    
                    if is_outside_class:
                        function_name = function_match.group(1)
                        
                        # Skip private functions
                        if function_name.startswith('_') and not function_name.startswith('__'):
                            continue
                        
                        function_params = function_match.group(2).strip()
                        
                        # Get return type if available
                        return_type_match = re.search(r'-> ?(.*?):', file_content[function_match.start():function_match.end() + 50])
                        return_type = return_type_match.group(1) if return_type_match else ""
                        
                        signature = f"{function_name}({function_params})"
                        if return_type:
                            signature += f" -> {return_type}"
                        
                        top_functions.append(signature)
                
                if top_functions:
                    architecture += "**Functions:**\n"
                    for func in top_functions:
                        architecture += f"- {func}\n"
                    architecture += "\n"
                    
            # Write the architecture description
            architecture_path = os.path.join(Config.CODE_DIR, Config.ARCHITECTURE_FILE)
            with open(architecture_path, 'w', encoding='utf-8') as f:
                f.write(architecture)
                
        except Exception as e:
            logger.error(f"Error updating architecture description: {str(e)}")


if __name__ == "__main__":
    a = ReadArchitecture()
    a.update_architecture_description()
