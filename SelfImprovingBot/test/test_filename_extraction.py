import sys
import os
import json

# Add the parent directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.code_manager import CodeManager

def test_all_filename_extraction_methods():
    """Test all the different ways filenames can be extracted from code blocks."""
    
    # Create a mock response with various code block formats
    mock_response = {
        "response": """
Here are examples of all the different ways filenames can be provided in code blocks:

1. Python-style comment with just the filename:

```python
# utils/simple_comment.py
def simple_function():
    return "Simple function"
```

2. Python-style comment with "filename:" prefix:

```python
# filename: utils/explicit_filename.py
def explicit_function():
    return "Explicit filename"
```

3. JavaScript-style comment with "filename:" prefix:

```javascript
// filename: utils/javascript_file.js
function jsFunction() {
    return "JavaScript function";
}
```

4. Filename directly in the code block:

```python utils/inline_filename.py
def inline_function():
    return "Inline filename"
```

5. Format on the second line:

```python
import os
# filename: utils/second_line.py
def second_line_function():
    return os.path.join('path', 'to', 'file')
```

6. Other language variations:

```ruby
# filename: utils/ruby_file.rb
def ruby_method
  puts "Ruby method"
end
```

```c
// filename: utils/c_file.c
int main() {
    printf("Hello from C");
    return 0;
}
```

7. Edge case - no filename:

```python
def no_filename_function():
    pass
```
"""
    }
    
    # Create a CodeManager instance
    code_manager = CodeManager()
    
    # Extract code from the mock response
    code_files = code_manager.extract_code_from_response(mock_response)
    
    # Print the results
    print("Extracted files:")
    for filename, code in code_files.items():
        print(f"\n--- {filename} ---")
        print(code[:100] + "..." if len(code) > 100 else code)
    
    # Verify that all expected filenames were extracted
    expected_filenames = [
        "utils/simple_comment.py",
        "utils/explicit_filename.py",
        "utils/javascript_file.js",
        "utils/inline_filename.py",
        "utils/second_line.py",
        "utils/ruby_file.rb",
        "utils/c_file.c",
        "generated_file_without_name.py"  # For the block without a filename
    ]
    
    missing_files = [f for f in expected_filenames if f not in code_files]
    unexpected_files = [f for f in code_files if f not in expected_filenames]
    
    if missing_files:
        print(f"\nERROR: Missing expected files: {missing_files}")
    
    if unexpected_files:
        print(f"\nERROR: Found unexpected files: {unexpected_files}")
    
    if not missing_files and not unexpected_files:
        print("\nSUCCESS: All expected files were correctly extracted!")

def test_single_code_block():
    """Test the case of a single code block without a filename."""
    
    mock_response = {
        "response": """
Here's a single code block without a filename:

```python
def main():
    print("Hello, world!")
    
if __name__ == "__main__":
    main()
```
"""
    }
    
    code_manager = CodeManager()
    code_files = code_manager.extract_code_from_response(mock_response)
    
    print("\nSingle Code Block Test:")
    for filename, code in code_files.items():
        print(f"\n--- {filename} ---")
        print(code[:100] + "..." if len(code) > 100 else code)
    
    if "main.py" in code_files:
        print("\nSUCCESS: Single code block without filename was correctly assigned to main.py!")
    else:
        print("\nERROR: Failed to assign main.py to single code block without filename")

def test_original_extraction():
    """Test the original example from the task."""
    
    mock_response = {
        "response": """
Here's the code:

```python
# filename: utils/claude_api.py
import requests

def call_claude_api(prompt, api_key):
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "content-type": "application/json"
    }
    data = {
        "prompt": prompt,
        "model": "claude-2.0",
        "max_tokens_to_sample": 1000
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
```
"""
    }
    
    code_manager = CodeManager()
    code_files = code_manager.extract_code_from_response(mock_response)
    
    print("\nOriginal Task Test:")
    for filename, code in code_files.items():
        print(f"\n--- {filename} ---")
        print(code[:100] + "..." if len(code) > 100 else code)
    
    if "utils/claude_api.py" in code_files:
        print("\nSUCCESS: Original task filename was correctly extracted!")
    else:
        print("\nERROR: Failed to extract filename from the original task example")

if __name__ == "__main__":
    test_all_filename_extraction_methods()
    test_single_code_block()
    test_original_extraction()
