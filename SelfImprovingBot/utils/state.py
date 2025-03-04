import json
import os
import time
import datetime
from config import STATE_FILE, VERSIONS_DIR, VERSION, BASE_SYSTEM_PROMPT, DEVELOPMENT_PHASES
from utils.commands import Commands

class StateManager:
    def __init__(self):
        self.state = {
            "version": VERSION,
            "start_time": time.time(),
            "last_update": time.time(),
            "system_prompt": BASE_SYSTEM_PROMPT,
            "development_phase": DEVELOPMENT_PHASES[0],
            "development_plan": {},
            "execution_log": [],
            "messages": []
        }
        
        # Create necessary directories
        Commands.create_directory(VERSIONS_DIR)
        
        # Load state if it exists
        self.load_state()
        
    def load_state(self):
        """Load the state from the state file if it exists."""
        if os.path.exists(STATE_FILE):
            try:
                state_content = Commands.read_file(STATE_FILE)
                loaded_state = json.loads(state_content)
                
                # Update the state with the loaded values
                self.state.update(loaded_state)
                
                # Always update the last update time
                self.state["last_update"] = time.time()
                return True
            except Exception as e:
                print(f"Error loading state: {str(e)}")
                return False
        return False
    
    def save_state(self):
        """Save the current state to the state file."""
        try:
            # Update last update time
            self.state["last_update"] = time.time()
            state_content = json.dumps(self.state, indent=2)
            Commands.write_file(STATE_FILE, state_content)
            return True
        except Exception as e:
            print(f"Error saving state: {str(e)}")
            return False
    
    def update_system_prompt(self, new_prompt=None):
        """Update the system prompt with current state and save."""
        if new_prompt:
            self.state["system_prompt"] = new_prompt
        
        # Create a dynamic system prompt that includes the current state
        current_phase = self.state["development_phase"]
        plan = self.state.get("development_plan", {})
        
        # Add dynamic information to the system prompt
        dynamic_prompt = f"""
Current Version: {self.state["version"]}
Current Development Phase: {current_phase}
Development Plan Summary: {json.dumps(plan, indent=2) if plan else "No plan yet"}

{BASE_SYSTEM_PROMPT}
"""
        self.state["system_prompt"] = dynamic_prompt
        self.save_state()
        return self.state["system_prompt"]
        
    def update_development_plan(self, plan):
        """Update the development plan and save the state."""
        self.state["development_plan"] = plan
        self.save_state()
        
    def advance_development_phase(self, new_phase=None):
        """Move to the next development phase or a specific one."""
        if new_phase and new_phase in DEVELOPMENT_PHASES:
            self.state["development_phase"] = new_phase
        else:
            current_index = DEVELOPMENT_PHASES.index(self.state["development_phase"])
            if current_index < len(DEVELOPMENT_PHASES) - 1:
                self.state["development_phase"] = DEVELOPMENT_PHASES[current_index + 1]
        
        # Update system prompt with new phase
        self.update_system_prompt()
        self.save_state()
        
    def log_execution(self, action, details=None):
        """Log an execution event."""
        log_entry = {
            "action": action,
            "timestamp": datetime.datetime.now().isoformat(),
            "details": details or {}
        }
        self.state["execution_log"].append(log_entry)
        
        # Keep only the last 100 log entries to save space
        if len(self.state["execution_log"]) > 100:
            self.state["execution_log"] = self.state["execution_log"][-100:]
            
        self.save_state()
        
    def add_message(self, role, content):
        """Add a message to the conversation history."""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.state["messages"].append(message)
        
        # Only keep the last 5 messages to save tokens
        if len(self.state["messages"]) > 5:
            self.state["messages"] = self.state["messages"][-5:]
            
        self.save_state()
        
    def get_messages_for_api(self):
        """Get the messages in a format suitable for the Claude API."""
        return [{"role": msg["role"], "content": msg["content"]} for msg in self.state["messages"]]
    
    def get_system_prompt(self):
        """Get the current system prompt."""
        return self.state["system_prompt"]
    
    def get_development_phase(self):
        """Get the current development phase."""
        return self.state["development_phase"]
    
    def backup_state(self):
        """Create a timestamped backup of the current state."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        backup_file = os.path.join(VERSIONS_DIR, f"state_{timestamp}.json")
        Commands.write_file(backup_file, json.dumps(self.state, indent=2))
        return backup_file