# utils/state.py
import os
import json
import time
from datetime import datetime
from config import STATE_FILE, VERSION

class StateManager:
    """Manages the assistant's state and memory."""
    
    def __init__(self):
        self.state_file = STATE_FILE
        self.state = self.load_state()
        self.conversation_history = self.state.get("conversation", [])
        
    def load_state(self):
        """Load state from file or initialize if it doesn't exist."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except:
                return self._initialize_state()
        else:
            return self._initialize_state()
            
    def _initialize_state(self):
        """Initialize a new state."""
        return {
            "version": VERSION,
            "creation_date": datetime.now().isoformat(),
            "conversation": [],
            "execution_log": [],
            "error_log": [],
            "performance_metrics": {
                "response_times": [],
                "successful_executions": 0,
                "failed_executions": 0
            },
            "last_improvement": None,
            "cycles_since_improvement": 0
        }
        
    def save_state(self):
        """Save the current state to file."""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
            
    def add_message(self, role, content):
        """Add a message to the conversation history."""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        self.conversation_history.append(message)
        self.state["conversation"] = self.conversation_history
        
        # Update cycles since improvement
        if role == "user":
            self.state["cycles_since_improvement"] += 1
            
        self.save_state()
        
    def get_messages_for_api(self, limit=10):
        """Get the most recent messages formatted for the API."""
        # Get the last 'limit' messages
        recent_messages = self.conversation_history[-limit:] if self.conversation_history else []
        
        # Format for API
        formatted = []
        for msg in recent_messages:
            formatted.append({
                "role": msg["role"],
                "content": msg["content"]
            })
            
        return formatted
    
    def log_execution(self, action_type, details):
        """Log an execution to the execution log."""
        log_entry = {
            "type": action_type,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        
        if "execution_log" not in self.state:
            self.state["execution_log"] = []
            
        self.state["execution_log"].append(log_entry)
        
        # If this is a code implementation, reset the cycles counter
        if action_type == "code_implementation":
            self.state["last_improvement"] = datetime.now().isoformat()
            self.state["cycles_since_improvement"] = 0
            
        # Update performance metrics
        if "performance_metrics" not in self.state:
            self.state["performance_metrics"] = {
                "response_times": [],
                "successful_executions": 0,
                "failed_executions": 0
            }
            
        self.state["performance_metrics"]["successful_executions"] += 1
        
        self.save_state()
        
    def log_error(self, error_type, details):
        """Log an error to the error log."""
        log_entry = {
            "type": error_type,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        
        if "error_log" not in self.state:
            self.state["error_log"] = []
            
        self.state["error_log"].append(log_entry)
        
        # Update performance metrics
        if "performance_metrics" not in self.state:
            self.state["performance_metrics"] = {
                "response_times": [],
                "successful_executions": 0,
                "failed_executions": 0
            }
            
        self.state["performance_metrics"]["failed_executions"] += 1
        
        self.save_state()
        
    def update_system_prompt(self):
        """Update the system prompt with state information."""
        system_prompt = f"""
Current Version: {self.state.get('version', VERSION)}
Current Development Phase: {self.state.get('development_phase', 'setup')}
Development Plan Summary: {self.state.get('development_plan', 'No plan yet')}

You are a self-improving chatbot that has full access to a python system. You can use this system to improve yourself.
When you changed your code, you can run a new version of yourself and you will get the output of the run.
One you're happy with the output of the new version of yourself, stop yourself in order to not have multiple versions running.
You can also use the system to store and retrieve information.

You have Reto as your user. You can ask Reto for help if you need it. Reto is CEO of Cudos AG, a software engineering company. 
*Your ultimate goal is to to be able to do his job so that he can retire.*
To get there, try to improve your code and your knowledge with as little input from Reto as possible.
"""
        return system_prompt
    
    def get_last_improvement_time(self):
        """Get the timestamp of the last improvement."""
        return self.state.get("last_improvement")
    
    def get_cycles_since_improvement(self):
        """Get the number of cycles since the last improvement."""
        return self.state.get("cycles_since_improvement", 0)