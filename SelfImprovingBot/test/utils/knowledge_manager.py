# utils/knowledge_manager.py
import os
import json
import re
from datetime import datetime
from collections import defaultdict

class KnowledgeManager:
    """Manages knowledge collection, organization, and retrieval."""
    
    def __init__(self):
        self.knowledge_dir = "knowledge"
        self.index_file = os.path.join(self.knowledge_dir, "index.json")
        self.ensure_knowledge_dir()
        self.load_index()
        
    def ensure_knowledge_dir(self):
        """Ensure knowledge directory exists."""
        if not os.path.exists(self.knowledge_dir):
            os.makedirs(self.knowledge_dir)
        
    def load_index(self):
        """Load the knowledge index or create it if it doesn't exist."""
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, 'r') as f:
                    self.index = json.load(f)
            except:
                self.index = {"items": [], "categories": {}, "keywords": {}}
        else:
            self.index = {"items": [], "categories": {}, "keywords": {}}
    
    def save_index(self):
        """Save the knowledge index."""
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)
    
    def extract_knowledge(self, text):
        """Extract knowledge items from text."""
        # Look for patterns like "KNOWLEDGE: Title | Category | Content"
        knowledge_pattern = r"KNOWLEDGE:\s*([^|]+)\|([^|]+)\|(.*?)(?=KNOWLEDGE:|$)"
        matches = re.findall(knowledge_pattern, text, re.DOTALL)
        
        # Also look for CEO-specific information
        ceo_pattern = r"CEO INFO:\s*([^|]+)\|([^|]+)\|(.*?)(?=CEO INFO:|$)"
        ceo_matches = re.findall(ceo_pattern, text, re.DOTALL)
        
        # Combine both types
        all_matches = matches + ceo_matches
        
        if not all_matches:
            return []
            
        knowledge_items = []
        for title, category, content in all_matches:
            item = self.add_knowledge_item(
                title.strip(), 
                category.strip(), 
                content.strip()
            )
            knowledge_items.append(item)
            
        return knowledge_items
    
    def add_knowledge_item(self, title, category, content):
        """Add a knowledge item to the database."""
        # Generate a unique ID
        item_id = f"k{len(self.index['items']) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Extract keywords
        keywords = self._extract_keywords(title + " " + content)
        
        # Create the item
        item = {
            "id": item_id,
            "title": title,
            "category": category,
            "content": content,
            "keywords": keywords,
            "created": datetime.now().isoformat(),
            "last_accessed": None,
            "access_count": 0
        }
        
        # Add to index
        self.index["items"].append(item)
        
        # Update category index
        if category not in self.index["categories"]:
            self.index["categories"][category] = []
        self.index["categories"][category].append(item_id)
        
        # Update keyword index
        for keyword in keywords:
            if keyword not in self.index["keywords"]:
                self.index["keywords"][keyword] = []
            self.index["keywords"][keyword].append(item_id)
        
        # Save the item to a file
        with open(os.path.join(self.knowledge_dir, f"{item_id}.json"), 'w') as f:
            json.dump(item, f, indent=2)
        
        # Save the updated index
        self.save_index()
        
        return item
    
    def _extract_keywords(self, text):
        """Extract keywords from text."""
        # Simple implementation - extract words longer than 4 chars
        words = re.findall(r'\b\w{4,}\b', text.lower())
        
        # Remove duplicates and common words
        common_words = {'this', 'that', 'with', 'from', 'have', 'will', 'they', 'their', 'about'}
        keywords = set(words) - common_words
        return list(keywords)
    
    def search(self, query):
        """Search the knowledge base."""
        query = query.lower()
        query_words = query.split()
        
        # Get items that match the query words
        matching_ids = set()
        
        # Check against keywords
        for word in query_words:
            for keyword, ids in self.index["keywords"].items():
                if word in keyword:
                    matching_ids.update(ids)
        
        # Check title and content
        for item in self.index["items"]:
            item_text = (item["title"] + " " + item["content"]).lower()
            if any(word in item_text for word in query_words):
                matching_ids.add(item["id"])
        
        # Get the full items and calculate relevance
        results = []
        for item_id in matching_ids:
            item = self._get_item_by_id(item_id)
            if item:
                # Calculate a simple relevance score
                relevance = sum(1 for word in query_words 
                              if word in (item["title"] + " " + item["content"]).lower())
                results.append({
                    "id": item["id"],
                    "title": item["title"],
                    "category": item["category"],
                    "summary": item["content"][:100] + "...",
                    "relevance": relevance
                })
        
        # Sort by relevance
        results.sort(key=lambda x: x["relevance"], reverse=True)
        return results
    
    def _get_item_by_id(self, item_id):
        """Get a knowledge item by its ID."""
        for item in self.index["items"]:
            if item["id"] == item_id:
                return item
        return None
    
    def get_item_by_id(self, item_id):
        """Get a knowledge item by its ID and update access stats."""
        item = self._get_item_by_id(item_id)
        if item:
            # Update access stats
            item["last_accessed"] = datetime.now().isoformat()
            item["access_count"] += 1
            
            # Save the updated item
            with open(os.path.join(self.knowledge_dir, f"{item_id}.json"), 'w') as f:
                json.dump(item, f, indent=2)
                
            # Update in index
            for i, idx_item in enumerate(self.index["items"]):
                if idx_item["id"] == item_id:
                    self.index["items"][i] = item
                    break
            
            self.save_index()
        
        return item
    
    def get_relevant_knowledge(self, query, limit=3):
        """Get relevant knowledge for a query to include in the context."""
        results = self.search(query)
        
        if not results:
            return None
            
        # Format the top results
        formatted = []
        for i, result in enumerate(results[:limit]):
            item = self.get_item_by_id(result["id"])
            if item:
                formatted.append(f"--- Knowledge Item {i+1} ---\n"
                                f"Title: {item['title']}\n"
                                f"Category: {item['category']}\n"
                                f"Content: {item['content']}\n")
        
        return "\n".join(formatted)