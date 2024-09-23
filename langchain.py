import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Load API key from environment variables
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

## Title of the app
st.title("Gemini Chatbot")

## Sidebar for settings
st.sidebar.title("Configuration Settings")

# Input API key
api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")
if api_key:
    os.environ["GEMINI_API_KEY"] = api_key
    genai.configure(api_key=api_key)

# Select Gemini model
engine = st.sidebar.selectbox("Select Gemini model", ["gemini-1.5-pro", "gemini-1.5-flash"])

# Additional settings
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

## Main interface for user input
st.write("Ask a question to the Gemini chatbot:")
user_input = st.text_input("You:")

## Function to generate response using Gemini
def generate_response(question, model_name, temperature, max_tokens):
    generation_config = {
        "temperature": temperature,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": max_tokens,
        "response_mime_type": "text/plain",
    }
    
    # Create a GenerativeModel instance
    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config
    )
    
    # Start a new chat session and send a message
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(question)
    
    return response.text

## Process the input and generate a response
if user_input and api_key:
    response = generate_response(user_input, engine, temperature, max_tokens)
    st.write(response)

elif user_input:
    st.warning("Please enter the Gemini API Key in the sidebar")
else:
    st.write("Please provide a question")
