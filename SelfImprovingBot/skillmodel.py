from dataclasses import dataclass, field
from typing import Any, Dict, List

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
