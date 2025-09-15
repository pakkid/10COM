questions = ["What is 2 + 2?", "What is the capital of France?"]
answers = ["4", "Paris"]

score = 0

for i in range(len(questions)):
    print(questions[i])
    user_answer = input("Your answer: ")
    if user_answer.strip().lower() == answers[i].lower():
        print("Correct!")
        score += 1
    else:
        print("Wrong!")

print(f"You got {score} out of {len(questions)} correct.")