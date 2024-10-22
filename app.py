# Install dependencies: Run this in your terminal before running the script
# pip install openai streamlit

import openai
import streamlit as st

# Set your OpenAI API key
openai.api_key = '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'

# Function to handle mathematical questions
def math_chatbot(question):
    try:
        # Call the OpenAI API to get the answer
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {"role": "user", "content": question}
            ]
        )
        # Extract the response text
        answer = response['choices'][0]['message']['content']
    except Exception as e:
        answer = f"Error: {e}"

    return answer

# Streamlit app
st.title("Math Chatbot")
st.write("Ask any mathematical question and get an answer from the OpenAI model.")

# Input box for the question
question = st.text_input("Enter your mathematical question:", "")

# Button to submit the question
if st.button("Get Answer"):
    if question.strip() != "":
        answer = math_chatbot(question)
        st.write(f"**Answer:** {answer}")
    else:
        st.write("Please enter a valid question.")
