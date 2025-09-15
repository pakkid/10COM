import os
import sys
import re
import json
import base64
import hashlib
import random
from pathlib import Path

QUIZ_FILE = Path(__file__).with_suffix(".quiz")
TXT_FILE = Path(__file__).with_suffix(".txt")

SECRET_PASSPHRASE = "change-this-key-123!@#"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def _key_bytes() -> bytes:
    return hashlib.sha256(SECRET_PASSPHRASE.encode("utf-8")).digest()

def _xor(data: bytes, key: bytes) -> bytes:
    klen = len(key)
    return bytes(b ^ key[i % klen] for i, b in enumerate(data))

def encrypt_str(text: str) -> str:
    raw = text.encode("utf-8")
    xored = _xor(raw, _key_bytes())
    return base64.urlsafe_b64encode(xored).decode("ascii")

def decrypt_str(token: str) -> str:
    data = base64.urlsafe_b64decode(token.encode("ascii"))
    plain = _xor(data, _key_bytes())
    return plain.decode("utf-8")

def write_quiz(records, path: Path):
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for rec in records:
            enc = {
                "q": encrypt_str(rec["q"]),
                "c": [encrypt_str(c) for c in rec["c"]],
                # store correct answer as 1..4 to match user input
                "a": encrypt_str(str(rec["a"]))
            }
            f.write(json.dumps(enc, ensure_ascii=False) + "\n")

def load_quiz(path: Path):
    items = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            q = decrypt_str(obj["q"])
            c = [decrypt_str(x) for x in obj["c"]]
            a = int(decrypt_str(obj["a"]))
            items.append({"q": q, "c": c, "a": a})
    return items

def generate_sample_quiz(path: Path):
    sample = [
        {
            "q": "What is the capital of France?",
            "c": ["Berlin", "Madrid", "Paris", "Rome"],
            "a": 3
        },
        {
            "q": "Which language runs in a web browser?",
            "c": ["C", "Java", "Python", "JavaScript"],
            "a": 4
        },
        {
            "q": "What is 2 + 2?",
            "c": ["3", "4", "5", "6"],
            "a": 2
        }
    ]
    write_quiz(sample, path)

def ask_int(prompt: str, min_v: int, max_v: int) -> int:
    while True:
        s = input(prompt).strip()
        if s.isdigit():
            v = int(s)
            if min_v <= v <= max_v:
                return v
        print(f"Please enter a number between {min_v} and {max_v}.")

def run_quiz():
    if not QUIZ_FILE.exists():
        print(f"No quiz file found. Creating sample at {QUIZ_FILE}")
        generate_sample_quiz(QUIZ_FILE)

    questions = load_quiz(QUIZ_FILE)
    if not questions:
        print("Quiz file is empty.")
        return

    random.shuffle(questions)
    score = 0
    total = len(questions)

    for idx, item in enumerate(questions, start=1):
        print(f"\nQ{idx}. {item['q']}")
        for i, choice in enumerate(item["c"], start=1):
            print(f"  {i}) {choice}")
        ans = ask_int("Your answer (1-4): ", 1, 4)
        if ans == item["a"]:
            print("Correct!")
            score += 1
        else:
            correct_text = item["c"][item["a"] - 1]
            print(f"Wrong. Correct answer: {item['a']}) {correct_text}")

    print(f"\nScore: {score}/{total}")

def _strip_choice_prefix(s: str) -> str:
    # Remove common prefixes like "1) ", "A. ", "- ", etc.
    return re.sub(r'^\s*(?:-|\d+[\).\s]|[A-Da-d][\).\s])\s*', '', s).strip()

def parse_quiz_txt(path: Path):
    """
    Expected format per question block (blocks separated by a blank line):
      Question text
      1) Choice 1
      2) Choice 2
      3) Choice 3
      4) Choice 4
      A: 2        (can be 'A:', 'Ans:', 'Answer:' or just '2')

    Choice prefixes are optional. Answer can be number or exact choice text.
    """
    text = path.read_text(encoding="utf-8")
    blocks = [b for b in re.split(r'\n\s*\n', text) if b.strip()]
    records = []
    for b in blocks:
        lines = [ln.strip() for ln in b.splitlines() if ln.strip()]
        if len(lines) < 6:
            raise ValueError("Each block must have question, 4 choices, and an answer line.")
        q = lines[0]
        choices = [_strip_choice_prefix(lines[i]) for i in range(1, 5)]
        ans_line = lines[5]

        m = re.search(r'(\d+)', ans_line)
        if m:
            a = int(m.group(1))
        else:
            s = re.sub(r'^\s*(?:A|Ans|Answer)\s*[:=\-]\s*', '', ans_line, flags=re.I).strip()
            try:
                a = next(i + 1 for i, c in enumerate(choices) if c.strip().lower() == s.lower())
            except StopIteration:
                raise ValueError(f"Cannot determine answer for question: {q}")

        if not (1 <= a <= 4):
            raise ValueError(f"Answer out of range (1-4) for question: {q}")
        records.append({"q": q, "c": choices, "a": a})
    return records

def ask_append_or_replace() -> str:
    while True:
        s = input("Append to existing quiz.quiz or replace it? [A/R]: ").strip().lower()
        if s in ("a", "append"):
            return "append"
        if s in ("r", "replace"):
            return "replace"
        print("Please enter A (append) or R (replace).")

def convert_txt_to_quiz():
    if not TXT_FILE.exists():
        print(f"No {TXT_FILE.name} found.")
        return

    try:
        new_records = parse_quiz_txt(TXT_FILE)
    except Exception as e:
        print(f"Failed to parse {TXT_FILE.name}: {e}")
        return

    if QUIZ_FILE.exists():
        mode = ask_append_or_replace()
        if mode == "append":
            try:
                existing = load_quiz(QUIZ_FILE)
            except Exception:
                existing = []
            combined = existing + new_records
        else:
            combined = new_records
    else:
        combined = new_records

    write_quiz(combined, QUIZ_FILE)

    try:
        TXT_FILE.unlink()
        print(f"Converted {len(new_records)} questions to {QUIZ_FILE.name} and deleted {TXT_FILE.name}.")
    except Exception as e:
        print(f"Converted {len(new_records)} questions to {QUIZ_FILE.name}. Could not delete {TXT_FILE.name}: {e}")

def generate_quiz_txt_template():
    if TXT_FILE.exists():
        print(f"{TXT_FILE.name} already exists at {TXT_FILE}. Not overwriting.")
        return

    template = (
        "Question 1: Replace with your question\n"
        "1) Choice 1\n"
        "2) Choice 2\n"
        "3) Choice 3\n"
        "4) Choice 4\n"
        "Answer: 1\n"
        "\n"
        "Question 2: Replace with another question\n"
        "A) Choice A\n"
        "B) Choice B\n"
        "C) Choice C\n"
        "D) Choice D\n"
        "Ans: 2\n"
    )
    with TXT_FILE.open("w", encoding="utf-8", newline="\n") as f:
        f.write(template)
    print(f"Wrote quiz template to {TXT_FILE}")

def goodbye():
    print(r"""
 $$$$$$\                            $$\ $$\                           $$\ 
$$  __$$\                           $$ |$$ |                          $$ |
$$ /  \__| $$$$$$\   $$$$$$\   $$$$$$$ |$$$$$$$\  $$\   $$\  $$$$$$\  $$ |
$$ |$$$$\ $$  __$$\ $$  __$$\ $$  __$$ |$$  __$$\ $$ |  $$ |$$  __$$\ $$ |
$$ |\_$$ |$$ /  $$ |$$ /  $$ |$$ /  $$ |$$ |  $$ |$$ |  $$ |$$$$$$$$ |\__|
$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$   ____|    
\$$$$$$  |\$$$$$$  |\$$$$$$  |\$$$$$$$ |$$$$$$$  |\$$$$$$$ |\$$$$$$$\ $$\ 
 \______/  \______/  \______/  \_______|\_______/  \____$$ | \_______|\__|
                                                  $$\   $$ |              
                                                  \$$$$$$  |              
                                                   \______/               """)


if __name__ == "__main__":
    try:
        clear()
        if "-t" in sys.argv:
            generate_quiz_txt_template()
        elif "-c" in sys.argv:
            convert_txt_to_quiz()
        else:
            run_quiz()
    except KeyboardInterrupt:
        clear()
        goodbye()