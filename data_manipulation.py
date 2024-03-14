from questions import Question
from data_storage import load_questions, save_question
from user_interaction import get_question_type, get_question


def create_index(filename):
    questions = load_questions(filename)
    if questions == []:
        return "#1"
    else:
        for question in questions:
            question_id = question["question_id"].strip("#")
            highest_id = int(question_id)

        new_index = f"#{highest_id + 1}"
        return new_index


def add_question():
    filename = "questions.json"
    try:
        question_id = create_index(filename)
        question_type = get_question_type()
        if question_type == "multiple_choice":
            question_text, answer, choices = get_question(question_type)
            new_question = Question(
                question_id, question_type, question_text, answer, choices
            )
        else:
            question_text, answer = get_question(question_type)
            new_question = Question(question_id, question_type, question_text, answer)
    except ValueError as e:
        print(f"Error: {e}")
    try:
        questions = load_questions(filename)
        questions.append(new_question.__dict__)
        save_question(filename, questions)
        print("Question added successfully!")
    except FileNotFoundError as e:
        print(f"Error loading or saving questions: {e}")


add_question()
