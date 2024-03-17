import json
from user_interaction import get_question_type, get_question, line_break


class Question:
    def __init__(self, question_id, question_type, question_text, answer, choices=None):
        self.question_id = question_id
        self.question_type = question_type
        self.question_text = question_text
        self.answer = answer
        self.choices = choices  # Optional for multiple-choice questions

        # Initialize statistics within the class
        self.answer_success_percentage = "0%"
        self.question_active = True
        self.number_of_occurrences = 0
        self.correct_answers = 0

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


    def check_answer(self, user_answer: str):
        self.number_of_occurrences += 1
        if user_answer.lower() == str(self.answer).lower():
            self.correct_answers += 1
            return True
        else:
            return False


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



    def add_question(self, new_question: Question):
        self.questions.append(new_question.__dict__)

        with open(self.filename, "w") as f:
            json.dump(self.questions, f, indent=4)

    def _create_index(self):
        return f"#{len(self.questions) + 1}"
    
    def update_question(self, question_id: str, new_value: dict):
        question_found = False
        for index, data in enumerate(self.questions):
            if data["question_id"] == question_id:
                self.questions[index].update(new_value)
                question_found = True
                break
        if question_found:
            with open(self.filename, "w") as f:
                json.dump(self.questions, f, indent = 4)



class QuestionManipulation:

    def __init__(self, filename: str):
        self.storage = QuestionStorage(filename)
    

    def create_question(self):
        try:
            question_id = self.storage._create_index()
            question_type = get_question_type()
            if question_type == "multiple_choice":
                question_text, answer, choices = get_question(question_type)
                choices.append(answer)
            else:
                question_text, answer = get_question(question_type)
                choices = None

            new_question = Question(question_id, question_type, question_text, answer, choices)
            self.storage.add_question(new_question)
            print("Question added successfully!")
        except FileNotFoundError as e:
            print(f"Error loading or saving questions: {e}")


    def change_question_status(self, question_id: str):
        for index, data in enumerate(self.storage.questions):
            if data["question_id"] == question_id:
                self.storage.questions[index]["question_active"] = not data["question_active"]
                new_status = data["question_active"]
        self.storage.update_question(question_id, {"question_active": new_status})
        print("Question enabled/disabled successfully!")


    def show_questions(self):
        l_break = line_break()
        for question in self.storage.questions:
            question_status = "Active" if question.question_active else "Disabled"

            print(f"{l_break}\nQuestion ID: {question.question_id}\nQuestion text: {question.question_text}\nQuestion stauts: {question_status}\nNumber of times question appeared: {question.number_of_occurrences}\nSuccess percentage: {question.answer_success_percentage}\n{l_break}")

    




def main():
    question_manipulation = QuestionManipulation("questions.json")
    question_storage = QuestionStorage("questions.json")
    questions = question_manipulation.storage.questions
    #question_manipulation.create_question()
    #question_storage.update_question("#2", {"question_active": True})
    #question_manipulation.change_question_status("#2")
    question_manipulation.show_questions()


if __name__ == "__main__":
    main()