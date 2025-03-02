# Architecture Documentation - Self-Improving Chatbot
(this file is "architecture.md")

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

## Class Descriptions

### `Config` in config.py
Configuration dataclass for system settings.
- `system_prompt()`: Returns the system prompt for Claude
- `ensure_directories()`: Creates necessary directories

### `KnowledgeItem` in knowledgeitem.py
Data structure for stored knowledge.
- `to_dict()`: Converts item to dictionary

### `SkillModel` in skillmodel.py
Tracks CEO skills and competencies.
- `update_skill()`: Updates a skill level
- `assess_overall_progress()`: Calculates overall skill progress
- `get_weakest_skills()`: Returns skills needing improvement

### `LearningPlan` in learningplan.py
Manages the chatbot's learning curriculum.
- `get_current_topic()`: Returns current learning topic
- `mark_current_complete()`: Completes current topic
- `add_topic()`: Adds new learning topic
- `get_progress()`: Returns learning progress percentage

### `KnowledgeBase` in knowledgebase.py
Core knowledge management system.
- `store_knowledge()`: Stores information
- `retrieve_knowledge()`: Retrieves stored information
- `list_knowledge()`: Lists available knowledge items
- `search_knowledge()`: Searches for knowledge
- `update_skill()`: Updates skill levels
- `get_skill_progress()`: Returns skill progress summary
- `get_learning_progress()`: Returns learning plan progress

### `ResearchManager` in researchmanager.py
Handles research and learning activities.
- `web_search()`: Simulates web search (placeholder)
- `learn_about_topic()`: Researches a specific topic
- `follow_learning_plan()`: Advances through learning plan

### `ConversationManager`
Manages chat interactions and history.
- `add_user_message()`: Adds user message to history
- `add_assistant_message()`: Adds assistant message to history
- `get_messages()`: Returns all conversation messages
- `log_interaction()`: Logs interactions to history file
- `extract_code_from_response()`: Extracts code from responses

### `CodeManager` in codemanager.py
Handles code modification and execution. If no filename is provided, it uses "main.py" as filename.
- `get_current_code([filename])`: Gets current code content
- `backup_current_code([filename])`: Creates code backup
- `update_code([filename])`: Updates code with new version
- `test_code([filename])`: Tests if code is valid Python
- `run_new_version()`: Runs updated code version of main.py

### `Claude`
Interface to the Claude API.
- `ask()`: Sends request to Claude and processes response

### `ProgressTracker`
Tracks progress toward CEO capabilities.
- `get_dashboard()`: Returns progress dashboard
- `record_interaction()`: Records user interactions

### `CommandProcessor`
Processes user commands.
- `process_command()`: Routes and handles commands
- Various command handlers: `/help`, `/knowledge`, `/learn`, etc.

### `SelfImprovingChatbot`
Main application class.
- `prepare_prompt()`: Prepares prompts for Claude
- `process_response()`: Handles Claude's responses
- `process_command()`: Processes user commands
- `run()`: Main execution loop

The system aims to learn and improve itself with minimal user input, gradually building CEO capabilities through self-directed learning and code modifications.