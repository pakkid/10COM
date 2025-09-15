import time

quiz_qa = [
    ["What is the capital of France?", "Paris"],
    ["What is the largest planet in our solar system?", "Jupiter"],
    ["Who wrote 'Romeo and Juliet'?", "Shakespeare"]
]

for row in quiz_qa:
    print("\nQuestion: ", end="", flush=True)
    for char in row[0]:
        print(char, end="", flush=True)
        time.sleep(0.02)
    print("\nAnswer: ", end="", flush=True)
    for char in row[1]:
        print(char, end="", flush=True)
        time.sleep(0.02)
    print()