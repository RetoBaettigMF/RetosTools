import os
import anthropic

# Initialize the Anthropic client with your API key
client = anthropic.Anthropic(
    # You can replace this with a hardcoded string if you prefer, but using
    # environment variables is generally more secure for API keys
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

def ask_claude(prompt):
    """
    Send a prompt to Claude 3.7 Sonnet and get a response.
    
    Args:
        prompt (str): The text prompt to send to Claude
        
    Returns:
        str: Claude's response
    """
    try:
        # Create a message using Claude 3.7 Sonnet
        message = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=1000,
            temperature=0.7,
            system="You are a helpful AI assistant that provides concise responses.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract and return the response
        return message.content[0].text
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("Simple Claude 3.7 Sonnet Demo")
    print("----------------------------")
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break
            
        # Get response from Claude
        response = ask_claude(user_input)
        print("\nClaude:", response, "\n")

if __name__ == "__main__":
    main()