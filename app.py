import streamlit as st
from transformers import AutoTokenizer, pipeline, GPTNeoForCausalLM
import sympy as sp

# Load model function with caching and detailed logging
@st.cache_resource  # Cache the model to avoid reloading
def load_model():
    try:
        st.info("Loading the model...")
        model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-125M")
        tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-125M")
        generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
        st.success("Model loaded successfully.")
        return generator
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def is_mathematical_question(question):
    """Check if the question is related to mathematics."""
    keywords = ["mean", "area", "volume", "solve", "what is", "calculate", "add", "subtract", "multiply", "divide"]
    return any(keyword in question.lower() for keyword in keywords)

def process_math_question(question):
    """Process the mathematical question and generate an answer."""
    # Check if the question is valid
    if not is_mathematical_question(question):
        return "This chatbot only answers questions related to mathematics. Please ask a mathematical question."

    # Using SymPy to parse and evaluate simple math questions
    try:
        result = sp.sympify(question)
        return f"The answer is: {result}"
    except Exception as e:
        return f"Could not evaluate the expression. Error: {str(e)}"

# Streamlit app
def main():
    st.title("Math Chatbot (Open Source)")
    st.write("Ask any mathematical question and get an answer. Non-mathematical questions will be restricted.")

    # Load the model once
    generator = load_model()

    if generator is not None:
        user_input = st.text_input("Enter your mathematical question:")
        if st.button("Get Answer"):
            if user_input:
                answer = process_math_question(user_input)
                st.write(answer)
            else:
                st.warning("Please enter a question.")
    else:
        st.warning("The model could not be loaded. Please try again later.")

if __name__ == "__main__":
    main()
