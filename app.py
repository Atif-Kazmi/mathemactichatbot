import streamlit as st
from transformers import pipeline, GPTNeoForCausalLM, AutoTokenizer

# Load the smaller GPT-Neo model from Hugging Face
@st.cache_resource  # Cache the model to avoid reloading
def load_model():
    model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-125M")  # Smaller model for faster loading
    tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-125M")
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
    return generator

# Load the model only once at the start
generator = load_model()

# Function to check if the question is related to mathematics
def is_math_question(question):
    math_keywords = [
        "calculate", "solve", "equation", "add", "subtract", "multiply",
        "divide", "integral", "derivative", "geometry", "algebra", 
        "calculus", "math", "mean", "median", "mode", "standard deviation",
        "variance", "probability", "function", "trigonometry", 
        "what is the value of", "solve for", "find"
    ]
    return any(keyword in question.lower() for keyword in math_keywords)

# Function to handle mathematical questions
def math_chatbot(question):
    if not is_math_question(question):
        return "This chatbot only answers questions related to mathematics. Please ask a mathematical question."
    
    try:
        # Generate the answer using the smaller model with reduced max_length
        result = generator(question, max_length=50, num_return_sequences=1)
        answer = result[0]['generated_text']
    except Exception as e:
        answer = f"Error: {e}"
    
    return answer

# Streamlit app interface
st.title("Math Chatbot (Open Source)")
st.write("Ask any mathematical question and get an answer. Non-mathematical questions will be restricted.")

# Input box for the question
question = st.text_input("Enter your mathematical question:", "")

# Button to submit the question
if st.button("Get Answer"):
    if question.strip() != "":
        answer = math_chatbot(question)
        st.write(f"**Answer:** {answer}")
    else:
        st.write("Please enter a valid question.")
