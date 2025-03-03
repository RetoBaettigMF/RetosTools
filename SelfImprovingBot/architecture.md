# Architecture Overview

## Overall Architecture

The code implements a self-improving chatbot system designed to learn and eventually replace a CEO. It follows a modular architecture with specialized components for knowledge management, conversation handling, code self-modification, and AI interactions via Claude API.

### Core Components

1. **Configuration** - Central settings management
2. **Knowledge Management** - Stores and retrieves information
3. **Learning System** - Tracks skills and learning progress
4. **Conversation Management** - Handles user interactions
5. **Code Management** - Self-modifies the codebase
6. **AI Interface** - Integrates with Claude API
7. **Progress Tracking** - Monitors improvement towards goal
8. **Command Processing** - Handles user commands

### Data Flow

```
User Input → Command Processor or Claude → Knowledge Base ↔ Research Manager
                                        ↓
                                  Code Manager → Self-Improvement
```


## config.py

**Classes:**
- import
- class

**Functions:**
- system_prompt
- ensure_directories

## knowledgebase.py

**Classes:**
- KnowledgeBase

**Functions:**
- store_knowledge
- retrieve_knowledge
- retrieve_knowledge_item
- list_knowledge
- search_knowledge
- update_skill
- get_skill_progress
- add_learning_topic
- complete_current_learning_topic
- get_learning_progress

## knowledgeitem.py

**Classes:**
- class

**Functions:**
- to_dict

## learningplan.py

**Classes:**
- class

**Functions:**
- get_current_topic
- mark_current_complete
- add_topic
- get_progress
- to_dict
- from_dict

## codemanager.py

**Classes:**
- CodeManager
- and

**Functions:**
- get_current_code
- list_code_files
- update_code
- update_multiple_files
- extract_code_blocks
- test_code
- run_new_version

## main.py

**Functions:**
- prepare_prompt

## researchmanager.py

**Classes:**
- ResearchManager

**Functions:**
- web_search
- learn_about_topic
- create_learning_summary
- follow_learning_plan

## skillmodel.py

**Classes:**
- class

**Functions:**
- update_skill
- assess_overall_progress
- get_weakest_skills
- to_dict
- from_dict

