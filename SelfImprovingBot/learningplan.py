from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

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
