import json
import os


class Question:

    def __init__(self, question_id, question_text, question_type, question_active):
        self.question_id = question_id
        self.question_type = question_type
        self.question_text = question_text
        self.question_active = question_active
        self.number_of_occurrences = 0
        self.answer_success_ratio = 0.0


class MultipleChoice(Question):

    def __init__(
        self,
        question_id,
        question_type,
        question_text,
        question_active,
        correct_answer,
        answer_choices,
    ):
        super().__init__(question_id, question_type, question_text, question_active)
        self.correct_answer = correct_answer
        self.answer_choices = answer_choices

    def get_answer_options(self):
        return self.answer_choices

    def check_answer(self, user_answer):
        if user_answer == self.correct_answer:
            # Implement logic for logging occurences and success ratio
            return True
        else:
            return False


class FreeForm(Question):

    def __init__(
        self, question_id, question_type, question_text, question_active, correct_answer
    ):
        super().__init__(
            question_id, question_type, question_text, question_active, correct_answer
        )
        self.correct_answer = correct_answer

    def check_answer(self, user_answer):
        if user_answer == self.correct_answer:
            # Implement logic for logging occurences and success ratio
            return True
        else:
            return False


def load_questions():
    try:
        with open("questions.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("Error: file question.json not found")


def save_question(question):

    filename = "questions.json"
    try:
        os.path.exists(filename)
        with open(filename, "r") as f:
            questions = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("Error: file question.json not found")

    questions.append(question)

    with open(filename, "w") as f:
        json.dump(questions, f, indent=4)


def create_index():
    questions = load_questions()
    if questions == []:
        return "#1"
    else:
        for question in questions:
            question_id = question["question_id"].strip("#")
            highest_id = int(question_id)

        new_index = f"#{highest_id + 1}"
        return new_index


print(create_index())
