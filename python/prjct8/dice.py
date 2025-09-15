import random
import time
import os

DICE_ART = {
    1: (
        "┌─────────┐",
        "│         │",
        "│    ●    │",
        "│         │",
        "└─────────┘"
    ),
    2: (
        "┌─────────┐",
        "│  ●      │",
        "│         │",
        "│      ●  │",
        "└─────────┘"
    ),
    3: (
        "┌─────────┐",
        "│  ●      │",
        "│    ●    │",
        "│      ●  │",
        "└─────────┘"
    ),
    4: (
        "┌─────────┐",
        "│  ●   ●  │",
        "│         │",
        "│  ●   ●  │",
        "└─────────┘"
    ),
    5: (
        "┌─────────┐",
        "│  ●   ●  │",
        "│    ●    │",
        "│  ●   ●  │",
        "└─────────┘"
    ),
    6: (
        "┌─────────┐",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "└─────────┘"
    ),
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_dice(num):
    for line in DICE_ART[num]:
        print(line)

def roll_animation():
    for _ in range(10):
        num = random.randint(1, 6)
        clear()
        print("Rolling the dice...")
        print_dice(num)
        time.sleep(0.08)
    return random.randint(1, 6)

def main():
    while True:
        input("Press Enter to roll the dice (or Ctrl+C to quit)...")
        result = roll_animation()
        clear()
        print("You rolled:")
        print_dice(result)
        print(f"Result: {result}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")