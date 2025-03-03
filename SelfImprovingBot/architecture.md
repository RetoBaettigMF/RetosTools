# Architecture Overview

## codemanager.py

**Class: CodeManager**

- __init__(self, code_dir: str = Config.CODE_DIR)
- get_current_code(self, filename: str) -> str
- list_code_files(self) -> List[str]
- update_code(self, code: str, filename: str = "main.py") -> bool
- update_multiple_files(self, file_contents: Dict[str, str]) -> Dict[str, bool]
- extract_code_blocks(self, response: str) -> Dict[str, str]

## config.py

**Class: Config**

- system_prompt(cls) -> str
- ensure_directories(cls) -> None

## knowledgebase.py

**Class: KnowledgeBase**

- __init__(self, knowledge_dir: str = Config.KNOWLEDGE_DIR)
- store_knowledge(self, category: str, key: str, data: Any, 
                        confidence: float = 0.5, source: str = "direct") -> bool
- retrieve_knowledge(self, category: str, key: str) -> Optional[Any]
- retrieve_knowledge_item(self, category: str, key: str) -> Optional[KnowledgeItem]
- list_knowledge(self, category: str = None) -> List[str]
- search_knowledge(self, query: str) -> List[Dict[str, Any]]
- update_skill(self, skill_name: str, new_level: float) -> None
- get_skill_progress(self) -> Dict[str, Any]
- add_learning_topic(self, name: str, priority: int = 2) -> None
- complete_current_learning_topic(self) -> None
- get_learning_progress(self) -> Dict[str, Any]

## knowledgeitem.py

**Class: KnowledgeItem**

- to_dict(self) -> Dict[str, Any]

## learningplan.py

**Class: LearningPlan**

- __post_init__(self)
- get_current_topic(self) -> Optional[Dict[str, Any]]
- mark_current_complete(self) -> None
- add_topic(self, name: str, priority: int = 2) -> None
- get_progress(self) -> float
- to_dict(self) -> Dict[str, Any]
- from_dict(cls, data: Dict[str, Any]) -> 'LearningPlan'

## main.py

**Class: ConversationManager**

- __init__(self, history_file: str = Config.HISTORY_FILE)
- add_user_message(self, content: str) -> None
- add_assistant_message(self, content: str) -> None
- get_messages(self) -> List[Dict[str, str]]
- get_context_window(self, window_size: int = 10) -> List[Dict[str, str]]
- format_response(self, response: Dict[str, str]) -> str
- log_interaction(self, prompt: str, response: Dict[str, str]) -> str
- extract_code_from_response(self, response: str) -> Optional[str]

**Class: Claude**

- __init__(self, api_key: Optional[str] = None)
- ask(self, messages: List[Dict[str, str]]) -> Dict[str, str]

**Class: ProgressTracker**

- __init__(self, knowledge_base: KnowledgeBase)
- get_dashboard(self) -> Dict[str, Any]
- record_interaction(self, interaction_type: str, details: Dict[str, Any]) -> None

**Class: CommandProcessor**

- __init__(self, knowledge_base: KnowledgeBase, research_manager: ResearchManager, 
                 code_manager: CodeManager, progress_tracker: ProgressTracker)
- process_command(self, command: str, args: List[str]) -> str

**Class: SelfImprovingChatbot**

- __init__(self)
- prepare_prompt(self, user_input: str) -> str
- process_response(self, response: Dict[str, str], user_input: str) -> None
- process_command(self, user_input: str) -> Optional[str]
- save_response(self, response: Dict[str, str]) -> None
- load_response(self) -> Optional[Dict[str, str]]
- run(self) -> None

## readarchitecture.py

**Class: ReadArchitecture**

- __init__(self)
- update_architecture_description(self) -> None

## researchmanager.py

**Class: ResearchManager**

- __init__(self, knowledge_base: KnowledgeBase)
- web_search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]
- learn_about_topic(self, topic: str) -> Dict[str, Any]
- create_learning_summary(self, topic: str) -> str
- follow_learning_plan(self) -> Dict[str, Any]

## skillmodel.py

**Class: SkillModel**

- __post_init__(self)
- update_skill(self, skill_name: str, new_level: float) -> None
- assess_overall_progress(self) -> float
- get_weakest_skills(self, n: int = 3) -> List[str]
- to_dict(self) -> Dict[str, Any]
- from_dict(cls, data: Dict[str, Any]) -> 'SkillModel'

