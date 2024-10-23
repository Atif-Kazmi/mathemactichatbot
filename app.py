import gradio as gr
from transformers import AutoTokenizer, pipeline, GPTNeoForCausalLM
import sympy as sp
import re

# Load model function
def load_model():
    try:
        model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-125M")
        tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-125M")
        generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
        return generator
    except Exception as e:
        return f"Error loading model: {e}"

# Function to check if the question is mathematical
def is_mathematical_question(question):
    keywords = ["mean", "area", "volume", "solve", "what is", "calculate", "add", "subtract", "multiply", "divide", "find", "equation"]
    return any(keyword in question.lower() for keyword in keywords)

# Function to extract specific parameters from the question
def extract_parameters(question):
    # Handle equations
    if "solve" in question.lower() or "find" in question.lower() or "=" in question:
        try:
            equation = re.search(r"[-+]?\d*\.*\d+\s*\w+\s*=\s*[-+]?\d*\.*\d+", question)
            if equation:
                expr = equation.group(0).replace(" ", "")
                lhs, rhs = expr.split("=")
                # Solve the equation
                y = sp.symbols('y')
                equation = sp.Eq(sp.sympify(lhs), sp.sympify(rhs))
                solution = sp.solve(equation, y)
                return f"The value of y is: {solution[0]}"
        except Exception:
            return "Error solving the equation. Please check the format."

    # Handle specific types of mathematical questions
    if "area of a circle" in question.lower():
        match = re.search(r"radius of (\d+)", question)
        if match:
            radius = float(match.group(1))
            return sp.pi * radius**2
    elif "what is" in question.lower() or "calculate" in question.lower():
        # Attempt to evaluate as a mathematical expression
        return sp.sympify(question.split("what is")[-1].strip())

    return None

# Function to process and evaluate the question
def process_math_question(question):
    if not is_mathematical_question(question):
        return "This chatbot only answers questions related to mathematics. Please ask a mathematical question."

    # Extract and calculate based on the question
    result = extract_parameters(question)
    
    if result is not None:
        return f"The answer is: {result}"
    else:
        return "I'm sorry, I could not process that question. Please rephrase."

# Load the model once when starting the app
generator = load_model()

# Gradio Interface
def chatbot_interface(user_input):
    return process_math_question(user_input)

if __name__ == "__main__":
    # Create Gradio Interface
    iface = gr.Interface(
        fn=chatbot_interface,
        inputs=gr.Textbox(label="Enter your mathematical question:"),
        outputs="text",
        title="Math Chatbot (Open Source)",
        description="Ask any mathematical question and get an answer. Non-mathematical questions will be restricted."
    )
    iface.launch()
