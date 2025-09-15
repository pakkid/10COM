import requests
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sys
import time
import threading

debug = 0  # Suppress debug output for clean CLI

questions = [
    ("What is the Sky Tower in Auckland primarily used for?", "observation and entertainment", "It's mainly for viewing the city and entertainment."),
    ("Which body of water surrounds Auckland?", "harbour", "Think of a large body of water where boats dock around the city."),
    ("What is the largest park in Auckland?", "auckland domain", "It's a famous park in the central city."),
    ("Which Auckland island is famous for its volcanic cones?", "rangitoto", "The island is volcanic and very iconic."),
    ("What is Auckland's nickname due to its many harbours and islands?", "city of sails", "Think about yachts and boating."),
    ("Which museum in Auckland showcases New Zealand history and art?", "auckland war memorial museum", "It's near the park and honors war history."),
    ("What annual event celebrates the arts and performances in Auckland?", "auckland arts festival", "A festival that celebrates music, theater, and arts."),
]

certificate_html = ""  # Will store the generated certificate HTML


def take_quiz():
    global certificate_html
    name = input("\nEnter your name: ")

    # Collect answers
    user_answers = []
    hinted_questions = [False] * len(questions)
    for i, (q, _, hint) in enumerate(questions, 1):
        user_ans = input(f"Q{i}: {q} (type 'hint' for a hint) ").strip()
        if user_ans.lower() == "hint":
            print(f"Hint: {hint}")
            hinted_questions[i-1] = True
            user_ans = input(f"Now answer Q{i}: ").strip()
        user_answers.append(user_ans)

    # Build model prompt
    prompt_lines = ["You are a helpful assistant that evaluates short quiz answers."]
    for i, (user_ans, (q, correct_ans, _)) in enumerate(zip(user_answers, questions), 1):
        prompt_lines.append(
            f"Q{i}: Question: '{q}' | User Answer: '{user_ans}' | Correct Answer: '{correct_ans}' | Respond with 'correct' or 'incorrect'."
        )
    prompt_lines.append("Return ONLY a JSON array like [\"correct\", \"incorrect\", ...] in order. No extra text.")
    prompt = "\n".join(prompt_lines)

    # Loader
    stop_loader = False

    def loader():
        while not stop_loader:
            for c in "|/-\\":
                sys.stdout.write(f"\rChecking answers... {c}")
                sys.stdout.flush()
                time.sleep(0.1)

    loader_thread = threading.Thread(target=loader)
    loader_thread.start()

    # Query model
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={'model': 'gemma3:4b', 'prompt': prompt, 'max_tokens': 300, 'stop': None, 'stream': False}
        )
        result_json = response.json()
        if debug:
            print("\n[DEBUG] Full JSON Response:", result_json)

        model_reply = result_json.get('response') or result_json.get('completion', '')
        model_reply = model_reply.strip()
        results = json.loads(model_reply)
        results = [r.lower().startswith("correct") for r in results[:len(questions)]]

    except Exception as e:
        stop_loader = True
        loader_thread.join()
        print("\nRequest failed or JSON parsing failed:", e)
        results = [False] * len(questions)

    # Stop loader
    stop_loader = True
    loader_thread.join()
    print("\rChecking answers... Done!    ")

    # Calculate score
    score = 0
    for i, correct in enumerate(results):
        if correct:
            score += 0.5 if hinted_questions[i] else 1
    percent = int((score / len(questions)) * 100)
    if percent == 100:
        title = "Auckland Expert"
    elif percent >= 70:
        title = "Auckland Enthusiast"
    elif percent >= 40:
        title = "Ackland Visitor"
    else:
        title = "Auckland Beginner"

    # Build HTML results
    question_results_html = ""
    for i, (user_ans, (q, correct_ans, _), correct, hinted) in enumerate(zip(user_answers, questions, results, hinted_questions), 1):
        if correct:
            status = "Correct"
            if hinted:
                status += " (Hint used, half points)"
        else:
            status = f"Incorrect (Answer: {correct_ans})"
        question_results_html += f"<p><b>Q{i}: {q}</b><br>Your Answer: {user_ans}<br>{status}</p>"

    # Certificate HTML
    certificate_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Quiz Certificate</title>
        <style>
            body {{ font-family: Arial; background: #f9f9f9; text-align: center; }}
            .cert {{ background: #fff; margin: 50px auto; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px #ccc; width: 600px; text-align: left; }}
            h1 {{ color: #2a5d84; text-align:center; }}
            .score {{ font-size: 1.5em; margin: 20px 0; text-align:center; }}
            .name {{ font-size: 1.2em; color: #444; text-align:center; }}
            p {{ margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="cert">
            <h1>{title} Certificate</h1>
            <div class="name">Awarded to: <b>{name}</b></div>
            <div class="score">{score} out of {len(questions)} correct</div>
            <div class="score">Percentage: {percent}%</div>
            <hr>
            <h2>Detailed Results:</h2>
            {question_results_html}
            <p>Congratulations on completing the Auckland Quiz!</p>
        </div>
    </body>
    </html>
    """

    # Serve HTML once, then shutdown
    class CertHandler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            return  # Suppress default logging

        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(certificate_html.encode())
            # Shutdown server after sending page
            threading.Thread(target=self.server.shutdown).start()

    server_address = ('', 8000)
    httpd = HTTPServer(server_address, CertHandler)
    print("Opening certificate in browser...")
    webbrowser.open("http://localhost:8000")
    httpd.serve_forever()


# --- Main Menu Loop ---
choice = ""
while choice.lower() != "exit":
    print("\n--- Auckland Quiz Menu ---")
    print("1. Take the quiz")
    print("2. Instructions")
    print("Type 'exit' to quit")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        take_quiz()
        # Ending menu after quiz
        while True:
            print("\nQuiz finished! What would you like to do next?")
            print("1. Play again")
            print("2. View certificate")
            print("3. Exit")
            end_choice = input("Choose an option: ").strip()
            if end_choice == "1":
                break  # Restart main menu loop
            elif end_choice == "2":
                # Reopen the last certificate
                webbrowser.open("http://localhost:8000")
            elif end_choice == "3":
                choice = "exit"
                break
            else:
                print("Invalid choice. Please select 1, 2, or 3.")
    elif choice == "2":
        print("\nInstructions:")
        print(" - You will be asked 7 questions about Auckland.")
        print(" - You can type 'hint' to get a hint, but it will give you half points for that question.")
        print(" - Your answers will be checked automatically and a certificate with detailed results will open in your browser.")
    elif choice.lower() == "exit":
        print("Goodbye!")
    else:
        print("Invalid choice. Please select 1, 2, or type 'exit'.")
