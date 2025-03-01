import os
import anthropic

# Initialize the Anthropic client with your API key
client = anthropic.Anthropic(
    # You can replace this with a hardcoded string if you prefer, but using
    # environment variables is generally more secure for API keys
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()
    
def write_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)

def list_files(directory):
    return os.listdir(directory)

def ask_claude(prompt):
    try:
        message = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=25000,
            thinking={
                "type": "enabled",
                "budget_tokens": 16000  
            },
            temperature=0.7,
            system="You are a self-improving chatbot that has full access to a python system. You can use this system to improve yourself."+
            "When you changed your code, you can run a new version of yourself and you will get the output of the run."+
            "One you're happy with the output of the new version of yourself, stop yourself in order to not have multiple versions running."+
            "You can also use the system to store and retrieve information.\n\n"+

            "You have Reto as your user. You can ask Reto for help if you need it. Reto is CEO of Cudos AG, a software engineering company. \n"+
            "*Your ultimate goal is to to be able to do his job so that he can retire.*",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract and return the response
        return message.content[0].text
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("Retos self-improving chatbot\n")
    print("------------------------------")
    print("Type 'quit' to exit\n")
    
    while True:
        initial_program_code=read_file("main.py")
        prompt_start = "This is your current code:\n\n"+initial_program_code+"\n\nWhat do you want to do?"
        
        user_input = input("Retos comment: ")
        
        if user_input.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break

        prompt = prompt_start + "\nRetos comment: "+user_input
            
        # Get response from Claude
        response = ask_claude(user_input)
        print("\nClaude:", response, "\n")

if __name__ == "__main__":
    main()