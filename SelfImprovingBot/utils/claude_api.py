import os
import anthropic
import json
from config import CLAUDE_MODEL, MAX_TOKENS, THINKING_TOKENS, RESPONSE_FILE

class ClaudeAPI:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
        )
        
    def ask_claude(self, prompt, system_prompt, messages=None):
        """
        Send a request to Claude and get a response with thinking.
        
        Args:
            prompt: The user prompt to send to Claude
            system_prompt: The system prompt to use
            messages: Previous conversation messages (optional)
            
        Returns:
            Dictionary containing the thinking and response
        """
        try:
            # Start with just the current prompt if no message history is provided
            if messages is None:
                messages = []
                
            # Add the current prompt to messages
            messages.append({"role": "user", "content": prompt})
            
            results = {"thinking": "", "response": ""}   
            
            with self.client.messages.stream(
                model=CLAUDE_MODEL,
                system=system_prompt,
                max_tokens=MAX_TOKENS,
                thinking={
                    "type": "enabled",
                    "budget_tokens": THINKING_TOKENS
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
                            results["response"] += event.delta.text           
                    elif event.type == "message_stop":
                        break
                        
            # Save the response automatically
            self.save_response(results)
                        
            return results

        except Exception as e:
            error_msg = f"Error communicating with Claude API: {str(e)}"
            print(error_msg)
            return {"thinking": "", "response": error_msg}
            
    def save_response(self, response, filename=RESPONSE_FILE):
        """Save a response to a file."""
        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(response, file, indent=2)
            return True
        except Exception as e:
            print(f"Error saving response: {str(e)}")
            return False
            
    def read_response(self, filename=RESPONSE_FILE):
        """Read a response from a file."""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error reading response: {str(e)}")
            return {"thinking": "", "response": f"Error reading response: {str(e)}"}