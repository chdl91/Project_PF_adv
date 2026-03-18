import json
import random
import signal
import csv
import datetime
import zoneinfo

# Opening and Loading the POM.json and DIB.json files
POM_json = open("./Data/POM.json")
POM_data = json.load(POM_json)

DIB_json = open("./Data/DIB.json")
DIB_data = json.load(DIB_json)


def validate_answer(question, user_input):
    """
    Validate a user's answer for a single question dict.
    Returns:
      - True if correct,
      - False if incorrect,
      - None if no correct answer is supplied.
    Assumes answers are integer strings '1'..'4' in user_input and integer in JSON.
    """
    # This finds the key in the question data set
    correct = next((question[k] for k in (
        "correct_answer", "answer", "correct") if k in question), None)
    if correct is None:
        return None
    return str(correct).strip() == str(user_input).strip()


# This function handles the timeout for each question
def _timeout_handler(signum, frame):
    raise TimeoutError()


signal.signal(signal.SIGALRM, _timeout_handler)

# This function exports the results and score to results.csv


def export_results_to_csv(subject, score, total_questions=None, filename="results.csv"):
    header = ["result", "subject", "time", "date"]

    # timestamp in Europe/Zurich timezone configuration
    tz = zoneinfo.ZoneInfo("Europe/Zurich")
    now = datetime.datetime.now(tz)
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%Y-%m-%d")

    # prettier result formatting: "score/total (XX%)" when total provided
    if total_questions:
        try:
            pct = (int(score) / int(total_questions)) * 100
            result_text = f"{score}/{total_questions} ({pct:.0f}%)"
        except Exception:
            result_text = f"{score}/{total_questions}"
    else:
        result_text = str(score)

    # Check if file exists
    try:
        with open(filename, "r", newline="") as f:
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)          # write header once
        writer.writerow([result_text, subject, time_str, date_str])


# This bad boy runs the quiz


def run_quiz(data, per_question_timer=60):
    """Run a quiz session on the provided data. Type 'menu' to return to the main menu."""
    if not isinstance(data, list) or len(data) == 0:
        print("No questions available.")
        return

    num_questions = min(10, len(data))
    questions = random.sample(data, num_questions)
    collected_answers = []
    score = 0

    for q in questions:
        print(f"\nQuestion: {q.get('question', '<no question>')}\n")
        answers = q.get('answers', q.get('options', []))
        explanation = q.get('explanation')
       # Normalize answers into a list so we can print them line by line
        if isinstance(answers, dict):
            answers_list = list(answers.values())
        else:
            answers_list = answers

        if isinstance(answers_list, list):
            print("Answers:")
            for idx, opt in enumerate(answers_list, start=1):
                print(f"  {idx}. {opt}")
        else:
            print(f"Answers: {answers_list}")

        # For each question: wait for user input before continuing
        while True:
            try:
                signal.alarm(per_question_timer)  # Set the alarm
                answer = input(
                    f"Enter your answer (1, 2, 3, 4) or type 'menu' to return to menu [{per_question_timer}s]: "
                ).strip()
            except TimeoutError:
                print("\nTime's up! Moving to the next question.")
                collected_answers.append(None)  # Record no answer
                break  # Move to the next question on timeout
            finally:
                # Ensure alarm is always disabled after input/timeout
                try:
                    signal.alarm(0)
                except Exception:
                    pass

            if answer.lower() == 'menu':
                print("Returning to menu...")
                return

            # Validating the user's answer and giving an explanation
            if answer in ['1', '2', '3', '4']:
                collected_answers.append(answer)
                validated = validate_answer(q, answer)
                if validated is True:
                    score += 1
                    print(f"\nCorrect! Score: {score}")
                    print(f"\nExplanation: {explanation}")
                elif validated is False:
                    correct = next(
                        (q[k] for k in ("correct_answer", "answer", "correct") if k in q), None)
                    # Try to get the correct answer's text if answers_list present
                    correct_text = None
                    if correct and isinstance(answers_list, list):
                        try:
                            idx = int(correct) - 1
                            if 0 <= idx < len(answers_list):
                                correct_text = answers_list[idx]
                        except Exception:
                            correct_text = None
                    if correct_text:
                        print(
                            f"\nIncorrect. Correct answer: {correct_text} ({correct})")
                        print(f"\nExplanation: {explanation}")
                    else:
                        print(f"\nIncorrect. Correct answer: {correct}")
                        print(f"\nExplanation: {explanation}")
                else:
                    print("\nNo correct answer provided for this question; not scored.")
                    print(f"\nExplanation: {explanation}")
                break

            print("Invalid input. Please enter 1, 2, 3, 4, or 'menu'.")

    print(f"\nSession finished — score: {score}/{num_questions}")
    return score, num_questions


# This is the Main Menu Loop
def start_menu():
    while True:
        print("\nWelcome to the Quiz Application!")
        print("Please select a subject:")
        print("1. Principles of Management")
        print("2. Digital Business")
        print("3. Exit")
        input_choice = input(
            "Please select a subject by entering the corresponding number: "
        ).strip()
        if input_choice == '1':
            result = run_quiz(POM_data)
            if result is not None:
                score, total = result
            export_results_to_csv("Principles of Management", score, total)
        elif input_choice == '2':
            result = run_quiz(DIB_data)
            if result is not None:
                score, total = result
                export_results_to_csv("Digital Business", score, total)
        elif input_choice == '3':
            print("Goodbye.")
            break
        else:
            print("Bad Input. Please try again.")
        continue


# Closing the POM.json and DIB.json files
POM_json.close()
DIB_json.close()
