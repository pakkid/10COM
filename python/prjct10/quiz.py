multiple_choice_quiz = [
    ["What is 2+2?", ["2", "3", "4", "5"], "4"],
    ["Capital of NZ?", ["Auckland", "Wellington", "Christchurch"], "Wellington"],
    ["Which planet is closest to the Sun?", ["Earth", "Venus", "Mercury", "Mars"], "Mercury"]
]

score = 0

for q, question in enumerate(multiple_choice_quiz):
    print(f"Question {q+1}: {question[0]}")
    print("Choices:")
    for i, choice in enumerate(question[1]):
        print(f"  {i+1}. {choice}")
    answer = input("Your answer (enter the number): ")
    try:
        selected = int(answer) - 1
        if question[1][selected] == question[2]:
            print("Correct!\n")
            score += 1
        else:
            print(f"Incorrect. The correct answer is: {question[2]}\n")
    except (ValueError, IndexError):
        print(f"Invalid input. The correct answer is: {question[2]}\n")

print(f"Quiz finished! Your score: {score}/{len(multiple_choice_quiz)}")