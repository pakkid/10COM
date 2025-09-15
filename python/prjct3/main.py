import requests
import json

# Collect all user information first
name = input("What is your name? ")
food = input("What is your favorite food? ")
age = input("How old are you? ")
hobbies = input("What are your hobbies? ")

print("Generating your welcome card...")

# Create a more comprehensive prompt for the AI
prompt = f"""Generate ONLY a welcome card for {name}.
Requirements:
- Welcome {name} specifically to Python programming
- Mention they are {age} years old
- Include their love for {food}
- Reference their hobbies: {hobbies}
- Keep it under 100 words
- Use natural, friendly language
- Format with appropriate line breaks
- NO salutations like 'Dear' or 'Regards'
- NO signature or closing phrases
- NO meta-commentary about the writing
- ONLY the welcome card text itself
"""

def create_text_box(text, width=60):
    """Create a nice CLI box around text with proper line breaks."""
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + (1 if current_length > 0 else 0) <= width - 4:
            if current_length > 0:
                current_line.append(' ')
                current_length += 1
            current_line.append(word)
            current_length += len(word)
        else:
            lines.append(''.join(current_line))
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        lines.append(''.join(current_line))
    
    top_bottom = '╔' + '═' * (width - 2) + '╗'
    empty_line = '║' + ' ' * (width - 2) + '║'
    
    box = [top_bottom, empty_line]
    
    for line in lines:
        padding = (width - 2 - len(line)) // 2
        right_padding = width - 2 - len(line) - padding
        box_line = '║' + ' ' * padding + line + ' ' * right_padding + '║'
        box.append(box_line)
    
    box.extend([empty_line, '╚' + '═' * (width - 2) + '╝'])
    
    return '\n'.join(box)

try:
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': 'gemma3:4b',
            'prompt': prompt,
            'max_tokens': 150,
            'stream': False
        }
    )
    
    response_json = response.json()
    card = response_json.get('response', '')
    
    formatted_card = create_text_box(card)
    
    print("\n")
    print(formatted_card)
    print("\n")
    
except Exception as e:
    print(f"Error: {e}")
    print("Make sure the Ollama server is running with the gemma3 model loaded.")