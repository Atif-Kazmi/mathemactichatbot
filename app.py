import streamlit as st

# Try importing openai and handle potential import errors
try:
    import openai
except ModuleNotFoundError:
    st.error("The OpenAI library is not installed. Please ensure it is listed in requirements.txt and reinstall.")
    st.stop()  # Stop further execution if openai is not installed

# Set your OpenAI API key (ensure it's secure in a production environment)
openai.api_key = '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'

# Function to handle mathematical questions using the new API
def math_chatbot(question):
    try:
        # Create the prompt for the question
        prompt = f"Answer the following mathematical question: {question}"

        # Call the OpenAI API using ChatCompletion for newer versions
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use text-davinci-002 for more complex completions
            messages=[
                {"role": "system", "content": "You are an expert mathematician."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=50,
            n=1
        )

        # Extract the response text
        answer = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        answer = f"Error: {e}"
    
    return answer

# Streamlit app interface
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
