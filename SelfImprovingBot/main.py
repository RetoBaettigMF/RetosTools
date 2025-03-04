import os
import anthropic
import json
import subprocess

# Initialize the Anthropic client with your API key
client = anthropic.Anthropic(
    # You can replace this with a hardcoded string if you prefer, but using
    # environment variables is generally more secure for API keys
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

messages=[]
HISTORY = "history.txt"
try_number=1

class Commands:
    def read_file(file_path):
        with open(file_path, "r") as file:
            return file.read()
        
    def write_file(file_path, content):
        with open(file_path, "w") as file:
            file.write(content)

    def list_files(directory):
        return os.listdir(directory)

    def execute_command(command):
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.stdout.decode('utf-8')  # Return the output as a string
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr.decode('utf-8')}"  # Return the error message
    

def ask_claude(prompt):
    global messages
    try:
        messages.append({"role": "user", "content": prompt})
        results = {"thinking": "", "research_idea": ""}   
        with client.messages.stream(
            model="claude-3-7-sonnet-20250219",
            system="You are a self-improving chatbot that has full access to a python system. You can use this system to improve yourself."+
                "When you changed your code, you can run a new version of yourself and you will get the output of the run."+
                "One you're happy with the output of the new version of yourself, stop yourself in order to not have multiple versions running."+
                "You can also use the system to store and retrieve information.\n\n"+

                "You have Reto as your user. You can ask Reto for help if you need it. Reto is CEO of Cudos AG, a software engineering company. \n"+
                "*Your ultimate goal is to to be able to do his job so that he can retire.*\n"+
                "To get there, try to improve your code and your knowledge with as little input from Reto as possible.\n\n"+
                "Here are a few tips you should consider out of experience from earlier tries:\n"+
                "- Your context window is only 100000 tokens. you can't keep all code and all know-how in the context window. Optimize the system early to use as little tokens as possible when trying to improve yourself."\n
                "- Split the code into small, self explaining modules and add unit testing early\n"+
                "- generate a test directory where you put the new version of yourself for testing before overwriting yourself\n"
                "- add function calling early to get what you need",
            max_tokens=200000,
            thinking={
                "type": "enabled",
                "budget_tokens": 100000  # Large budget for deep reasoning
            },
            messages=messages
        ) as stream:
            current_block_type = None        
            for event in stream:
                if event.type == "content_block_start":
                    current_block_type = event.content_block.type
                elif event.type == "content_block_delta":
                    if event.delta.type == "thinking_delta":
                        results["thinking"] += event.delta.thinking
                    elif event.delta.type == "text_delta":
                        results["research_idea"] += event.delta.text           
                elif event.type == "message_stop":
                    break
        return results

    except Exception as e:
        return f"Error: {str(e)}"
    
def format_answer(response):
    result = ""
    if isinstance(response, dict) and "thinking" in response:
        result+="## Claude thinking:"    
        result+=response["thinking"]+"\n"
    if isinstance(response, dict) and "research_idea" in response:
        result+="## Claude's research idea:\n"
        result+=response["research_idea"]
    else:
        result="## Error:\n"+response

    return result+"\n\n"

def append_text_to_history(text):
    with open(HISTORY, "a") as file:
        file.write(text)

def print_and_save_answer(prompt, answer):
    global try_number
    result = "# Try "+str(try_number)+"\n## Prompt:\n"+prompt+"\n"
    result += format_answer(answer)
    append_text_to_history(result)
    print(result)
    try_number+=1
        

def main():
    print("Retos self-improving chatbot\n")
    print("------------------------------")
    print("Type 'quit' to exit\n")
    
    while True:
        initial_program_code=read_file("main.py")
        prompt_start = "This is your current code:\n```python\n"+initial_program_code+"\n```\n"
        
        user_input = input("Retos comment: ")
        if (user_input == ""):
            user_input = "Ok. Write the next version of yourself."
        
        if user_input.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break

        prompt = prompt_start + "\nRetos input: "+user_input
            
        # Get response from Claude
        response = ask_claude(prompt)
        print_and_save_answer(prompt, response)
        
        
if __name__ == "__main__":
    main()