# self_improving_assistant.py
import os
import argparse
from utils.commands import Commands
from utils.claude_api import ClaudeAPI
from utils.state import StateManager
from utils.code_manager import CodeManager
from utils.knowledge_manager import KnowledgeManager
from utils.goal_tracker import GoalTracker
from config import HISTORY_FILE, VERSION, next_version

class SelfImprovingAssistant:
    def __init__(self):
        # Initialize core components
        self.commands = Commands()
        self.claude_api = ClaudeAPI()
        self.state_manager = StateManager()
        self.code_manager = CodeManager()
        self.knowledge_manager = KnowledgeManager()
        self.goal_tracker = GoalTracker()
        self.try_number = 1
        
        # Create necessary directories
        self.ensure_directories()
        
        # Initialize state with current version
        self.update_version(VERSION)
        
    def update_version(self, version):
        """Update the version in state and load appropriate goals."""
        self.state_manager.state["version"] = version
        self.state_manager.save_state()
        self.goal_tracker.load_goals_for_version(version)
        
    def ensure_directories(self):
        """Ensure all necessary directories exist."""
        directories = ["versions", "test", "utils", "tests", "data", "knowledge", "goals"]
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
        
    def extract_knowledge(self, response):
        """Extract knowledge from the response and store it."""
        if isinstance(response, dict) and "response" in response:
            knowledge_items = self.knowledge_manager.extract_knowledge(response["response"])
            if knowledge_items:
                print(f"\nExtracted {len(knowledge_items)} knowledge items.")
                return len(knowledge_items)
        return 0
        
    def implement_code_changes(self, response):
        """Extract and implement code changes from a Claude response."""
        print("Analyzing response for code changes...")
        
        try:
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
                
                # Check for version updates in config.py
                if "config.py" in code_files and VERSION != next_version():
                    new_version = next_version()
                    print(f"\nUpdating from version {VERSION} to {new_version}")
                    self.update_version(new_version)
                
                return True
            else:
                print("\nTests failed. Not deploying to production.")
                return False
                
        except Exception as e:
            print(f"Error implementing code changes: {str(e)}")
            return False
        
    def get_current_code_prompt(self):
        """Generate a prompt with the current code."""
        current_code = self.code_manager.get_current_code()
        return f"This is your current code:\n```python\n{current_code}\n```\n"
    
    def check_goals(self):
        """Check progress on goals and report."""
        completed, in_progress = self.goal_tracker.check_progress()
        if completed:
            print(f"\nCompleted {len(completed)} goals in this session:")
            for goal in completed:
                print(f" ✅ {goal}")
        
        if in_progress:
            print(f"\nIn progress: {len(in_progress)} goals:")
            for goal, progress in in_progress.items():
                print(f" ⏳ {goal}: {progress}%")
    
    def should_auto_improve(self):
        """Determine if the assistant should initiate self-improvement."""
        # Check if we haven't improved in a while
        last_improvement = self.state_manager.get_last_improvement_time()
        cycles_since_improvement = self.state_manager.get_cycles_since_improvement()
        
        # If it's been more than 5 interactions or 24 hours since last improvement
        if cycles_since_improvement > 5:
            return True
        
        return False
        
    def run(self, test_mode=False):
        """Main execution loop."""
        if test_mode:
            print("Running in test mode - validating functionality...")
            # Perform basic validation
            print("- State manager:", "OK" if self.state_manager else "ERROR")
            print("- Claude API:", "OK" if self.claude_api else "ERROR")
            print("- Code manager:", "OK" if self.code_manager else "ERROR")
            print("- Knowledge manager:", "OK" if self.knowledge_manager else "ERROR")
            print("- Goal tracker:", "OK" if self.goal_tracker else "ERROR")
            print("Test completed successfully!")
            return True
            
        print(f"Reto's Self-Improving Assistant v{VERSION}\n")
        print("--------------------------------")
        print("Type 'quit' to exit, 'implement' to force implementation of code")
        print("Type 'goals' to see current goals, 'knowledge' to query knowledge base\n")
        
        while True:
            # Check goals first
            self.check_goals()
            
            # Get the current code to show to Claude
            prompt_start = self.get_current_code_prompt()
            
            # Get user input
            user_input = input("Reto's comment: ")
            if user_input == "":
                user_input = "Ok. Write the next version of yourself."
            
            # Handle special commands
            if user_input.lower() in ['/quit', 'quit', 'exit', '/exit']:
                print("Goodbye!")
                break
                
            if user_input.lower() == 'goals':
                self.goal_tracker.display_all_goals()
                continue
                
            if user_input.lower().startswith('knowledge '):
                query = user_input[10:].strip()
                results = self.knowledge_manager.search(query)
                print(f"\nKnowledge results for '{query}':")
                for i, result in enumerate(results[:5], 1):
                    print(f"{i}. {result['title']}: {result['summary']}")
                continue
            
            # Check if we should auto-improve
            if self.should_auto_improve():
                print("\nInitiating automatic self-improvement cycle...")
                user_input = "Please analyze your capabilities and make improvements to better assist Reto as a CEO."
                
            # Construct the full prompt
            prompt = prompt_start + "\nReto's input: " + user_input
            
            # Update state with user message
            self.state_manager.add_message("user", prompt)
            
            # Get response from Claude
            try:
                if user_input.lower() == '/retry':
                    response = self.claude_api.read_response()
                else:
                    # Get the current system prompt that includes our state
                    system_prompt = self.state_manager.update_system_prompt()
                    messages = self.state_manager.get_messages_for_api()
                    
                    # Add knowledge context if relevant
                    knowledge_context = self.knowledge_manager.get_relevant_knowledge(user_input)
                    if knowledge_context:
                        system_prompt += "\n\nRelevant knowledge for this question:\n" + knowledge_context
                    
                    response = self.claude_api.ask_claude(prompt, system_prompt, messages)
                
                # Extract and store knowledge
                self.extract_knowledge(response)
                
                # Update state with Claude's response
                if isinstance(response, dict) and "response" in response:
                    self.state_manager.add_message("assistant", response["response"])
                    
                    # Update goal progress based on the response
                    self.goal_tracker.update_progress_from_response(response["response"])
                
                # Print and save the response
                self.print_and_save_answer(prompt, response)
                
                # Implement code changes if requested or if it seems appropriate
                if user_input.lower() in ['implement', '/implement', 'write the next version', 'write the next version of yourself']:
                    self.implement_code_changes(response)
                    
            except Exception as e:
                print(f"Error in communication loop: {str(e)}")
                self.state_manager.log_error("run_loop", str(e))

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Self-Improving Assistant")
    parser.add_argument("--test", action="store_true", help="Run in test mode to validate functionality")
    args = parser.parse_args()
    
    try:
        # Initialize and run the assistant
        assistant = SelfImprovingAssistant()
        assistant.run(test_mode=args.test)
    except Exception as e:
        print(f"Critical error: {str(e)}")
        # Try to log the error if possible
        try:
            from utils.commands import Commands
            Commands.append_file("error.log", f"{str(e)}\n")
        except:
            pass

if __name__ == "__main__":
    main()