import json
from datetime import datetime
from user_interaction import get_question_type, get_question, line_break


class Question:
    def __init__(
        self,
        question_id,
        question_type,
        question_text,
        answer,
        question_active,
        number_of_occurrences,
        correct_answers,
        answer_success_percentage,
        choices=None,
    ):
        self.question_id = question_id
        self.question_type = question_type
        self.question_text = question_text
        self.answer = answer
        self.choices = choices

        self.question_active = question_active
        self.number_of_occurrences = number_of_occurrences
        self.correct_answers = correct_answers
        self.answer_success_percentage = answer_success_percentage

        
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
        if self.question_type == "multiple_choice":
            if len(value) < 4:
                raise ValueError("Choices must contain at least 4 options.")
            for choice in value:
                if not choice:
                    raise ValueError("Choices cannot contain empty strings.")
            self._choices = value
        else:
            pass

    def update_statistics(self, is_correct: bool):
        self.number_of_occurrences += 1
        if is_correct:
            self.correct_answers += 1
        new_percentage = QuestionManipulation.success_percentage_calc(self, self)
        self.answer_success_percentage = new_percentage

    def check_answer(self, user_answer: str):
        self.update_statistics(user_answer.lower() == str(self.answer).lower())
        return user_answer.lower() == str(self.answer).lower()

    @classmethod
    def map_values(cls, data):
        mapped_data = {
            "question_id": data.get("question_id"),
            "question_type": data.get("_question_type"),
            "question_text": data.get("_question_text"),
            "answer": data.get("_answer"),
            "choices": data.get("_choices"),
            "question_active": data.get("question_active"),
            "number_of_occurrences": data.get("number_of_occurrences"),
            "correct_answers": data.get("correct_answers"),
            "answer_success_percentage": data.get("answer_success_percentage"),
        }
        return cls(**mapped_data)



class QuestionStorage:

    def __init__(self, filename: str):
        self.filename = filename
        self.questions = self.load_questions()

    
    def load_questions(self):
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: file {self.filename} not found")

    def save_questions(self, question_list):
        with open(self.filename, "w") as f:
            json.dump(question_list, f, indent=4)

    def add_question(self, new_question: Question):
        self.questions.append(new_question.__dict__)

        with open(self.filename, "w") as f:
            json.dump(self.questions, f, indent=4)

    def _create_index(self):
        return f"#{len(self.questions) + 1}"
    


class QuestionManipulation:

    def __init__(self, filename: str):
        self.storage = QuestionStorage(filename)
        


    def create_new_question(self):
        try:
            question_id = self.storage._create_index()
            question_type = get_question_type()
            if question_type == "multiple_choice":
                question_text, answer, choices = get_question(question_type)
                choices.append(answer)
            else:
                question_text, answer = get_question(question_type)
                choices = None
            question_active=True
            number_of_occurrences=0
            correct_answers=0
            answer_success_percentage="0%"

            new_question = Question(
            question_id,
            question_type,
            question_text,
            answer,
            question_active,
            number_of_occurrences,
            correct_answers,
            answer_success_percentage,
            choices,
            )
            self.storage.add_question(new_question)
            print("Question added successfully!")
        except FileNotFoundError as e:
            print(f"Error loading or saving questions: {e}")


    def show_all_questions(self):
        l_break = line_break()
        for data in self.storage.questions:
            question_id = data["question_id"]
            question_text = data["_question_text"]
            question_active = data["question_active"]
            question_status = "Active" if question_active else "Disabled"
            number_of_occurrences = data["number_of_occurrences"]
            answer_success_percentage = data["answer_success_percentage"]

            print(f"{l_break}\nQuestion ID: {question_id}\nQuestion text: {question_text}\nQuestion status: {question_status}\nNumber of times question appeared: {number_of_occurrences}\nSuccess percentage: {answer_success_percentage}\n{l_break}")


    def success_percentage_calc(self, question: Question):
        percentage = (question.correct_answers / question.number_of_occurrences) * 100
        return f"{percentage:.0f}%"


    def update_question_status(self, question_id: str):
        for index, data in enumerate(self.storage.questions):
            if data["question_id"] == question_id:
                self.storage.questions[index]["question_active"] = not data["question_active"]
                self.storage.save_questions(self.storage.questions)
                break
        print("Question enabled/disabled successfully!")


    def check_active_questions(self):
        active = 0
        for index, data in enumerate(self.storage.questions):
            if data["question_active"] == True:
                active += 1
        return active


    def calculate_weight(self, answer_success_percentage):
        percentage_value = int(answer_success_percentage.strip("%"))
        return 1.0 / (percentage_value + 0.1)

def save_results(result):
    with open("results.txt", "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp}: {result}\n")