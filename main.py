import streamlit as st
import random
import time
from fractions import Fraction
import pandas as pd

def generate_question():
    question_type = random.choice(["integer", "decimal"])

    if question_type == "integer":
        num1 = random.randint(1, 99)
        num2 = random.randint(1, 99)
        operation = random.choice(['+', '-', '*'])
        question = f"{num1} {operation} {num2}"
        correct_answer = eval(question)

    elif question_type == "decimal":
        num1 = round(random.uniform(0.1, 100.0), 2)
        num2 = round(random.uniform(0.1, 100.0), 2)
        operation = random.choice(['+', '-'])
        question = f"{num1} {operation} {num2}"
        correct_answer = eval(question)

    

    return question, correct_answer, question_type

def main():
    st.title("Mental Math For Traders")

    # Initialize session state

    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()
    if 'question_start_time' not in st.session_state:
        st.session_state.question_start_time = st.session_state.start_time
    if 'correct_count' not in st.session_state:
        st.session_state.correct_count = 0
    if 'correct_answers_by_type' not in st.session_state:
        st.session_state.correct_answers_by_type = {'integer': 0, 'decimal': 0}
    if 'answer_times' not in st.session_state:
        st.session_state.answer_times = []
    if 'question' not in st.session_state:
        st.session_state.question, st.session_state.correct_answer, st.session_state.question_type = generate_question()
    if 'last_answer' not in st.session_state:
        st.session_state.last_answer = None
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0
    if 'new_question' not in st.session_state:
        st.session_state.new_question = False

        

    # Time limit (in seconds)
    time_limit = 120

    elapsed_time = time.time() - st.session_state.start_time

    # Display the question and timer
    st.write(f"Time remaining: {max(0, int(time_limit - elapsed_time))} seconds")
    st.write("Solve the following math question:")
    st.write(st.session_state.question)

    # Check if time limit has been reached
    if elapsed_time > time_limit:
        st.write(f"Time's up! You answered {st.session_state.correct_count} questions correctly.")
        # Display results in a chart
        df = pd.DataFrame(list(st.session_state.correct_answers_by_type.items()), columns=['Question Type', 'Correct Answers'])
        st.bar_chart(df.set_index('Question Type'))
        if st.session_state.answer_times:
            st.line_chart(st.session_state.answer_times)
        st.stop()

    # Input for the answer
    user_answer = st.text_input("Your answer", value="", key=f"answer_input_{st.session_state.input_key}")

    # Check if the answer is correct
    if user_answer:
        try:
            user_answer_float = float(user_answer)
            if user_answer_float == st.session_state.correct_answer:
                st.success("Correct!")
                st.session_state.correct_count += 1
                st.session_state.correct_answers_by_type[st.session_state.question_type] += 1
                st.session_state.new_question = True
                time_taken = time.time() - st.session_state.question_start_time
                st.session_state.answer_times.append(time_taken)
            elif user_answer_float != st.session_state.last_answer:
                st.error(f"Incorrect. Try again!")
            st.session_state.last_answer = user_answer_float
        except ValueError:
            st.error("Please enter a valid number.")

    # Generate a new question if correct
    if st.session_state.new_question:
        st.session_state.question, st.session_state.correct_answer, st.session_state.question_type = generate_question()
        st.session_state.input_key += 1  # Increment the input key
        st.session_state.question_start_time = time.time()
        st.session_state.new_question = False
        
        st.experimental_rerun()

if __name__ == "__main__":
    main()
