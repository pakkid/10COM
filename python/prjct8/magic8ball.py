import random
import os

answers = [
    "Yes, definitely.",
    "No, certainly not.",
    "Ask again later.",
    "Cannot predict now.",
    "It is certain.",
    "Very doubtful.",
    "Most likely.",
    "Don't count on it.",
    "Outlook good.",
    "My reply is no."
]

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def magic_8_ball():
    clear()
    print("Welcome to Magic 8 Ball")
    while True:
        question = input("\n\nAsk a Yes/No question (or Ctrl+C to quit)... ")
        clear()
        print("Magic 8 Ball says:", random.choice(answers))

if __name__ == "__main__":
    try:
        magic_8_ball()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")