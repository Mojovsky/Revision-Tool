import json


class Question:

    def __init__(
        self,
        question_id,
        question_type,
        question_text,
        answer,
        question_active,
        choices=None,
    ):
        self.question_id = question_id
        self.question_type = question_type
        self.question_text = question_text
        self.answer = answer
        self.choices = choices
        self.question_active = question_active
        self.correct_answers = 0
        self.number_of_occurrences = 0
        self.answer_success_ratio = 0.0

    @property
    def question_type(self):
        return self._question_type

    @question_type.setter
    def question_type(self, value):
        if value not in ("multiple_choice", "free_form"):
            raise ValueError(
                "Invalid question type. Must be 'multiple_choice' or 'free_form'"
            )
        self._question_type = value

    @property
    def question_text(self):
        return self._question_text

    @question_text.setter
    def question_text(self, value):
        if not value:
            raise ValueError("Question text cannot be empty")
        self._question_text = value

    @property
    def answer(self):
        return self._answer

    @answer.setter
    def answer(self, value):
        if not value:
            raise ValueError("Answer text cannot be empty")
        self._answer = value

    @property
    def choices(self):
        return self._choices

    @choices.setter
    def choices(self, value):
        if not isinstance(value, list):
            raise ValueError("Choices must be a list of strings.")
        if len(value) < 4:
            raise ValueError("Choices must contain at least 4 options.")
        for choice in value:
            if not choice:
                raise ValueError("Choices cannot contain empty strings.")
        self._choices = value


def check_answer(question: Question, user_answer: str):
    question.number_of_occurrences += 1
    if user_answer == question.answer:
        question.correct_answers += 1
        return True
    else:
        return False


def success_percentage_calc(question: Question):
    percentage = (question.correct_answers / question.number_of_occurrences) * 100
    return f"{percentage:.0f}%"


def test():
    new_index = create_index("questions.json")
    new_question = {
        "question_id": new_index,
        "question_type": "multiple_choice",
        "question_text": "What is the capital of Poland",
        "answer": "Warsaw",
        "choices": ["Berlin", "Prague", "Warsaw", "Madrid"],
        "question_active": True,
        "number_of_occurences": 0,
        "correct_answers": 0,
        "answer_success_percentage": "0%",
    }

    save_question("questions.json", new_question)
