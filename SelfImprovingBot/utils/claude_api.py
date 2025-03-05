# filename: utils/claude_api.py
import os
import json
import inspect
from anthropic import Anthropic
from config import CLAUDE_MODEL, MAX_TOKENS
from utils.commands import Commands

class ClaudeAPI:
    """Interface for communicating with the Claude API with function calling capabilities."""
    
    def __init__(self):
        self.api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        self.model = CLAUDE_MODEL
        self.max_tokens = MAX_TOKENS
        self.last_response = None
        self.available_tools = self._register_tools()
        self.client = Anthropic(api_key=self.api_key)
        
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
                "input_schema": {
                    "type": "object",
                    "properties": properties
                }
            }
            
            # Add required parameters if any
            if tool["required"]:
                tool_def["input_schema"]["required"] = tool["required"]
            
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
            # Format the messages
            if messages:
                message_list = messages
            else:
                message_list = [{"role": "user", "content": prompt}]
            
            # Create message parameters
            params = {
                "model": self.model,
                "system": system_prompt,
                "messages": message_list,
                "max_tokens": self.max_tokens
            }
            
            # Add tools if requested
            if with_tools:
                params["tools"] = self._format_tools_for_api()
            
            # Send the request using the anthropic client with streaming
            response_text = ""
            tool_calls = []
            
            # Process the streaming response
            with self.client.messages.stream(**params) as stream:
                for text in stream.text_stream:
                    response_text += text
                
                # Get the final message for tool calls
                final_message = stream.get_final_message()
                
                # Extract tool calls from the final message
                for content in final_message.content:
                    if content.type == "tool_use":
                        # Store tool use information
                        tool_calls.append({
                            "id": content.id,
                            "name": content.name,
                            "parameters": content.input
                        })
            
            # If there are tool calls, process them
            if tool_calls:
                return self._process_tool_calls(final_message, tool_calls, system_prompt, message_list)
            
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
        
        # If initial_response is a Message object, extract text from it
        if hasattr(initial_response, 'content'):
            for content in initial_response.content:
                if content.type == "text":
                    initial_text += content.text
        else:
            # If it's already the text from streaming
            initial_text = initial_response
        
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
                # Create a new message list with the original messages plus tool outputs
                updated_messages = messages.copy()
                
                # Add the assistant's response with tool calls
                assistant_message = {
                    "role": "assistant",
                    "content": []
                }
                
                # Add text content if available
                if initial_text:
                    assistant_message["content"].append({
                        "type": "text",
                        "text": initial_text
                    })
                
                # Add tool calls
                for tool_call in tool_calls:
                    assistant_message["content"].append({
                        "type": "tool_use",
                        "id": tool_call["id"],
                        "name": tool_call["name"],
                        "input": tool_call["parameters"]
                    })
                
                updated_messages.append(assistant_message)
                
                # Add tool outputs as user messages
                for tool_output in tool_outputs:
                    tool_result = json.loads(tool_output["output"])
                    result_text = tool_result.get("result", str(tool_result))
                    
                    # Parse the tool result
                    tool_result_json = json.loads(tool_output["output"])
                    
                    # Create the user message with tool result
                    user_message = {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_output["tool_call_id"],
                                "content": tool_output["output"]  # Use the raw JSON string
                            }
                        ]
                    }
                    updated_messages.append(user_message)
                
                # Create follow-up parameters with the updated messages
                follow_up_params = {
                    "model": self.model,
                    "system": system_prompt,
                    "messages": updated_messages,
                    "max_tokens": self.max_tokens,
                    "tools": self._format_tools_for_api()  # Make sure to include tools in the follow-up request
                }
                
                # Use streaming API for the follow-up response
                follow_up_text = ""
                new_tool_calls = []
                
                with self.client.messages.stream(**follow_up_params) as stream:
                    for text in stream.text_stream:
                        follow_up_text += text
                    
                    # Get the final message to check for additional tool calls
                    final_message = stream.get_final_message()
                    
                    # Extract any new tool calls from the final message
                    for content in final_message.content:
                        if content.type == "tool_use":
                            # Store tool use information
                            new_tool_calls.append({
                                "id": content.id,
                                "name": content.name,
                                "parameters": content.input
                            })
                
                # If there are additional tool calls, process them recursively
                if new_tool_calls:
                    # Recursively process the new tool calls
                    recursive_result = self._process_tool_calls(final_message, new_tool_calls, system_prompt, updated_messages)
                    
                    # Combine the current tool calls/outputs with the recursive ones
                    combined_result = {
                        "thinking": "",
                        "response": recursive_result.get("response", ""),
                        "tool_calls": tool_calls + recursive_result.get("tool_calls", []),
                        "tool_outputs": tool_outputs + recursive_result.get("tool_outputs", [])
                    }
                    
                    self.last_response = combined_result
                    return combined_result
                else:
                    # No more tool calls, return the final result
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
