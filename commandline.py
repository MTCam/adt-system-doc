import argparse
import requests
import json

OLLAMA_URL = 'https://secret-ollama.ncsa.ai'
OLLAMA_API_URL = f'{OLLAMA_URL}/api'
OLLAMA_CHAT_URL = f'{OLLAMA_API_URL}/chat'
#OLLAMA_CHAT_URL = 'https://uiuc.chat/api/chat-api/chat'
OLLAMA_MODEL = 'llama3.1:70b'

def start_conversation(character):
    return [{'role': 'system', 'content': character}]

def query(conversation, prompt):
    conversation.append({'role': 'user', 'content': prompt})
    print(f"{conversation=}, posting request")
    response = requests.post(
        OLLAMA_CHAT_URL,
        json={
            'model': OLLAMA_MODEL,
            'messages': conversation,
            'stream': True
        },
        stream=True
    )
    print(f"Request posted: {response=}")
    reply = ""

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            # Parse the JSON response
            try:
                message = json.loads(decoded_line)
                if 'message' in message and 'content' in message['message']:
                    # Append the content to the reply
                    reply += message['message']['content']
            except json.JSONDecodeError:
                print('Could not decode:', decoded_line)
    
    conversation.append({'role': 'assistant', 'content': reply})
    return reply

def main():
    parser = argparse.ArgumentParser(
        description='Chat with Ollama about your Python codebase.')
    parser.add_argument('--query', type=str,
                        help='Your question or prompt for Ollama')
    parser.add_argument('--role', type=str, help='AI Character Name')
    parser.add_argument('--char', type=str, help='AI Character')

    # Parse arguments
    args = parser.parse_args()
    prompt = args.query or None
    role = args.role or 'assistant'
    character = args.char or 'You are a helpful assistant.'
    print(f"{role=}, {character=}, {prompt=}")
    conversation = start_conversation(character)

    if prompt:
        response = query(conversation, prompt)
        print(f'{role}>> {response}\n')

    while True:
        # Get user input
        prompt = input('>> ')
        # Check if the user wants to quit
        if prompt.lower() == 'quit':
            break
        response = query(conversation, prompt)
        print(f'\n{role}>> {response}\n')

if __name__ == '__main__':
    main()
