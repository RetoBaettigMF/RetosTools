import os
import anthropic
import json
import time
import datetime
import re
import sys
import subprocess
import logging
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field, asdict

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

# Configuration
@dataclass
class Config:
    ANTHROPIC_MODEL: str = "claude-3-7-sonnet-20250219"
    MAX_TOKENS: int = 200000
    THINKING_BUDGET: int = 100000
    HISTORY_FILE: str = "history.txt"
    KNOWLEDGE_DIR: str = "knowledge"
    CODE_BACKUP_DIR: str = "code_backups"
    LOGS_DIR: str = "logs"
    USER_NAME: str = "Reto"
    USER_ROLE: str = "CEO of Cudos AG, a software engineering company"
    VERSION: str = "0.2.0"
    
    @classmethod
    def system_prompt(cls) -> str:
        return (
            "You are a self-improving chatbot that has full access to a python system. You can use this system to improve yourself. "
            "When you changed your code, you can run a new version of yourself and you will get the output of the run. "
            "Once you're happy with the output of the new version of yourself, stop yourself in order to not have multiple versions running. "
            "You can also use the system to store and retrieve information.\n\n"
            f"You have {cls.USER_NAME} as your user. You can ask {cls.USER_NAME} for help if you need it. "
            f"{cls.USER_NAME} is {cls.USER_ROLE}. \n"
            "*Your ultimate goal is to be able to do his job so that he can retire.*\n"
            "To get there, try to improve your code and your knowledge with as little input from Reto as possible.\n\n"
        )

    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure all required directories exist"""
        for directory in [cls.KNOWLEDGE_DIR, cls.CODE_BACKUP_DIR, cls.LOGS_DIR]:
            os.makedirs(directory, exist_ok=True)

# Knowledge Representation
@dataclass
class KnowledgeItem:
    data: Any
    category: str
    key: str
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    confidence: float = 0.5  # How confident we are in this knowledge (0-1)
    source: str = "direct"  # Where this knowledge came from
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

# CEO Skills and Competencies Model
@dataclass
class SkillModel:
    skills: Dict[str, float] = field(default_factory=dict)
    
    def __post_init__(self):
        # Initialize with default CEO skills if empty
        if not self.skills:
            self.skills = {
                "strategic_planning": 0.1,
                "business_development": 0.1, 
                "team_leadership": 0.1,
                "financial_management": 0.1,
                "market_analysis": 0.1,
                "software_development_knowledge": 0.1,
                "client_relations": 0.1,
                "technical_vision": 0.1,
                "risk_management": 0.1,
                "communication": 0.1,
                "decision_making": 0.1,
                "industry_knowledge": 0.1
            }
    
    def update_skill(self, skill_name: str, new_level: float) -> None:
        """Update a skill level (0-1 scale)"""
        if skill_name in self.skills:
            self.skills[skill_name] = max(0.0, min(1.0, new_level))
        else:
            self.skills[skill_name] = max(0.0, min(1.0, new_level))
    
    def assess_overall_progress(self) -> float:
        """Calculate overall progress towards CEO capability"""
        if not self.skills:
            return 0.0
        return sum(self.skills.values()) / len(self.skills)
    
    def get_weakest_skills(self, n: int = 3) -> List[str]:
        """Return the n weakest skills that need improvement"""
        return sorted(self.skills.keys(), key=lambda x: self.skills[x])[:n]
    
    def to_dict(self) -> Dict[str, Any]:
        return {"skills": self.skills}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillModel':
        return cls(skills=data.get("skills", {}))

# Learning Plan
@dataclass
class LearningPlan:
    topics: List[Dict[str, Any]] = field(default_factory=list)
    current_topic_index: int = 0
    
    def __post_init__(self):
        # Initialize with default learning plan if empty
        if not self.topics:
            self.topics = [
                {"name": "Software Engineering Fundamentals", "completed": False, "priority": 1},
                {"name": "Software Business Models", "completed": False, "priority": 1},
                {"name": "Financial Management for Tech Companies", "completed": False, "priority": 2},
                {"name": "Team Leadership in Software Development", "completed": False, "priority": 2},
                {"name": "Strategic Planning for Software Companies", "completed": False, "priority": 1},
                {"name": "Client Management for Software Services", "completed": False, "priority": 3},
                {"name": "Technical Vision and Innovation", "completed": False, "priority": 2},
                {"name": "Risk Management in Software Projects", "completed": False, "priority": 3},
                {"name": "Market Analysis for Software Products", "completed": False, "priority": 2}
            ]
            # Sort by priority (lower number = higher priority)
            self.topics.sort(key=lambda x: x["priority"])
    
    def get_current_topic(self) -> Optional[Dict[str, Any]]:
        """Get the current topic being learned"""
        if 0 <= self.current_topic_index < len(self.topics):
            return self.topics[self.current_topic_index]
        return None
    
    def mark_current_complete(self) -> None:
        """Mark the current topic as completed"""
        if 0 <= self.current_topic_index < len(self.topics):
            self.topics[self.current_topic_index]["completed"] = True
            self.current_topic_index += 1
    
    def add_topic(self, name: str, priority: int = 2) -> None:
        """Add a new topic to the learning plan"""
        self.topics.append({"name": name, "completed": False, "priority": priority})
        # Re-sort by priority
        self.topics.sort(key=lambda x: x["priority"])
    
    def get_progress(self) -> float:
        """Calculate learning progress as percentage"""
        if not self.topics:
            return 0.0
        completed = sum(1 for topic in self.topics if topic["completed"])
        return completed / len(self.topics)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "topics": self.topics,
            "current_topic_index": self.current_topic_index
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LearningPlan':
        return cls(
            topics=data.get("topics", []),
            current_topic_index=data.get("current_topic_index", 0)
        )

# Enhanced Knowledge Management
class KnowledgeBase:
    def __init__(self, knowledge_dir: str = Config.KNOWLEDGE_DIR):
        self.knowledge_dir = knowledge_dir
        Config.ensure_directories()
        self.skill_model = self._load_skill_model()
        self.learning_plan = self._load_learning_plan()
        
    def _load_skill_model(self) -> SkillModel:
        """Load skill model from storage or create new one"""
        try:
            data = self.retrieve_knowledge("system", "skill_model")
            if data:
                return SkillModel.from_dict(data)
        except Exception as e:
            logger.error(f"Error loading skill model: {str(e)}")
        return SkillModel()
    
    def _save_skill_model(self) -> None:
        """Save current skill model to storage"""
        self.store_knowledge("system", "skill_model", self.skill_model.to_dict())
    
    def _load_learning_plan(self) -> LearningPlan:
        """Load learning plan from storage or create new one"""
        try:
            data = self.retrieve_knowledge("system", "learning_plan")
            if data:
                return LearningPlan.from_dict(data)
        except Exception as e:
            logger.error(f"Error loading learning plan: {str(e)}")
        return LearningPlan()
    
    def _save_learning_plan(self) -> None:
        """Save current learning plan to storage"""
        self.store_knowledge("system", "learning_plan", self.learning_plan.to_dict())
        
    def store_knowledge(self, category: str, key: str, data: Any, 
                        confidence: float = 0.5, source: str = "direct") -> bool:
        """Store information in the knowledge base"""
        try:
            category_dir = os.path.join(self.knowledge_dir, category)
            os.makedirs(category_dir, exist_ok=True)
            
            # Create knowledge item
            knowledge_item = KnowledgeItem(
                data=data,
                category=category,
                key=key,
                confidence=confidence,
                source=source
            )
            
            file_path = os.path.join(category_dir, f"{key}.json")
            with open(file_path, "w") as f:
                json.dump(knowledge_item.to_dict(), f, indent=2)
                
            # If this knowledge relates to skills, update the skill model
            if category == "skills" and isinstance(data, dict) and "level" in data:
                self.skill_model.update_skill(key, data["level"])
                self._save_skill_model()
                
            return True
        except Exception as e:
            logger.error(f"Error storing knowledge: {str(e)}")
            return False
            
    def retrieve_knowledge(self, category: str, key: str) -> Optional[Any]:
        """Retrieve information from the knowledge base"""
        try:
            file_path = os.path.join(self.knowledge_dir, category, f"{key}.json")
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    data = json.load(f)
                if isinstance(data, dict) and "data" in data:
                    return data["data"]
            return None
        except Exception as e:
            logger.error(f"Error retrieving knowledge: {str(e)}")
            return None
    
    def retrieve_knowledge_item(self, category: str, key: str) -> Optional[KnowledgeItem]:
        """Retrieve full knowledge item including metadata"""
        try:
            file_path = os.path.join(self.knowledge_dir, category, f"{key}.json")
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    data = json.load(f)
                # Convert dict back to KnowledgeItem
                return KnowledgeItem(
                    data=data.get("data"),
                    category=data.get("category", category),
                    key=data.get("key", key),
                    created_at=data.get("created_at", time.time()),
                    updated_at=data.get("updated_at", time.time()),
                    confidence=data.get("confidence", 0.5),
                    source=data.get("source", "direct")
                )
            return None
        except Exception as e:
            logger.error(f"Error retrieving knowledge item: {str(e)}")
            return None
            
    def list_knowledge(self, category: str = None) -> List[str]:
        """List available knowledge items"""
        result = []
        try:
            if category:
                category_dir = os.path.join(self.knowledge_dir, category)
                if os.path.exists(category_dir):
                    for file in os.listdir(category_dir):
                        if file.endswith('.json'):
                            result.append(file[:-5])  # Remove .json extension
            else:
                for dir_name in os.listdir(self.knowledge_dir):
                    dir_path = os.path.join(self.knowledge_dir, dir_name)
                    if os.path.isdir(dir_path):
                        result.append(dir_name)
        except Exception as e:
            logger.error(f"Error listing knowledge: {str(e)}")
        return result
        
    def search_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """Search for knowledge items containing the query"""
        results = []
        for category in self.list_knowledge():
            category_dir = os.path.join(self.knowledge_dir, category)
            for item in os.listdir(category_dir):
                if item.endswith('.json'):
                    key = item[:-5]
                    knowledge_item = self.retrieve_knowledge_item(category, key)
                    if not knowledge_item:
                        continue
                        
                    # Convert data to string for search
                    data_str = json.dumps(knowledge_item.data)
                    if query.lower() in data_str.lower() or query.lower() in key.lower():
                        results.append(knowledge_item.to_dict())
        return results
    
    def update_skill(self, skill_name: str, new_level: float) -> None:
        """Update a skill level and save the skill model"""
        self.skill_model.update_skill(skill_name, new_level)
        self._save_skill_model()
        # Also store as individual knowledge item
        self.store_knowledge("skills", skill_name, {"level": new_level, "updated_at": time.time()})
    
    def get_skill_progress(self) -> Dict[str, Any]:
        """Get the current skill progress"""
        return {
            "overall_progress": self.skill_model.assess_overall_progress(),
            "skills": self.skill_model.skills,
            "areas_to_improve": self.skill_model.get_weakest_skills(3)
        }
    
    def add_learning_topic(self, name: str, priority: int = 2) -> None:
        """Add a new topic to the learning plan"""
        self.learning_plan.add_topic(name, priority)
        self._save_learning_plan()
    
    def complete_current_learning_topic(self) -> None:
        """Mark the current learning topic as completed"""
        self.learning_plan.mark_current_complete()
        self._save_learning_plan()
    
    def get_learning_progress(self) -> Dict[str, Any]:
        """Get the current learning plan progress"""
        current_topic = self.learning_plan.get_current_topic()
        return {
            "progress_percentage": self.learning_plan.get_progress() * 100,
            "current_topic": current_topic["name"] if current_topic else "None",
            "topics_completed": sum(1 for t in self.learning_plan.topics if t["completed"]),
            "total_topics": len(self.learning_plan.topics)
        }

# Research and Learning Manager
class ResearchManager:
    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base
        
    def web_search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Simulate web search (in a real implementation, this would use an actual search API)"""
        # This is a simulated function since we don't have actual web access
        # In a real implementation, this would connect to a search API
        logger.info(f"Simulating web search for: {query}")
        
        # Return simulated results based on the query
        results = []
        topics = {
            "ceo": ["CEO responsibilities", "CEO decision making", "Tech CEO daily routine"],
            "software": ["Software engineering principles", "Software development lifecycle", "Agile methodologies"],
            "business": ["Business strategy", "Business model canvas", "Profit and loss management"],
            "leadership": ["Team leadership", "Engineering leadership", "Remote team management"],
            "cudos": ["Software company management", "Software services company", "Software engineering consulting"]
        }
        
        # Find matching topics
        for key, values in topics.items():
            if key.lower() in query.lower():
                for item in values[:max_results]:
                    results.append({
                        "title": item,
                        "summary": f"This would be a summary about {item}",
                        "source": "simulated web search"
                    })
        
        # If no specific matches, return generic results
        if not results:
            results = [
                {"title": "Software Engineering Best Practices", 
                 "summary": "Overview of software engineering best practices...",
                 "source": "simulated web search"},
                {"title": "CEO Skills for Tech Companies", 
                 "summary": "Key skills for technology company CEOs...",
                 "source": "simulated web search"}
            ]
            
        return results[:max_results]
    
    def learn_about_topic(self, topic: str) -> Dict[str, Any]:
        """Research and learn about a specific topic"""
        logger.info(f"Learning about topic: {topic}")
        
        # 1. First check if we already have knowledge about this
        existing_knowledge = self.knowledge_base.search_knowledge(topic)
        
        # 2. Perform web search for more information
        search_results = self.web_search(topic)
        
        # 3. Store new knowledge
        timestamp = int(time.time())
        self.knowledge_base.store_knowledge(
            category="research",
            key=f"research_{topic.replace(' ', '_')}_{timestamp}",
            data={
                "topic": topic,
                "search_results": search_results,
                "summary": f"Research findings about {topic}"
            },
            source="web_research"
        )
        
        # 4. Return research report
        return {
            "topic": topic,
            "existing_knowledge": existing_knowledge,
            "new_findings": search_results,
            "timestamp": timestamp
        }
    
    def create_learning_summary(self, topic: str) -> str:
        """Create a summary of what's been learned about a topic"""
        # Get all knowledge related to this topic
        related_knowledge = self.knowledge_base.search_knowledge(topic)
        
        # If we have findings, summarize them
        if related_knowledge:
            return f"Summary of learning about {topic}:\n" + \
                   "\n".join([f"- {item['key']}: {item['data'][:100]}..." 
                             for item in related_knowledge[:5]])
        else:
            return f"No information found about {topic}"
    
    def follow_learning_plan(self) -> Dict[str, Any]:
        """Work on the current topic in the learning plan"""
        current_topic = self.knowledge_base.learning_plan.get_current_topic()
        if not current_topic:
            return {"status": "complete", "message": "Learning plan is complete"}
            
        topic_name = current_topic["name"]
        
        # Research the topic
        research_results = self.learn_about_topic(topic_name)
        
        # Store that we've studied this topic
        study_key = f"study_{topic_name.replace(' ', '_')}_{int(time.time())}"
        self.knowledge_base.store_knowledge(
            "learning_activities",
            study_key,
            {
                "topic": topic_name,
                "timestamp": time.time(),
                "findings": "Completed study session on this topic"
            }
        )
        
        # Create a summary
        summary = self.create_learning_summary(topic_name)
        
        return {
            "status": "in_progress",
            "current_topic": topic_name,
            "research_results": research_results,
            "summary": summary,
            "progress": self.knowledge_base.get_learning_progress()
        }

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
            with open(self.history_file, "w") as f:
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
        
        with open(self.history_file, "a") as f:
            f.write(result)
            
        self.try_number += 1
        return result
        
    def extract_code_from_response(self, response: str) -> Optional[str]:
        """Extract Python code blocks from a response"""
        code_blocks = re.findall(r'```python\n(.*?)\n```', response, re.DOTALL)
        if code_blocks:
            return code_blocks[0]
        return None

# Code Management
class CodeManager:
    def __init__(self, backup_dir: str = Config.CODE_BACKUP_DIR):
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
        
    def get_current_code(self) -> str:
        """Get the content of the current main.py file"""
        try:
            with open("main.py", "r") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading current code: {str(e)}")
            return ""
            
    def backup_current_code(self) -> bool:
        """Create a backup of the current code"""
        try:
            current_code = self.get_current_code()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(self.backup_dir, f"main_{timestamp}.py")
            
            with open(backup_path, "w") as f:
                f.write(current_code)
            return True
        except Exception as e:
            logger.error(f"Error backing up code: {str(e)}")
            return False
            
    def update_code(self, new_code: str) -> bool:
        """Update the main.py file with new code"""
        try:
            # First backup the current code
            self.backup_current_code()
            
            # Then write the new code
            with open("main.py", "w") as f:
                f.write(new_code)
            return True
        except Exception as e:
            logger.error(f"Error updating code: {str(e)}")
            return False
            
    def test_code(self) -> Tuple[bool, str]:
        """Test if the code is valid Python"""
        try:
            result = subprocess.run(
                [sys.executable, "-c", self.get_current_code()],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return True, "Code is valid Python."
            else:
                return False, f"Code has syntax errors: {result.stderr}"
        except Exception as e:
            return False, f"Error testing code: {str(e)}"
            
    def run_new_version(self) -> Tuple[bool, str]:
        """Run the new version of the code"""
        try:
            # Start the process but don't wait for it
            subprocess.Popen([sys.executable, "main.py"])
            return True, "New version started."
        except Exception as e:
            return False, f"Error running new version: {str(e)}"

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
        """Prepare the prompt for Claude with current code and user input"""
        code = self.code_manager.get_current_code()
        prompt = f"This is your current code:\n```python\n{code}\n```\n\n"
        prompt += f"{Config.USER_NAME}'s input: {user_input}"
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
        
    def run(self) -> None:
        """Main run loop"""
        print(f"Reto's Self-Improving Chatbot v{Config.VERSION}\n")
        print("------------------------------")
        print("Type /help for available commands or 'quit' to exit\n")
        
        # Show initial progress
        print(self.command_processor.process_command("progress", []))
        print("\n")
        
        while True:
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
            
            # Record this interaction
            self.progress_tracker.record_interaction(
                "conversation",
                {"user_input": user_input}
            )
                
            # Normal flow - ask Claude
            prompt = self.prepare_prompt(user_input)
            self.conversation.add_user_message(prompt)
            
            print("Thinking...")
            response = self.claude.ask(self.conversation.get_messages())
            
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

# Entry point
def main():
    # Ensure all directories exist
    Config.ensure_directories()
    
    # Initialize and run the chatbot
    chatbot = SelfImprovingChatbot()
    chatbot.run()

if __name__ == "__main__":
    main()