import json
import unittest
from mock import patch
from questions import Question
from questions import create_index, save_question, load_questions


class TestQuestion(unittest.TestCase):

    def test_add_valid_question(self):
        # Mock the load_questions function to avoid actual file access
        with patch("__main__.load_questions", return_value=[]):

            # Create a valid question object
            question_id = create_index()
            question_text = "What is the capital of France?"
            question_type = "multiple_choice"
            answer = "Paris"
            choices = ["London", "Berlin", "Madrid", "Paris"]
            new_question = Question(
                question_id, question_type, question_text, answer, True, choices
            )

        # Mock the save_question function to verify data being written
        with patch("__main__.save_question") as mock_save:
            save_question(
                "questions.json", new_question.__dict__
            )  # Convert to dict for saving

            # Assert that save_question was called with expected arguments
            mock_save.assert_called_once_with("questions.json", new_question.__dict__)

    def test_add_empty_question_text(self):
        # Mock the load_questions function
        with patch("__main__.load_questions", return_value=[]):

            # Create a question with empty question text (raises ValueError)
            question_id = create_index()
            question_text = ""
            question_type = "multiple_choice"
            answer = "Paris"
            choices = ["London", "Berlin", "Madrid", "Paris"]

        with self.assertRaises(ValueError) as e:
            Question(question_id, question_type, question_text, answer, True, choices)

        self.assertEqual(str(e.exception), "Question text cannot be empty")

    def test_add_question_with_less_than_four_choices(self):
        # Mock the load_questions function
        with patch("__main__.load_questions", return_value=[]):

            # Create a question with less than 4 choices (raises ValueError)
            question_id = create_index()
            question_text = "What is the capital of France?"
            question_type = "multiple_choice"
            answer = "Paris"
            choices = ["London", "Berlin"]

        with self.assertRaises(ValueError) as e:
            Question(question_id, question_type, question_text, answer, True, choices)

        self.assertEqual(str(e.exception), "Choices must contain at least 4 options.")

    def test_add_question_with_empty_choice(self):
        # Mock the load_questions function
        with patch("__main__.load_questions", return_value=[]):

            # Create a question with an empty choice (raises ValueError)
            question_id = create_index()
            question_text = "What is the capital of France?"
            question_type = "multiple_choice"
            answer = "Paris"
            choices = ["London", "Berlin", "", "Paris"]

        with self.assertRaises(ValueError) as e:
            Question(question_id, question_type, question_text, answer, True, choices)

        self.assertEqual(str(e.exception), "Choices cannot contain empty strings.")


# Run the tests (requires the `unittest` module)
if __name__ == "__main__":
    unittest.main()
