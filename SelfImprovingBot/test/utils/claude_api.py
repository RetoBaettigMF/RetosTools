# filename: utils/claude_api.py
import os
import json
import requests
import inspect
from config import CLAUDE_MODEL, MAX_TOKENS
from utils.commands import Commands

class ClaudeAPI:
    """Interface for communicating with the Claude API with function calling capabilities."""
    
    def __init__(self):
        self.api_key = os.environ.get("CLAUDE_API_KEY", "")
        self.api_url = os.environ.get("CLAUDE_API_URL", "https://api.anthropic.com/v1/messages")
        self.model = CLAUDE_MODEL
        self.max_tokens = MAX_TOKENS
        self.last_response = None
        self.available_tools = self._register_tools()
        
    def _register_tools(self):
        """Register all tools from the Commands class."""
        tools = {}
        
        # Get all static methods from Commands class
        for name, method in inspect.getmembers(Commands, predicate=inspect.isfunction):
            if not name.startswith('_'):  # Skip private methods
                # Get method signature and docstring
                sig = inspect.signature(method)
                doc = inspect.getdoc(method) or "No description available"
                
                # Parse parameters
                parameters = {}
                required = []
                
                for param_name, param in sig.parameters.items():
                    # Skip self parameter
                    if param_name == 'self':
                        continue
                    
                    # Determine parameter type
                    param_type = "string"  # Default type
                    if param.annotation != inspect.Parameter.empty:
                        if param.annotation == str:
                            param_type = "string"
                        elif param.annotation == int:
                            param_type = "number"
                        elif param.annotation == bool:
                            param_type = "boolean"
                        elif param.annotation == dict or param.annotation == list:
                            param_type = "object"
                    
                    # Create parameter definition
                    parameters[param_name] = {
                        "type": param_type,
                        "description": f"Parameter for {name}: {param_name}"
                    }
                    
                    # Add to required parameters if no default value
                    if param.default == inspect.Parameter.empty:
                        required.append(param_name)
                
                # Register the tool
                tools[name] = {
                    "function": method,
                    "description": doc,
                    "parameters": parameters,
                    "required": required
                }
        
        return tools
    
    def _format_tools_for_api(self):
        """Format tools for the Claude API."""
        tools = []
        
        for name, tool in self.available_tools.items():
            # Create properties dictionary for parameters
            properties = {}
            for param_name, param_info in tool["parameters"].items():
                properties[param_name] = {
                    "type": param_info["type"],
                    "description": param_info["description"]
                }
            
            # Create tool definition
            tool_def = {
                "name": name,
                "description": tool["description"],
                "parameters": {
                    "type": "object",
                    "properties": properties
                }
            }
            
            # Add required parameters if any
            if tool["required"]:
                tool_def["parameters"]["required"] = tool["required"]
            
            # Add to tools list
            tools.append(tool_def)
        
        return tools
    
    def _execute_tool(self, tool_name, parameters):
        """Execute a tool with the given parameters."""
        if tool_name not in self.available_tools:
            return {"error": f"Tool not found: {tool_name}"}
        
        try:
            # Get the tool function
            tool_func = self.available_tools[tool_name]["function"]
            
            # Execute the function with the parameters
            result = tool_func(**parameters)
            
            return {"result": result}
        except Exception as e:
            return {"error": f"Error executing tool {tool_name}: {str(e)}"}
    
    def ask_claude(self, prompt, system_prompt, messages=None, with_tools=True):
        """
        Send a prompt to Claude API and return the response.
        
        Args:
            prompt: The user's prompt 
            system_prompt: The system prompt
            messages: Previous messages (optional)
            with_tools: Whether to enable tool use (default: True)
            
        Returns:
            A dictionary containing Claude's response
        """
        try:
            # Prepare the API request
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            
            # Format the messages
            if messages:
                message_list = messages
            else:
                message_list = [{"role": "user", "content": prompt}]
            
            # Create the request payload
            payload = {
                "model": self.model,
                "system": system_prompt,
                "messages": message_list,
                "max_tokens": self.max_tokens
            }
            
            # Add tools if requested
            if with_tools:
                payload["tools"] = self._format_tools_for_api()
            
            # Send the request
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload
            )
            
            # Check for errors
            response.raise_for_status()
            response_data = response.json()
            
            # Extract the response text
            response_text = ""
            tool_calls = []
            
            for content in response_data.get("content", []):
                if content["type"] == "text":
                    response_text += content["text"]
                elif content["type"] == "tool_use":
                    # Store tool use information
                    tool_calls.append({
                        "id": content["id"],
                        "name": content["name"],
                        "parameters": content["input"]
                    })
            
            # If there are tool calls, process them
            if tool_calls:
                return self._process_tool_calls(response_data, tool_calls, system_prompt, message_list)
            
            # No tool calls, just return the response
            result = {
                "thinking": "",
                "response": response_text
            }
            
            self.last_response = result
            return result
            
        except Exception as e:
            error_msg = f"Error communicating with Claude API: {str(e)}"
            result = {
                "thinking": "",
                "response": error_msg
            }
            self.last_response = result
            return result
    
    def _process_tool_calls(self, initial_response, tool_calls, system_prompt, messages):
        """Process tool calls in Claude's response."""
        initial_text = ""
        tool_outputs = []
        
        # Extract initial text response
        for content in initial_response.get("content", []):
            if content["type"] == "text":
                initial_text += content["text"]
        
        # Process each tool call
        for tool_call in tool_calls:
            tool_name = tool_call["name"]
            tool_params = tool_call["parameters"]
            
            # Execute the tool and get result
            tool_result = self._execute_tool(tool_name, tool_params)
            
            # Add to outputs
            tool_outputs.append({
                "tool_call_id": tool_call["id"],
                "output": json.dumps(tool_result)
            })
        
        # If there are tool outputs, send a follow-up request
        if tool_outputs:
            try:
                # Prepare headers
                headers = {
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                }
                
                # Create follow-up payload
                follow_up_payload = {
                    "model": self.model,
                    "system": system_prompt,
                    "messages": messages,
                    "max_tokens": self.max_tokens,
                    "tool_outputs": tool_outputs
                }
                
                # Send follow-up request
                follow_up_response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=follow_up_payload
                )
                
                # Check for errors
                follow_up_response.raise_for_status()
                follow_up_data = follow_up_response.json()
                
                # Extract follow-up response
                follow_up_text = ""
                for content in follow_up_data.get("content", []):
                    if content["type"] == "text":
                        follow_up_text += content["text"]
                
                result = {
                    "thinking": "",
                    "response": follow_up_text,
                    "tool_calls": tool_calls,
                    "tool_outputs": tool_outputs
                }
                
                self.last_response = result
                return result
                
            except Exception as e:
                error_msg = f"Error processing tool calls: {str(e)}"
                result = {
                    "thinking": "",
                    "response": error_msg + "\n\nInitial response: " + initial_text,
                    "tool_calls": tool_calls
                }
                self.last_response = result
                return result
        
        # No tool outputs to process
        result = {
            "thinking": "",
            "response": initial_text,
            "tool_calls": tool_calls
        }
        
        self.last_response = result
        return result
    
    def read_response(self):
        """Return the last response."""
        return self.last_response or {"thinking": "", "response": "No previous response available."}