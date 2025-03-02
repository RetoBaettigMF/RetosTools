import os
import traceback
import anthropic
import json
import time
import datetime
import re
import sys
import subprocess
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from config import Config
from knowledgebase import KnowledgeBase
from researchmanager import ResearchManager
from codemanager import CodeManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("chatbot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("self-improving-chatbot")

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
            with open(self.history_file, "w", encoding='utf-8') as f:
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
    
    def get_context_window(self, window_size: int = 10) -> List[Dict[str, str]]:
        """Get the most recent n messages"""
        return self.messages[-window_size:] if len(self.messages) > window_size else self.messages
        
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
        
        with open(self.history_file, "a", encoding='utf-8') as f:
            f.write(result)
            
        self.try_number += 1
        return result
        
    def extract_code_from_response(self, response: str) -> Optional[str]:
        """Extract Python code blocks from a response"""
        code_blocks = re.findall(r'```python\n(.*?)\n```', response, re.DOTALL)
        if code_blocks:
            return code_blocks[0]
        return None

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
                thinking={"type": "enabled", "budget_tokens": Config.THINKING_BUDGET},
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
            logger.error(f"Claude API error: {str(e)}")
            return {"thinking": "", "research_idea": f"Error: {str(e)}"}

# Progress Tracking
class ProgressTracker:
    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base
        
    def get_dashboard(self) -> Dict[str, Any]:
        """Get a dashboard of current progress towards CEO capabilities"""
        skill_progress = self.knowledge_base.get_skill_progress()
        learning_progress = self.knowledge_base.get_learning_progress()
        
        # Calculate overall progress as weighted average of skills and learning
        overall_readiness = skill_progress["overall_progress"] * 0.7 + (learning_progress["progress_percentage"] / 100) * 0.3
        
        return {
            "version": Config.VERSION,
            "overall_ceo_readiness": overall_readiness,
            "skill_progress": skill_progress,
            "learning_progress": learning_progress,
            "areas_to_improve": skill_progress["areas_to_improve"],
            "next_learning_topic": learning_progress["current_topic"]
        }
    
    def record_interaction(self, interaction_type: str, details: Dict[str, Any]) -> None:
        """Record an interaction for progress tracking"""
        self.knowledge_base.store_knowledge(
            "interactions",
            f"interaction_{interaction_type}_{int(time.time())}",
            {
                "type": interaction_type,
                "timestamp": time.time(),
                "details": details
            }
        )

# Command Processor
class CommandProcessor:
    def __init__(self, knowledge_base: KnowledgeBase, research_manager: ResearchManager, 
                 code_manager: CodeManager, progress_tracker: ProgressTracker):
        self.knowledge_base = knowledge_base
        self.research_manager = research_manager
        self.code_manager = code_manager
        self.progress_tracker = progress_tracker
        
    def process_command(self, command: str, args: List[str]) -> str:
        """Process a command from the user"""
        if command == "help":
            return self._cmd_help()
        elif command == "knowledge":
            return self._cmd_knowledge(args)
        elif command == "learn":
            return self._cmd_learn(args)
        elif command == "skills":
            return self._cmd_skills(args)
        elif command == "progress":
            return self._cmd_progress()
        elif command == "run":
            return self._cmd_run()
        elif command == "code":
            return self._cmd_code(args)
        elif command == "version":
            return self._cmd_version()
        else:
            return f"Unknown command: {command}. Type /help for available commands."
    
    def _cmd_help(self) -> str:
        """Show help information"""
        return (
            "Available commands:\n"
            "/help - Show this help message\n"
            "/knowledge [category] - List knowledge categories or items in a category\n"
            "/learn <topic> - Research and learn about a topic\n"
            "/skills - Show current skill levels\n"
            "/progress - Show progress dashboard\n"
            "/run - Run the new version of the code\n"
            "/code status - Show code status\n"
            "/version - Show current version"
        )
    
    def _cmd_knowledge(self, args: List[str]) -> str:
        """Handle knowledge commands"""
        if not args:
            # List knowledge categories
            categories = self.knowledge_base.list_knowledge()
            return f"Knowledge categories: {', '.join(categories) if categories else 'None'}"
        else:
            # List items in the specified category
            category = args[0]
            items = self.knowledge_base.list_knowledge(category)
            return f"Items in {category}: {', '.join(items) if items else 'None'}"
    
    def _cmd_learn(self, args: List[str]) -> str:
        """Handle learning commands"""
        if not args:
            # Follow the learning plan
            result = self.research_manager.follow_learning_plan()
            if result["status"] == "complete":
                return "Learning plan is complete. Use /learn <topic> to learn about a specific topic."
            else:
                return f"Currently learning: {result['current_topic']}\n" + \
                       f"Progress: {result['progress']['progress_percentage']:.1f}%\n" + \
                       f"Summary: {result['summary'][:200]}..."
        else:
            # Learn about a specific topic
            topic = " ".join(args)
            result = self.research_manager.learn_about_topic(topic)
            return f"Research on: {topic}\n" + \
                   f"Found {len(result['existing_knowledge'])} existing knowledge items\n" + \
                   f"Added {len(result['new_findings'])} new findings"
    
    def _cmd_skills(self, args: List[str]) -> str:
        """Handle skills commands"""
        if not args:
            # Show all skills
            skills = self.knowledge_base.get_skill_progress()
            result = "Current skill levels:\n"
            for skill, level in skills["skills"].items():
                result += f"- {skill}: {level:.2f}\n"
            result += f"\nOverall progress: {skills['overall_progress']:.2f}\n"
            result += f"Areas to improve: {', '.join(skills['areas_to_improve'])}"
            return result
        elif args[0] == "update" and len(args) >= 3:
            # Update a skill level
            skill_name = args[1]
            try:
                new_level = float(args[2])
                self.knowledge_base.update_skill(skill_name, new_level)
                return f"Updated skill {skill_name} to level {new_level}"
            except ValueError:
                return "Error: Skill level must be a number between 0 and 1"
        else:
            return "Usage: /skills or /skills update <skill_name> <level>"
    
    def _cmd_progress(self) -> str:
        """Show progress dashboard"""
        dashboard = self.progress_tracker.get_dashboard()
        result = f"Progress Dashboard (v{dashboard['version']}):\n"
        result += f"Overall CEO readiness: {dashboard['overall_ceo_readiness']:.2f}\n\n"
        
        result += "Learning Progress:\n"
        lp = dashboard["learning_progress"]
        result += f"- {lp['progress_percentage']:.1f}% complete ({lp['topics_completed']}/{lp['total_topics']} topics)\n"
        result += f"- Current topic: {lp['current_topic']}\n\n"
        
        result += "Skill Progress:\n"
        result += f"- Overall skill level: {dashboard['skill_progress']['overall_progress']:.2f}\n"
        result += f"- Areas to improve: {', '.join(dashboard['areas_to_improve'])}\n"
        
        return result
    
    def _cmd_run(self) -> str:
        """Run the new version"""
        success, message = self.code_manager.run_new_version()
        if success:
            return f"{message} Shutting down this instance..."
        else:
            return message
    
    def _cmd_code(self, args: List[str]) -> str:
        """Handle code-related commands"""
        if not args:
            return "Usage: /code status"
        elif args[0] == "status":
            is_valid, message = self.code_manager.test_code()
            if is_valid:
                return "Code status: Valid Python code"
            else:
                return f"Code status: Invalid - {message}"
        else:
            return f"Unknown code command: {args[0]}"
    
    def _cmd_version(self) -> str:
        """Show current version"""
        return f"Current version: {Config.VERSION}"

# Main Application
class SelfImprovingChatbot:
    def __init__(self):
        self.knowledge = KnowledgeBase()
        self.conversation = ConversationManager()
        self.code_manager = CodeManager()
        self.claude = Claude()
        self.research_manager = ResearchManager(self.knowledge)
        self.progress_tracker = ProgressTracker(self.knowledge)
        self.command_processor = CommandProcessor(
            self.knowledge, 
            self.research_manager,
            self.code_manager,
            self.progress_tracker
        )
        
    def prepare_prompt(self, user_input: str) -> str:
        """Prepare the prompt for Claude with current architecture, code and user input"""
        code = self.code_manager.get_current_code("main.py")
        architecture = self.code_manager.get_current_code(Config.ARCHITECTURE_FILE)
        prompt = f"# This is your current architecture:\n{architecture}\n\n"
        prompt = f"# This is your current code:\n```python\n{code}\n```\n\n"
        prompt += f"# {Config.USER_NAME}'s input: {user_input}"
        return prompt
        
    def process_response(self, response: Dict[str, str], user_input: str) -> None:
        """Process Claude's response and look for code improvements"""
        # Extract code if present
        if "research_idea" in response:
            code = self.conversation.extract_code_from_response(response["research_idea"])
            if code:
                # Backup and update the code
                if self.code_manager.update_code(code):
                    logger.info("Code updated successfully!")
                    
                    # Test if the code is valid
                    is_valid, message = self.code_manager.test_code()
                    if is_valid:
                        logger.info("Code is valid Python.")
                    else:
                        logger.warning(f"Warning: {message}")
                        
                    # Extract knowledge if present
                    if "thinking" in response:
                        thinking = response["thinking"]
                        # Process thinking for insights
                        self._process_thinking_for_insights(thinking, user_input)
    
    def _process_thinking_for_insights(self, thinking: str, user_input: str) -> None:
        """Process Claude's thinking to extract insights"""
        # Look for insights about CEO role and software engineering
        if "CEO" in thinking or "software" in thinking or "business" in thinking:
            # Store the insight
            self.knowledge.store_knowledge(
                "insights", 
                f"insight_{int(time.time())}", 
                {
                    "thinking": thinking[:1000],  # Store a larger portion
                    "user_input": user_input,
                    "timestamp": time.time()
                }
            )
            
            # Update skills based on insights
            skill_keywords = {
                "strategic_planning": ["strategy", "planning", "vision", "roadmap"],
                "business_development": ["business development", "growth", "opportunity"],
                "team_leadership": ["leadership", "team", "management", "motivation"],
                "financial_management": ["finance", "budget", "cost", "profit"],
                "market_analysis": ["market", "competition", "industry", "trend"],
                "software_development_knowledge": ["software", "development", "coding", "programming"],
                "client_relations": ["client", "customer", "relationship", "satisfaction"],
                "technical_vision": ["technical", "architecture", "vision", "innovation"],
                "risk_management": ["risk", "mitigation", "contingency", "security"],
                "communication": ["communication", "presentation", "speaking", "writing"],
                "decision_making": ["decision", "judgment", "choice", "analysis"],
                "industry_knowledge": ["industry", "sector", "domain", "expertise"]
            }
            
            # Check for skill-related content and slightly improve relevant skills
            for skill, keywords in skill_keywords.items():
                for keyword in keywords:
                    if keyword.lower() in thinking.lower():
                        # Get current skill level
                        current_level = self.knowledge.skill_model.skills.get(skill, 0.1)
                        # Increase slightly (max 0.03 per interaction)
                        self.knowledge.update_skill(skill, min(current_level + 0.01, 1.0))
                        break
    
    def process_command(self, user_input: str) -> Optional[str]:
        """Process a command if the input is a command"""
        if user_input.startswith('/'):
            parts = user_input[1:].split(' ')
            command = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []
            
            result = self.command_processor.process_command(command, args)
            
            # Record this command interaction
            self.progress_tracker.record_interaction(
                "command",
                {"command": command, "args": args}
            )
            
            # Special case for run command
            if command == "run" and "Shutting down" in result:
                print(result)
                sys.exit(0)
                
            return result
        return None
    
    def save_response(self, response: Dict[str, str]) -> None:
        """Save the response to a file"""     
        with open("response.json", "w") as f:
            json.dump(response, f, indent=4)

    def load_response(self) -> Optional[Dict[str, str]]:
        """Load a response from a file"""     
        if os.path.exists("response.json"):
            with open("response.json", "r") as f:
                return json.load(f)
        
    def run(self) -> None:
        """Main run loop"""
        print(f"Reto's Self-Improving Chatbot v{Config.VERSION}\n")
        print("------------------------------")
        print("Type /help for available commands or 'quit' to exit\n")
        
        # Show initial progress
        print(self.command_processor.process_command("progress", []))
        print("\n")
        error = None
            
        while True:
            if (not error):
                user_input = input(f"{Config.USER_NAME}'s input: ")
                
                # Handle empty input
                if user_input == "":
                    user_input = "Ok. Write the next version of yourself."
                    
                # Handle exit commands
                if user_input.lower() in ['quit', 'exit']:
                    print("Goodbye!")
                    break
                
                # Handle special commands
                if user_input.startswith('/'):
                    result = self.process_command(user_input)
                    if result:
                        print(result)
                        continue
                
            else: 
                user_input = error
                
            try:
                # Record this interaction
                self.progress_tracker.record_interaction(
                    "conversation",
                    {"user_input": user_input}
                )
                    
                # Normal flow - ask Claude
                prompt = self.prepare_prompt(user_input)
                self.conversation.add_user_message(prompt)
                
                print("Thinking...")
                if user_input.lower() in ['repeat', 'retry']:
                    response = self.load_response()
                else:   
                    response = self.claude.ask(self.conversation.get_messages())
                    self.save_response(response)
                
                # Add response to conversation history
                if "research_idea" in response:
                    self.conversation.add_assistant_message(response["research_idea"])
                    
                # Process and log the interaction
                formatted_response = self.conversation.log_interaction(prompt, response)
                print(formatted_response)
                
                # Process the response for potential code updates and knowledge extraction
                self.process_response(response, user_input)
                
                # After processing a response that might relate to the learning plan,
                # check if we should advance in the learning plan
                current_topic = self.knowledge.learning_plan.get_current_topic()
                if current_topic:
                    topic_name = current_topic["name"].lower()
                    if topic_name in user_input.lower() or topic_name in response.get("research_idea", "").lower():
                        # This interaction was related to the current learning topic
                        # There's a chance we should mark it as complete
                        if "complete" in user_input.lower() or "finished" in user_input.lower():
                            self.knowledge.complete_current_learning_topic()
                            print(f"Marked learning topic '{topic_name}' as complete!")
                error = None
            except Exception as e:
                error_message = f"Error: {str(e)}"
    
                # Get the stack trace
                stack_trace = traceback.format_exc()
    
                # Combine the error message and stack trace
                error = f"{error_message}\nStack Trace:\n{stack_trace}"
                logger.error(error)
                print(error)
                print("Trying again.")

# Entry point
def main():
    # Ensure all directories exist
    Config.ensure_directories()
    
    # Initialize and run the chatbot
    chatbot = SelfImprovingChatbot()
    chatbot.run()

if __name__ == "__main__":
    main()

"""
Your self improvement mechanism uses to many tokens. Implement a plan to improve that situation. E.g. make multiple code files and add Function calling to read them if needed. You could also consider documenting the architecture of the code and read it first when needed instead of reading the whole code.
"""