from questions import QuestionManipulation
from revision_modes import practice_mode, test_mode


def main():
    while True:
        print("Choose one of the following options by refering to its index: ")
        while True:
            manipulation = QuestionManipulation("questions.json")
            user_choice = input("\n1. Add questions\n2. View questions/stats\n3. Disable/enable questions\n4. Practice mode\n5. Test mode")
            if user_choice == "1":
                manipulation.create_new_question()
                break

            elif user_choice == "2":
                try:
                    manipulation.show_all_questions
                    break
                except ValueError as e:
                    print(f"Value Error: {e}")

            elif user_choice == "3":
                try:
                    user_input = ("Please input index number of the question: ")
                    if "#" not in user_input:
                        user_input = f"#{user_input}"
                    manipulation.update_question_status(user_input)
                    break
                except IndexError as e:
                    print(f"Index Error: {e}")


            elif user_choice == "4":
                try:
                    practice_mode()
                    break
                except ValueError as e:
                    print(f"Value Error: {e}")


            elif user_choice == "5":
                try:
                    test_mode()
                    break
                except ValueError as e:
                    print(f"Value Error: {e}")


            else:
                print("Please choose one of the available options.")
                continue
            