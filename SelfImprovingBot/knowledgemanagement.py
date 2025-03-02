import json
import os
from datetime import datetime

class KnowledgeManagementSystem:
    def __init__(self):
        self.data_file = "knowledge_base.json"
        self.knowledge = self.load_knowledge()
        # Initialize with basic categories
        categories = ["cudos_ag", "software_industry", "projects", "reto_preferences", "business_strategy"]
        for category in categories:
            if category not in self.knowledge:
                self.knowledge[category] = {}
                def load_knowledge(self):
                    if os.path.exists(self.data_file):
                        try:
                            with open(self.data_file, 'r') as f:
                                return json.load(f)
                        except:
                            return {}
                        return {}
                    def save_knowledge(self):
                        with open(self.data_file, 'w') as f:\n            json.dump(self.knowledge, f, indent=2)\n    \n    def add_information(self, category, key, value):\n        """Add or update information in a specific category"""\n        if category not in self.knowledge:\n            self.knowledge[category] = {}\n        \n        self.knowledge[category][key] = {\n            "value": value,\n            "updated_at": datetime.now().isoformat()\n        }\n        self.save_knowledge()\n        return f"Added information about \'{key}\' to category \'{category}\'"\n    \n    def get_information(self, category, key=None):\n        """Retrieve information from the knowledge base"""\n        if category not in self.knowledge:\n            return f"Category \'{category}\' not found"\n        \n        if key is not None:\n            if key not in self.knowledge[category]:\n                return f"No information found for \'{key}\' in category \'{category}\'"\n            return self.knowledge[category][key]["value"]\n        \n        return self.knowledge[category]\n    \n    def list_categories(self):\n        """List all available categories"""\n        return list(self.knowledge.keys())\n    \n    def list_keys_in_category(self, category):\n        """List all keys in a specific category"""\n        if category not in self.knowledge:\n            return f"Category \'{category}\' not found"\n        \n        return list(self.knowledge[category].keys())\n\n# Example of how to use the system\nknowledge_system = KnowledgeManagementSystem()\nprint("Knowledge management system initialized with categories:", knowledge_system.list_categories())\n