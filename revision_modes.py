from questions import Question
from data_storage import load_questions, update_question
from data_manipulation import success_percentage_calc


def practice_mode():
    questions = load_questions()
    if len(questions) < 5:
        print("Need at least 5 questions in order to proceed. Please add more questions.")
    while True:
        ...