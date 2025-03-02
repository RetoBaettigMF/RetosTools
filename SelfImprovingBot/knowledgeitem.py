# Knowledge Representation
from dataclasses import asdict, dataclass, field
import time
from typing import Any, Dict

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
