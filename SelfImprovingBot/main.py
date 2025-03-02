def prepare_prompt(self, user_input: str) -> str:
    """Prepare the prompt for Claude with current architecture, code and user input"""
    code = self.code_manager.get_current_code("main.py")
    architecture = self.code_manager.get_current_code(Config.ARCHITECTURE_FILE)
    prompt = f"# This is your current architecture:\n{architecture}\n\n"
    prompt = f"# This is your current code:\n```python\n{code}\n```\n\n"
    prompt += f"# {Config.USER_NAME}'s input: {user_input}"
    return prompt