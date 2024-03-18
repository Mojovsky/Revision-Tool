from questions import Question, QuestionStorage, QuestionManipulation
import random


def practice_mode():
    storage = QuestionStorage("questions.json")
    manipulation = QuestionManipulation("questions.json")
    if manipulation.check_active_questions() < 5:
        print("Not enough questions to proceed. Please add more questions.")
        return
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
            user_input = input(question_obj._question_text)
            print("Correct!" if Question.check_answer(question_obj, user_input) else "False")
            selected_question.update(question_obj.__dict__)
        storage.save_questions(question_list)

        


practice_mode()