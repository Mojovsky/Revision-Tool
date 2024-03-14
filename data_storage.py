import json


def load_questions(filename: str):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: file {filename} not found")


def save_question(filename: str, question: dict):
    questions = load_questions(filename)
    questions.append(question)

    with open(filename, "w") as f:
        json.dump(questions, f, indent=4)
