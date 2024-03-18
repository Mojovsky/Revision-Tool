from questions import Question, QuestionStorage, QuestionManipulation
import random


def practice_mode():
    storage = QuestionStorage("questions.json")
    question_list = storage.load_questions()
    if len(question_list) < 5:
        return "Need at least 5 questions in order to proceed. Please add more questions."
    while True:
        for q in question_list:
            question_obj = Question.map_values(q)
            if question_obj.question_active == False:
                continue
            trigger = input("Press ENTER to continue or type DONE to end the program. ")
            if trigger == "DONE".lower():
                break
            elif trigger == "":
                user_input = input(question_obj._question_text)
                if Question.check_answer(question_obj, user_input):
                    print("Correct!")
                else:
                    print("False")
                q.update(question_obj.__dict__)
            else:
                pass
        storage.save_questions(question_list)


practice_mode()