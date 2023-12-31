from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai

# Load environment variables and configure Google API
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load OpenAI model and get responses
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input_text])
    return response.text

# Function to handle sending messages
def send_message(message):
    if message:
        # Append user message to chat history
        st.session_state.chat_history.append(("You", message))
        # Get Gemini's response
        try:
            response = get_gemini_response(message)
            st.session_state.chat_history.append(("Chatbot", response))
        except Exception as e:
            st.session_state.chat_history.append(("Chatbot", f"Error: {str(e)}"))
        # Rerun the app to update the chat display
        st.experimental_rerun()

# Initialize Streamlit app
st.set_page_config(page_title="Gideon's Chat Application")
st.sidebar.header("Instructions")
st.sidebar.write("Interact with the model by typing in your message!...Please Note that This Chatbot cannot keep memory of previous chats")

st.header("Gideon's Chat Application")

# Initialize or get the chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Chat UI
st.write("## Chat")
chat_container = st.container()
for author, message in st.session_state.chat_history:
    if author == "You":
        chat_container.markdown(f"<span style='color: blue;'>{author}:</span> {message}", unsafe_allow_html=True)
    else:  # "Chatbot"
        chat_container.markdown(f"<span style='color: green;'>{author}:</span> {message}", unsafe_allow_html=True)


# Chat input form
with st.form("chat_form", clear_on_submit=True):
    input_message = st.text_input("Your message:", key="input")
    submit_button = st.form_submit_button(label='Send')

# Handling form submission
if submit_button and input_message:
    send_message(input_message)

st.write("----")
st.header("Feedback")

# Feedback form
with st.form("feedback_form", clear_on_submit=True):
    feedback = st.text_area("Your feedback", key="feedback_text")
    submitted_feedback = st.form_submit_button(label="Submit Feedback")

# Path to the feedback file
feedback_file_path = "feedback.txt"

if submitted_feedback and feedback:
    # Append the feedback to a text file in the current directory
    with open(feedback_file_path, "a") as file:
        file.write(f"Feedback: {feedback}\n")
    st.write("Thank you for your feedback!")

st.write("Privacy Notice: Your data is handled with confidentiality.")
