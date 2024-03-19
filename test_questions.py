import unittest
import json
from unittest.mock import patch, mock_open
from questions import Question, QuestionStorage, QuestionManipulation

class TestQuestion(unittest.TestCase):
    def setUp(self):
        self.question = Question(
            "1",
            "multiple_choice",
            "What is the capital of France?",
            "Paris",
            True,
            0,
            0,
            "0%",
            ["Paris", "London", "Berlin", "Madrid"]
        )

    def test_question_type_setter(self):
        with self.assertRaises(ValueError):
            self.question.question_type = "invalid_type"

    def test_question_text_setter(self):
        with self.assertRaises(ValueError):
            self.question.question_text = ""

    def test_answer_setter(self):
        with self.assertRaises(ValueError):
            self.question.answer = ""

    def test_choices_setter(self):
        with self.assertRaises(ValueError):
            self.question.choices = ["Paris", "London", ""]

        with self.assertRaises(ValueError):
            self.question.choices = ["Paris", "London"]

    def test_update_statistics(self):
        self.question.update_statistics(True)
        self.assertEqual(self.question.number_of_occurrences, 1)
        self.assertEqual(self.question.correct_answers, 1)
        self.assertEqual(self.question.answer_success_percentage, "100%")

    def test_check_answer(self):
        self.assertTrue(self.question.check_answer("Paris"))
        self.assertFalse(self.question.check_answer("London"))

    def test_map_values(self):
        data = {
            "question_id": "1",
            "_question_type": "multiple_choice",
            "_question_text": "What is the capital of France?",
            "_answer": "Paris",
            "_choices": ["Paris", "London", "Berlin", "Madrid"],
            "question_active": True,
            "number_of_occurrences": 0,
            "correct_answers": 0,
            "answer_success_percentage": "0%"
        }
        mapped_question = Question.map_values(data)
        self.assertEqual(mapped_question.question_id, "1")
        self.assertEqual(mapped_question.question_type, "multiple_choice")
        self.assertEqual(mapped_question.question_text, "What is the capital of France?")
        self.assertEqual(mapped_question.answer, "Paris")
        self.assertEqual(mapped_question.choices, ["Paris", "London", "Berlin", "Madrid"])
        self.assertEqual(mapped_question.question_active, True)
        self.assertEqual(mapped_question.number_of_occurrences, 0)
        self.assertEqual(mapped_question.correct_answers, 0)
        self.assertEqual(mapped_question.answer_success_percentage, "0%")

class TestQuestionStorage(unittest.TestCase):
    def setUp(self):
        self.filename = "test_questions.json"
        self.questions = [
            {
                "question_id": "1",
                "_question_type": "multiple_choice",
                "_question_text": "What is the capital of France?",
                "_answer": "Paris",
                "_choices": ["Paris", "London", "Berlin", "Madrid"],
                "question_active": True,
                "number_of_occurrences": 0,
                "correct_answers": 0,
                "answer_success_percentage": "0%"
            }
        ]

    def test_load_questions(self):
        with patch('builtins.open', new_callable=mock_open, read_data=json.dumps(self.questions)):
            storage = QuestionStorage(self.filename)
            self.assertEqual(storage.questions, self.questions)


    def test_add_question(self):
        with patch('builtins.open', new_callable=mock_open, read_data=json.dumps(self.questions)):
            storage = QuestionStorage(self.filename)
            question = Question(
                "2",
                "multiple_choice",
                "What is the largest planet in our solar system?",
                "Jupiter",
                True,
                0,
                0,
                "0%",
                ["Jupiter", "Saturn", "Mars", "Earth"]
            )
            storage.add_question(question)
            self.assertEqual(len(storage.questions), 2)
            self.assertEqual(storage.questions[1]["question_id"], "2")

class TestQuestionManipulation(unittest.TestCase):
    def setUp(self):
        self.filename = "test_questions.json"
        self.questions = [
            {
                "question_id": "1",
                "_question_type": "multiple_choice",
                "_question_text": "What is the capital of France?",
                "_answer": "Paris",
                "_choices": ["Paris", "London", "Berlin", "Madrid"],
                "question_active": True,
                "number_of_occurrences": 10,
                "correct_answers": 8,
                "answer_success_percentage": "80%"
            }
        ]
        with patch('builtins.open', new_callable=mock_open, read_data=json.dumps(self.questions)):
            self.manipulation = QuestionManipulation(self.filename)


    def test_success_percentage_calc(self):
        question = Question(
            "1",
            "multiple_choice",
            "What is the capital of France?",
            "Paris",
            True,
            10,
            8,
            "0%",
            ["Paris", "London", "Berlin", "Madrid"]
        )
        percentage = self.manipulation.success_percentage_calc(question)
        self.assertEqual(percentage, "80%")


    def test_check_active_questions(self):
        with patch('builtins.open', new_callable=mock_open, read_data=json.dumps([
            {
                "question_id": "1",
                "question_active": True
            },
            {
                "question_id": "2",
                "question_active": False
            }
        ])):
            active_count = self.manipulation.check_active_questions()
            self.assertEqual(active_count, 1)

    def test_calculate_weight(self):
        weight = self.manipulation.calculate_weight("80%")
        self.assertAlmostEqual(weight, 1.0 / 80.1)



if __name__ == '__main__':
    unittest.main()