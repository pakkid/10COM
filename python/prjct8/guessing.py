import random

def guessing_game():
    number = random.randint(1, 10)
    print("I'm thinking of a number between 1 and 10.")
    while True:
        try:
            guess = int(input("Take a guess: "))
            if guess == number:
                print("Correct! You guessed the number.")
                break
            else:
                print("Wrong guess. Try again.")
        except ValueError:
            print("Please enter a valid integer.")

if __name__ == "__main__":
    guessing_game()