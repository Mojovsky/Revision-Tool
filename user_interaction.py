def get_question_type(
    prompt: str = "Choose one of the following options by refering to its index\n1. Multiple choice question\n2. Free form question\n",
):
    while True:
        user_choice = input(prompt).strip()
        if user_choice in ("1", "2"):
            if user_choice == "1":
                return "multiple_choice"
            return "free_form"
        else:
            raise ValueError("Please choose one of the two options (1 or 2)")


def get_question(question_type):
    question_text = input("Please enter the question: ").strip()
    if not question_text:
        raise ValueError("Question cannot be empty")
    answer = input("Please enter the correct answer: ").strip()
    if not answer:
        raise ValueError("Answer cannot be empty")
    if question_type == "multiple_choice":
        choices = []
        for i in range(3):
            while True:
                choice = input(f"Please enter invalid choice nr. {i+1}: ")
                if choice:
                    choices.append(choice)
                    break
                else:
                    raise ValueError("Invalid choice cannot be empty")

        return question_text, answer, choices
    return question_text, answer


def line_break():
    return "---------------------------------------------"