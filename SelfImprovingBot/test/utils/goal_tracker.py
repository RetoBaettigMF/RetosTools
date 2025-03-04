# utils/goal_tracker.py
import os
import json
import re
from datetime import datetime

class GoalTracker:
    """Tracks progress towards goals and milestones."""
    
    def __init__(self):
        self.goals_dir = "goals"
        self.ensure_goals_dir()
        self.current_goals = []
        self.completed_goals = []
        
    def ensure_goals_dir(self):
        """Ensure goals directory exists."""
        if not os.path.exists(self.goals_dir):
            os.makedirs(self.goals_dir)
    
    def load_goals_for_version(self, version):
        """Load goals for a specific version."""
        # Initialize with default goals if we don't have specific ones for this version
        self._initialize_default_goals(version)
        
        # Try to load version-specific goals
        goals_file = os.path.join(self.goals_dir, f"goals_v{version}.json")
        if os.path.exists(goals_file):
            try:
                with open(goals_file, 'r') as f:
                    data = json.load(f)
                    self.current_goals = data.get("current_goals", [])
                    self.completed_goals = data.get("completed_goals", [])
            except Exception as e:
                print(f"Error loading goals: {str(e)}")
                
    def _initialize_default_goals(self, version):
        """Initialize default goals if none exist for this version."""
        # Clear existing goals
        self.current_goals = []
        self.completed_goals = []
        
        # Define basic goals by version
        if version == "0.1.0":
            self.current_goals = [
                {"id": "g1", "name": "Set up basic system architecture", "progress": 100, "criteria": "System runs and responds to input"},
                {"id": "g2", "name": "Implement basic knowledge capture", "progress": 0, "criteria": "Can extract and store knowledge from conversations"}
            ]
        elif version == "0.2.0":
            self.current_goals = [
                {"id": "g1", "name": "Implement knowledge management", "progress": 0, "criteria": "Can store, retrieve, and use knowledge"},
                {"id": "g2", "name": "Add goal tracking", "progress": 0, "criteria": "System tracks progress towards being CEO-capable"},
                {"id": "g3", "name": "Learn about Reto's company", "progress": 0, "criteria": "Gather basic information about Cudos AG"}
            ]
        elif version.startswith("0.3"):
            self.current_goals = [
                {"id": "g1", "name": "Develop basic business analytics", "progress": 0, "criteria": "Can analyze simple business metrics"},
                {"id": "g2", "name": "Implement decision support system", "progress": 0, "criteria": "Can help with basic decision-making"},
                {"id": "g3", "name": "Learn software engineering best practices", "progress": 0, "criteria": "Understand software development lifecycle"}
            ]
        else:
            # Generic goals for any version
            self.current_goals = [
                {"id": "g1", "name": "Improve knowledge base", "progress": 0, "criteria": "Continuously add relevant knowledge"},
                {"id": "g2", "name": "Learn about CEO responsibilities", "progress": 0, "criteria": "Understand key CEO tasks and skills"},
                {"id": "g3", "name": "Develop self-improvement capabilities", "progress": 0, "criteria": "Can identify and fix own limitations"}
            ]
            
        # Save the goals
        self.save_goals(version)
        
    def save_goals(self, version):
        """Save the current goals."""
        goals_file = os.path.join(self.goals_dir, f"goals_v{version}.json")
        data = {
            "current_goals": self.current_goals,
            "completed_goals": self.completed_goals,
            "last_updated": datetime.now().isoformat()
        }
        
        with open(goals_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_goal(self, name, criteria, version):
        """Add a new goal."""
        goal_id = f"g{len(self.current_goals) + len(self.completed_goals) + 1}"
        goal = {
            "id": goal_id,
            "name": name,
            "progress": 0,
            "criteria": criteria,
            "created": datetime.now().isoformat()
        }
        
        self.current_goals.append(goal)
        self.save_goals(version)
        return goal
    
    def update_goal_progress(self, goal_id, progress, version):
        """Update progress on a goal."""
        for goal in self.current_goals:
            if goal["id"] == goal_id:
                goal["progress"] = min(100, max(0, progress))  # Ensure 0-100 range
                goal["last_updated"] = datetime.now().isoformat()
                
                # If goal is completed, move it to completed list
                if goal["progress"] >= 100:
                    goal["completed"] = datetime.now().isoformat()
                    self.completed_goals.append(goal)
                    self.current_goals.remove(goal)
                
                self.save_goals(version)
                return True
        return False
    
    def check_progress(self):
        """Check which goals were completed in this session."""
        # Note: In a real implementation, we'd track which goals were completed
        # in the current session. For now, just return the most recent completions.
        completed = []
        for goal in self.completed_goals:
            if "completed" in goal:
                completed.append(goal["name"])
                
        # Format in-progress goals with progress
        in_progress = {}
        for goal in self.current_goals:
            in_progress[goal["name"]] = goal["progress"]
            
        return completed[-3:] if completed else [], in_progress
    
    def update_progress_from_response(self, response):
        """Update goal progress based on the response content."""
        # Look for explicit progress updates
        progress_pattern = r"GOAL PROGRESS:\s*([^|]+)\|(\d+)"
        matches = re.findall(progress_pattern, response, re.DOTALL)
        
        updated = False
        for goal_name, progress_str in matches:
            goal_name = goal_name.strip()
            progress = int(progress_str.strip())
            
            # Find the goal by name
            for goal in self.current_goals:
                if goal["name"].lower() == goal_name.lower():
                    goal["progress"] = min(100, max(goal["progress"], progress))
                    updated = True
                    break
        
        # Update based on content analysis
        if not updated:
            # This is a simplified example - in practice, we'd use a more 
            # sophisticated analysis of the response to update goal progress
            
            # For the knowledge-related goal
            for goal in self.current_goals:
                if "knowledge" in goal["name"].lower():
                    if "KNOWLEDGE:" in response:
                        goal["progress"] = min(100, goal["progress"] + 10)
                        updated = True
                
                elif "reto's company" in goal["name"].lower():
                    if "Cudos AG" in response and "software engineering" in response:
                        goal["progress"] = min(100, goal["progress"] + 15)
                        updated = True
                
                elif "ceo" in goal["name"].lower():
                    if "CEO" in response and ("responsibilities" in response or "skills" in response):
                        goal["progress"] = min(100, goal["progress"] + 10)
                        updated = True
        
        # Save if we made updates
        if updated:
            # We don't have version here, but we can get it from the state manager instance
            # For now, use a placeholder
            self.save_goals("current")
    
    def display_all_goals(self):
        """Display all goals and their progress."""
        print("\n=== Current Goals ===")
        for goal in self.current_goals:
            print(f"{goal['id']}: {goal['name']} - {goal['progress']}% complete")
            print(f"   Criteria: {goal['criteria']}")
        
        print("\n=== Completed Goals ===")
        for goal in self.completed_goals:
            completed_date = goal.get("completed", "Unknown date")
            if isinstance(completed_date, str) and completed_date.startswith("20"):
                completed_date = completed_date.split("T")[0]  # Format date
            print(f"{goal['id']}: {goal['name']} - Completed on {completed_date}")