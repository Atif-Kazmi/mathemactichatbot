import streamlit as st
from transformers import pipeline, GPTNeoForCausalLM, AutoTokenizer
import math
import re

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
        "calculate", "solve", "area", "perimeter", "volume", "equation",
        "add", "subtract", "multiply", "divide", "integral", "derivative", 
        "geometry", "algebra", "calculus", "mean", "median", "mode", 
        "standard deviation", "variance", "probability", "function", 
        "trigonometry", "what is the value of", "solve for", "find",
        "radius", "diameter", "circle", "square", "triangle", "rectangle"
    ]
    return any(keyword in question.lower() for keyword in math_keywords)

# Function to evaluate simple arithmetic expressions
def evaluate_expression(expression):
    try:
        # Evaluate the mathematical expression safely
        return eval(expression)
    except Exception:
        return "I couldn't evaluate that expression."

# Function to handle mathematical questions
def math_chatbot(question):
    # Check if the question is related to mathematics
    if not is_math_question(question):
        return "This chatbot only answers questions related to mathematics. Please ask a mathematical question."

    # Handle specific mathematical problems
    if "area of a circle" in question.lower():
        try:
            radius = float(question.split("radius of ")[1].split()[0])
            area = math.pi * (radius ** 2)
            return f"The area of a circle with a radius of {radius} units is {area:.2f} square units."
        except (ValueError, IndexError):
            return "Could not understand the radius. Please specify the radius clearly."
    
    # Handle basic arithmetic operations
    # Check if the question is a simple math expression
    if re.match(r'^\s*\d+\s*[\+\-\*/]\s*\d+\s*$', question):  # Regex to match simple expressions like "25 + 75"
        return f"The answer is {evaluate_expression(question)}."

    # If it's not a specific case, use the model to generate an answer
    prompt = f"Answer the following math question: {question}"
    result = generator(prompt, max_length=100, num_return_sequences=1)
    answer = result[0]['generated_text']
    
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
