def main():
    filename = "aboutme.txt"
    facts = [
        "I enjoy programming in Python.",
        "I am learning file I/O operations.",
        "I like solving problems."
    ]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(facts))

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    print(content)

if __name__ == "__main__":
    main()