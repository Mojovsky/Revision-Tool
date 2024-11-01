from questions import Question, QuestionStorage, QuestionManipulation, save_results
import random


def practice_mode():
    storage = QuestionStorage("questions.json")
    manipulation = QuestionManipulation("questions.json")

    if manipulation.check_active_questions() < 5:
        raise ValueError("Not enough questions to proceed. Please add more questions.")
    
    while True:
        question_list = storage.load_questions()
        weights = [manipulation.calculate_weight(q.get("answer_success_percentage")) for q in question_list]
        selected_question = random.choices(question_list, weights=weights)[0]
        question_obj = Question.map_values(selected_question)

        if not question_obj.question_active:
            continue

        trigger = input("Press ENTER to continue or type DONE to end the program. ")

        if trigger == "DONE".lower():
            break

        elif trigger == "":
            choices = ""
            if hasattr(question_obj, "choices"):
                choices = "   ".join(question_obj.choices)
                print(f"{question_obj._question_text}\n{choices}")
            else:
                print(question_obj._question_text)
            user_input = input()
            print("\nCorrect!\n" if Question.check_answer(question_obj, user_input) else "\nFalse\n")
            selected_question.update(question_obj.__dict__)

        storage.save_questions(question_list)

        
def test_mode(num_of_questions: int):
    storage = QuestionStorage("questions.json")
    manipulation = QuestionManipulation("questions.json")
    questions_asked = 0
    questions_correct = 0

    if manipulation.check_active_questions() < num_of_questions:
        raise ValueError("Not enough active questions to proceed. Please add more questions.")
    
    while True:
        question_list = storage.load_questions()
        selected_questions = []

        while len(selected_questions) < num_of_questions:
            selected_question = random.choice(question_list)

            if selected_question not in selected_questions:
                selected_questions.append(selected_question)

        for question in selected_questions:
            question_obj = Question.map_values(question)
            choices = ""
            if hasattr(question_obj, "choices"):
                choices = "   ".join(question_obj.choices)
                print(f"{question_obj._question_text}\n{choices}")
            else:
                print(question_obj._question_text)
            user_input = input()
            questions_asked += 1
            if Question.check_answer(question_obj, user_input):
                questions_correct += 1
                print("\nCorrect!\n")
            else:
                print("\nFalse\n")
            question.update(question_obj.__dict__)

            storage.save_questions(question_list)
        break
    result = f"Score: {questions_correct} out of {questions_asked}"
    print(result)
    save_results(result)



