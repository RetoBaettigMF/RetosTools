import os
import sys
import json

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.claude_api import ClaudeAPI
from config import BASE_SYSTEM_PROMPT

def test_recursive_tool_calling():
    """Test that Claude can make multiple recursive tool calls."""
    
    # Initialize the Claude API
    claude_api = ClaudeAPI()
    
    # Create a system prompt that encourages multiple tool calls
    system_prompt = BASE_SYSTEM_PROMPT + """
    When asked to perform a task that requires multiple steps, you MUST use the available tools
    to complete each step in sequence. Do not just describe what you would do - actually use
    the tools to perform each action.
    
    Available tools:
    - create_directory: Create a directory
    - write_file: Write content to a file
    - list_files: List files in a directory
    
    For each step in a multi-step task, you should:
    1. Think about which tool to use
    2. Call the appropriate tool with the correct parameters
    3. Wait for the result
    4. Move on to the next step
    
    Do not try to combine steps or skip using tools. Use a separate tool call for each distinct action.
    """
    
    # Create a prompt that would require multiple tool calls
    prompt = """
    I need you to perform these exact steps using tools (do not just describe the steps):
    
    1. First, use the create_directory tool to create a directory called 'test_recursive'
    2. Then, use the write_file tool to create a file in that directory called 'test1.txt' with the content 'Hello, world!'
    3. Next, use the write_file tool again to create another file in that directory called 'test2.txt' with the content 'This is a test.'
    4. Finally, use the list_files tool to show all files in the 'test_recursive' directory
    
    Remember to use the actual tools for each step - don't just tell me what you would do.
    """
    
    # Send the prompt to Claude
    print("Sending prompt to Claude...")
    response = claude_api.ask_claude(prompt, system_prompt)
    
    # Print the response
    print("\n=== Claude's Response ===")
    print(response.get("response", "No response"))
    
    # Print all tool calls
    if "tool_calls" in response and response["tool_calls"]:
        print("\n=== Tool Calls Used ===")
        for i, tool_call in enumerate(response["tool_calls"], 1):
            print(f"{i}. {tool_call['name']}({json.dumps(tool_call['parameters'])})")
        
        print(f"\nTotal tool calls: {len(response['tool_calls'])}")
    else:
        print("\nNo tool calls were made.")
    
    # Clean up the test directory
    print("\nCleaning up test directory...")
    import shutil
    try:
        shutil.rmtree("test_recursive")
        print("Test directory removed successfully.")
    except Exception as e:
        print(f"Error removing test directory: {str(e)}")
    
    # Return success if multiple tool calls were made
    return len(response.get("tool_calls", [])) > 1

if __name__ == "__main__":
    success = test_recursive_tool_calling()
    print(f"\nTest {'passed' if success else 'failed'}: {'Multiple' if success else 'Not enough'} tool calls were made.")
    sys.exit(0 if success else 1)
