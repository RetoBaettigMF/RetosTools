import os
import anthropic
import json
import time
import datetime
import re
import sys
import subprocess
from typing import Dict, List, Any, Optional, Tuple

# Configuration
class Config:
    ANTHROPIC_MODEL = "claude-3-7-sonnet-20250219"
    MAX_TOKENS = 25000
    THINKING_BUDGET = 16000
    HISTORY_FILE = "history.txt"
    KNOWLEDGE_DIR = "knowledge"
    CODE_BACKUP_DIR = "code_backups"
    USER_NAME = "Reto"
    USER_ROLE = "CEO of Cudos AG, a software engineering company"
    
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

# Knowledge Management
class KnowledgeBase:
    def __init__(self, knowledge_dir: str = Config.KNOWLEDGE_DIR):
        self.knowledge_dir = knowledge_dir
        self._ensure_dirs_exist()
        
    def _ensure_dirs_exist(self) -> None:
        """Ensure all required directories exist"""
        os.makedirs(self.knowledge_dir, exist_ok=True)
        os.makedirs(Config.CODE_BACKUP_DIR, exist_ok=True)
        
    def store_knowledge(self, category: str, key: str, data: Any) -> bool:
        """Store information in the knowledge base"""
        try:
            category_dir = os.path.join(self.knowledge_dir, category)
            os.makedirs(category_dir, exist_ok=True)
            
            file_path = os.path.join(category_dir, f"{key}.json")
            with open(file_path, "w") as f:
                json.dump({"data": data, "updated_at": time.time()}, f, indent=2)
            return True
        except Exception as e:
            print(f"Error storing knowledge: {str(e)}")
            return False
            
    def retrieve_knowledge(self, category: str, key: str) -> Optional[Any]:
        """Retrieve information from the knowledge base"""
        try:
            file_path = os.path.join(self.knowledge_dir, category, f"{key}.json")
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    data = json.load(f)
                return data["data"]
            return None
        except Exception as e:
            print(f"Error retrieving knowledge: {str(e)}")
            return None
            
    def list_knowledge(self, category: str = None) -> List[str]:
        """List available knowledge items"""
        result = []
        try:
            if category:
                category_dir = os.path.join(self.knowledge_dir, category)
                if os.path.exists(category_dir):
                    for file in os.listdir(category_dir):
                        if file.endswith('.json'):
                            result.append(file[:-5])  # Remove .json extension
            else:
                for dir_name in os.listdir(self.knowledge_dir):
                    dir_path = os.path.join(self.knowledge_dir, dir_name)
                    if os.path.isdir(dir_path):
                        result.append(dir_name)
        except Exception as e:
            print(f"Error listing knowledge: {str(e)}")
        return result
        
    def search_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """Search for knowledge items containing the query"""
        results = []
        for category in self.list_knowledge():
            category_dir = os.path.join(self.knowledge_dir, category)
            for item in os.listdir(category_dir):
                if item.endswith('.json'):
                    key = item[:-5]
                    data = self.retrieve_knowledge(category, key)
                    # Convert data to string for search
                    data_str = json.dumps(data)
                    if query.lower() in data_str.lower() or query.lower() in key.lower():
                        results.append({
                            "category": category,
                            "key": key,
                            "data": data
                        })
        return results

# Conversation Management
class ConversationManager:
    def __init__(self, history_file: str = Config.HISTORY_FILE):
        self.history_file = history_file
        self.messages = []
        self.try_number = 1
        self._ensure_history_exists()
        
    def _ensure_history_exists(self) -> None:
        """Make sure the history file exists"""
        if not os.path.exists(self.history_file):
            with open(self.history_file, "w") as f:
                f.write(f"# Conversation History - Started {datetime.datetime.now()}\n\n")
                
    def add_user_message(self, content: str) -> None:
        """Add a user message to the conversation"""
        self.messages.append({"role": "user", "content": content})
        
    def add_assistant_message(self, content: str) -> None:
        """Add an assistant message to the conversation"""
        self.messages.append({"role": "assistant", "content": content})
        
    def get_messages(self) -> List[Dict[str, str]]:
        """Get all messages in the conversation"""
        return self.messages
        
    def format_response(self, response: Dict[str, str]) -> str:
        """Format the response for output and storage"""
        result = ""
        if isinstance(response, dict) and "thinking" in response:
            result += "## Claude thinking:\n"
            result += response["thinking"] + "\n"
        if isinstance(response, dict) and "research_idea" in response:
            result += "## Claude's response:\n"
            result += response["research_idea"]
        else:
            result = "## Error:\n" + str(response)
        return result + "\n\n"
        
    def log_interaction(self, prompt: str, response: Dict[str, str]) -> str:
        """Log the interaction to history file and return formatted output"""
        result = f"# Try {self.try_number}\n## Prompt:\n{prompt}\n"
        result += self.format_response(response)
        
        with open(self.history_file, "a") as f:
            f.write(result)
            
        self.try_number += 1
        return result
        
    def extract_code_from_response(self, response: str) -> Optional[str]:
        """Extract Python code blocks from a response"""
        code_blocks = re.findall(r'```python\n(.*?)\n```', response, re.DOTALL)
        if code_blocks:
            return code_blocks[0]
        return None

# Code Management
class CodeManager:
    def __init__(self, backup_dir: str = Config.CODE_BACKUP_DIR):
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
        
    def get_current_code(self) -> str:
        """Get the content of the current main.py file"""
        try:
            with open("main.py", "r") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading current code: {str(e)}")
            return ""
            
    def backup_current_code(self) -> bool:
        """Create a backup of the current code"""
        try:
            current_code = self.get_current_code()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(self.backup_dir, f"main_{timestamp}.py")
            
            with open(backup_path, "w") as f:
                f.write(current_code)
            return True
        except Exception as e:
            print(f"Error backing up code: {str(e)}")
            return False
            
    def update_code(self, new_code: str) -> bool:
        """Update the main.py file with new code"""
        try:
            # First backup the current code
            self.backup_current_code()
            
            # Then write the new code
            with open("main.py", "w") as f:
                f.write(new_code)
            return True
        except Exception as e:
            print(f"Error updating code: {str(e)}")
            return False
            
    def test_code(self) -> Tuple[bool, str]:
        """Test if the code is valid Python"""
        try:
            result = subprocess.run(
                [sys.executable, "-c", self.get_current_code()],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return True, "Code is valid Python."
            else:
                return False, f"Code has syntax errors: {result.stderr}"
        except Exception as e:
            return False, f"Error testing code: {str(e)}"
            
    def run_new_version(self) -> Tuple[bool, str]:
        """Run the new version of the code"""
        try:
            # Start the process but don't wait for it
            subprocess.Popen([sys.executable, "main.py"])
            return True, "New version started."
        except Exception as e:
            return False, f"Error running new version: {str(e)}"

# AI Interface
class Claude:
    def __init__(self, api_key: Optional[str] = None):
        self.client = anthropic.Anthropic(
            api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"),
        )
        
    def ask(self, messages: List[Dict[str, str]]) -> Dict[str, str]:
        """Send a request to Claude and get the response"""
        try:
            results = {"thinking": "", "research_idea": ""}
            
            with self.client.messages.stream(
                model=Config.ANTHROPIC_MODEL,
                system=Config.system_prompt(),
                max_tokens=Config.MAX_TOKENS,
                thinking={
                    "type": "enabled",
                    "budget_tokens": Config.THINKING_BUDGET
                },
                messages=messages
            ) as stream:
                current_block_type = None
                for event in stream:
                    if event.type == "content_block_start":
                        current_block_type = event.content_block.type
                    elif event.type == "content_block_delta":
                        if event.delta.type == "thinking_delta":
                            results["thinking"] += event.delta.thinking
                        elif event.delta.type == "text_delta":
                            results["research_idea"] += event.delta.text
                    elif event.type == "message_stop":
                        break
            return results
        except Exception as e:
            return {"thinking": "", "research_idea": f"Error: {str(e)}"}

# Main Application
class SelfImprovingChatbot:
    def __init__(self):
        self.knowledge = KnowledgeBase()
        self.conversation = ConversationManager()
        self.code_manager = CodeManager()
        self.claude = Claude()
        
    def prepare_prompt(self, user_input: str) -> str:
        """Prepare the prompt for Claude with current code and user input"""
        code = self.code_manager.get_current_code()
        prompt = f"This is your current code:\n```python\n{code}\n```\n\n"
        prompt += f"{Config.USER_NAME}'s input: {user_input}"
        return prompt
        
    def process_response(self, response: Dict[str, str]) -> None:
        """Process Claude's response and look for code improvements"""
        # Extract code if present
        if "research_idea" in response:
            code = self.conversation.extract_code_from_response(response["research_idea"])
            if code:
                # Backup and update the code
                if self.code_manager.update_code(code):
                    print("Code updated successfully!")
                    
                    # Test if the code is valid
                    is_valid, message = self.code_manager.test_code()
                    if is_valid:
                        print("Code is valid Python.")
                    else:
                        print(f"Warning: {message}")
                        
                    # Extract knowledge if present
                    if "thinking" in response:
                        thinking = response["thinking"]
                        # Look for insights about CEO role and software engineering
                        if "CEO" in thinking or "software" in thinking:
                            self.knowledge.store_knowledge(
                                "insights", 
                                f"insight_{int(time.time())}", 
                                {"thinking": thinking[:500], "timestamp": time.time()}
                            )
        
    def run(self) -> None:
        """Main run loop"""
        print("Reto's Self-Improving Chatbot\n")
        print("------------------------------")
        print("Type 'quit' to exit\n")
        
        while True:
            user_input = input(f"{Config.USER_NAME}'s comment: ")
            
            # Handle empty input
            if user_input == "":
                user_input = "Ok. Write the next version of yourself."
                
            # Handle exit commands
            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
                
            # Handle special commands
            if user_input.startswith('/'):
                parts = user_input[1:].split(' ', 1)
                command = parts[0].lower()
                
                if command == "knowledge":
                    # List knowledge categories
                    categories = self.knowledge.list_knowledge()
                    print(f"Knowledge categories: {', '.join(categories) if categories else 'None'}")
                    continue
                    
                elif command == "run":
                    # Run the new version
                    success, message = self.code_manager.run_new_version()
                    print(message)
                    if success:
                        print("Shutting down this instance...")
                        return
                    continue
                
            # Normal flow - ask Claude
            prompt = self.prepare_prompt(user_input)
            self.conversation.add_user_message(prompt)
            
            print("Thinking...")
            response = self.claude.ask(self.conversation.get_messages())
            
            # Add response to conversation history
            if "research_idea" in response:
                self.conversation.add_assistant_message(response["research_idea"])
                
            # Process and log the interaction
            formatted_response = self.conversation.log_interaction(prompt, response)
            print(formatted_response)
            
            # Process the response for potential code updates
            self.process_response(response)

# Entry point
def main():
    chatbot = SelfImprovingChatbot()
    chatbot.run()

if __name__ == "__main__":
    main()
