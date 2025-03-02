from typing import Any, Dict, List, Optional
import json 
import os
import time
import logging
from knowledgeitem import KnowledgeItem
from config import Config
from skillmodel import SkillModel
from learningplan import LearningPlan

logger = logging.getLogger("self-improving-chatbot")

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
            with open(file_path, "w", encoding='utf-8') as f:
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
