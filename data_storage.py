import json


def load_questions(filename: str):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: file {filename} not found")


def save_question(filename: str, question: dict, questions):
    questions.append(question)

    with open(filename, "w") as f:
        json.dump(questions, f, indent=4)


def update_question(filename: str, question_id: str, new_value: dict, questions):
    question_found = False
    for index, data in enumerate(questions):
        if data["question_id"] == question_id:
            questions[index].update(new_value)
            question_found = True
            break
    if question_found:
        with open(filename, "w") as f:
            json.dump(questions, f, indent = 4)
        
