from questions import Question
from data_storage import load_questions, save_question
from user_interaction import get_question_type, get_question, line_break


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
    question_id = create_index(filename)
    question_type = get_question_type()
    if question_type == "multiple_choice":
        question_text, answer, choices = get_question(question_type)
        choices.append(answer)
    else:
        question_text, answer = get_question(question_type)

    try:
        new_question = Question(
            question_id,
            question_type,
            question_text,
            answer,
            choices if question_type == "multiple_choice" else None,
        )
        questions = load_questions(filename)
        new_question = new_question.__dict__
        questions = new_question
        save_question(filename, questions)
        print("Question added successfully!")
    except FileNotFoundError as e:
        print(f"Error loading or saving questions: {e}")


def show_questions():
    l_break = line_break()
    question_list = load_questions("questions.json")
    for data in question_list:
        question_id = data["question_id"]
        question_text = data["question_text"]
        question_active = data["question_active"]
        question_status = "Active" if question_active else "Disabled"
        number_of_occurrences = data["number_of_occurrences"]
        answer_success_percentage = data["answer_success_percentage"]

        print(f"{l_break}\nQuestion ID: {question_id}\nQuestion text: {question_text}\nQuestion stauts: {question_status}\nNumber of times question appeared: {number_of_occurrences}\nSuccess percentage: {answer_success_percentage}\n{l_break}")


show_questions()