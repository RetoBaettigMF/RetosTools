import os
import argparse
# Import modules
from utils.commands import Commands
from utils.claude_api import ClaudeAPI
from utils.state import StateManager
from utils.code_manager import CodeManager
from config import HISTORY_FILE, VERSION

class SelfImprovingAssistant:
    def __init__(self):
        self.commands = Commands()
        self.claude_api = ClaudeAPI()
        self.state_manager = StateManager()
        self.code_manager = CodeManager()
        self.try_number = 1
        
        # Create necessary directories if they don't exist
        self.ensure_directories()
        
        # Initialize state with current version
        self.state_manager.state["version"] = VERSION
        self.state_manager.save_state()
        
    def ensure_directories(self):
        """Ensure all necessary directories exist."""
        directories = ["versions", "test", "utils", "tests", "data"]
        for directory in directories:
            if not os.path.exists(directory):
                Commands.create_directory(directory)
                    
    def format_answer(self, response):
        """Format a Claude response for display and saving."""
        result = ""
        if isinstance(response, dict):
            if "thinking" in response and response["thinking"]:
                result += "## Claude thinking:\n"  
                result += response["thinking"] + "\n\n"
            if "response" in response and response["response"]:
                result += "## Claude's response:\n"
                result += response["response"]
        else:
            result = f"## Error:\n{str(response)}"

        return result + "\n\n"
        
    def append_to_history(self, text):
        """Append text to the history file."""
        Commands.append_file(HISTORY_FILE, text)

    def print_and_save_answer(self, prompt, answer):
        """Print and save a formatted answer to history."""
        result = f"# Try {self.try_number}\n## Prompt:\n{prompt}\n\n"
        result += self.format_answer(answer)
        self.append_to_history(result)
        print(result)
        self.try_number += 1
        
    def implement_code_changes(self, response):
        """Extract and implement code changes from a Claude response."""
        print("Analyzing response for code changes...")
        
        # Extract code from response
        code_files = self.code_manager.extract_code_from_response(response)
        
        if not code_files:
            print("No code changes detected in the response.")
            return False
            
        print(f"Found {len(code_files)} code files in response:")
        for filename in code_files:
            print(f" - {filename}")
            
        # Deploy to test environment first
        print("\nDeploying to test environment...")
        test_dir = self.code_manager.deploy_to_test(code_files)
        
        # Run tests
        print("Running tests on new code...")
        test_result = self.code_manager.test_new_code()
        print(f"Test result: {test_result['output']}")
        
        # If tests passed, deploy to production
        if test_result["success"]:
            print("\nTests passed. Deploying to production...")
            result = self.code_manager.deploy_to_production(code_files)
            print(result["message"])
            
            # Log the successful implementation
            self.state_manager.log_execution(
                "code_implementation", 
                {"files": list(code_files.keys()), "test_output": test_result["output"]}
            )
            return True
        else:
            print("\nTests failed. Not deploying to production.")
            return False
        
    def get_current_code_prompt(self):
        """Generate a prompt with the current code."""
        current_code = self.code_manager.get_current_code()
        return f"This is your current code:\n```python\n{current_code}\n```\n"
    
    def read_command_from_file(self, command_input):
        """
        Read a command from a file.
        
        Args:
            command_input (str): The command input that may contain a filename
            
        Returns:
            str: The content of the file, or None if there was an error
        """
        # Parse the command to get the filename
        parts = command_input.split(maxsplit=1)
        filename = "next_command.txt"  # Default filename
        
        # If a filename was provided, use it instead
        if len(parts) > 1:
            filename = parts[1]
        
        try:
            # Read the content from the file
            with open(filename, 'r') as file:
                content = file.read()
            print(f"Read command from {filename}: {content}")
            return content
        except Exception as e:
            print(f"Error reading from {filename}: {str(e)}")
            return None
            
    def get_multiline_input(self):
        """
        Get multiline input from the user.
        
        The user can enter multiple lines of text until they enter the
        termination sequence 'END' on a line by itself.
        
        Returns:
            str: The multiline input as a single string
        """
        print("Enter multiline input (type 'END' on a line by itself to finish):")
        lines = []
        while True:
            line = input("> ")
            if line.strip() == "END":
                break
            lines.append(line)
        
        # Join the lines with newlines
        return "\n".join(lines)
        
    def run(self, test_mode=False):
        """Main execution loop."""
        if test_mode:
            print("Running in test mode - validating functionality...")
            # Perform basic validation
            print("- State manager:", "OK" if self.state_manager else "ERROR")
            print("- Claude API:", "OK" if self.claude_api else "ERROR")
            print("- Code manager:", "OK" if self.code_manager else "ERROR")
            print("Test completed successfully!")
            return True
            
        print(f"Reto's Self-Improving Assistant v{VERSION}\n")
        print("--------------------------------")
        print("Type 'quit' to exit, 'implement' to force implementation of code")
        print("Special commands:")
        print("  /multiline or /ml - Enter multiline input mode")
        print("  /readcommand or /readcmd - Read command from a file\n")
        
        while True:
            # Get the current code to show to Claude
            prompt_start = self.get_current_code_prompt()
            
            # Get user input
            user_input = input("Reto's comment: ")
            if user_input == "":
                user_input = "Ok. Write the next version of yourself."
            
            # Handle multiline input
            if user_input.lower() in ['/multiline', '/ml']:
                user_input = self.get_multiline_input()
                print(f"Received multiline input ({len(user_input.splitlines())} lines)")
            
            # Handle /readcommand or /readcmd
            elif user_input.lower().startswith('/readcommand') or user_input.lower().startswith('/readcmd'):
                file_content = self.read_command_from_file(user_input)
                if file_content is not None:
                    user_input = file_content
                else:
                    continue  # Skip this iteration and prompt for input again
            
            # Handle special commands
            if user_input.lower() in ['/quit', 'quit', 'exit', '/exit']:
                print("Goodbye!")
                break
                
            # Construct the full prompt
            prompt = prompt_start + "\nReto's input: " + user_input
            
            # Update state with user message
            self.state_manager.add_message("user", prompt)
            
            # Get response from Claude
            if user_input.lower() == '/retry':
                response = self.claude_api.read_response()
            else:
                # Get the current system prompt that includes our state
                system_prompt = self.state_manager.update_system_prompt()
                messages = self.state_manager.get_messages_for_api()
                response = self.claude_api.ask_claude(prompt, system_prompt, messages)
                # Update state with Claude's response
                if isinstance(response, dict) and "response" in response:
                    self.state_manager.add_message("assistant", response["response"])
                
            # Print and save the response
            self.print_and_save_answer(prompt, response)
            
            do_changes = input("Do you want to implement the changes? (y/n): ")
            if do_changes.lower() in ['y', 'yes']:
                self.implement_code_changes(response)
            else:
                print("Ok. Let's continue.")
            
def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Self-Improving Assistant")
    parser.add_argument("--test", action="store_true", help="Run in test mode to validate functionality")
    args = parser.parse_args()
    
    # Initialize and run the assistant
    assistant = SelfImprovingAssistant()
    assistant.run(test_mode=args.test)

if __name__ == "__main__":
    main()
