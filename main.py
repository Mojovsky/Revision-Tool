from questions import QuestionManipulation
import sys
from revision_modes import practice_mode, test_mode


def main():
    while True:
        try:
            display_menu()
            user_selected_option = input("Enter your choice: ")
            handle_user_choice(user_selected_option)
        except(ValueError, IndexError, FileNotFoundError) as e:
            print(f"Error: {e}")
            input("Press ENTER to continue.")
        except KeyboardInterrupt:
            print("\nExiting program.")
            break
            

def display_menu():
    print("\nChoose one of the following options by referencing its index: \n")
    print("1. Add questions")
    print("2. View questions/stats")
    print("3. Disable/enable questions")
    print("4. Practice mode")
    print("5. Test mode")
    print("Type 'DONE' to exit.")

def handle_user_choice(user_choice):
    manipulation = QuestionManipulation("questions.json")
    if user_choice == "1":
        manipulation.create_new_question()
        print("Question added successfully!")

    elif user_choice == "2":
        manipulation.show_all_questions()
        input("Here's a list of all the questions. Press ENTER to continue.")

    elif user_choice == "3":
        user_input = input("Please input index number of the question: ")
        if "#" not in user_input:
            user_input = f"#{user_input}"
        manipulation.update_question_status(user_input)
        input("Question enabled/disabled successfully! Press ENTER to continue.")
    
    elif user_choice == "4":
        practice_mode()

    elif user_choice == "5":
        user_input = int(input("Select the number of questions for the test: \n"))
        test_mode(user_input)
        input("Press ENTER to continue.")

    elif user_choice.lower() == "done":
        print("Exiting program.")
        sys.exit()
    else:
        print("Invalid choice. Please select one of the available options.")


if __name__ == "__main__":
    main()