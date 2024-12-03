# import requests
# import streamlit as st

# streamlit run streamlit_todo_gui.py

import os
import subprocess
import time

import requests
import streamlit as st
from dotenv import load_dotenv

# from openai import OpenAI
from src.ChatGPT import ChatGPT
from src.GeminiLLM import GeminiLLM

# client_openAI = OpenAI()

class ToDoGUI:
        
    def __init__(self, fastAPI_url):
        self.fastAPI_url = fastAPI_url
        # self.gemini_llm = GeminiLLM()
        
        load_dotenv()
        # Fetch the API key from environment variables
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables or .env file.")
        
        self.chatgpt = ChatGPT(api_key)  # Replace with actual key
        
    def get_all_tasks(self):
        try:
            response = requests.get(f"{self.fastAPI_url}/tasks")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching tasks: {e}")
            return {}

    def create_task(self, task, description):
        try:
            task_data = {"task": task, "description": description}
            response = requests.post(f"{self.fastAPI_url}/tasks", json=task_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error creating task: {e}")
            return {}

    def get_task(self, task_id):
        response = requests.get(f"{self.fastAPI_url}/tasks/{task_id}")
        return response.json()

    def update_task(self, task_id, task, description):
        task_data = {"task": task, "description": description}
        response = requests.post(f"{self.fastAPI_url}/tasks/{task_id}", json=task_data)
        return response.json()
    
    def render_suggestions(self):
        # Suggestions
        suggestions = ["3 + 6", "write a greeting in one line", "Do nothing"]
        if "selected_suggestion" not in st.session_state:
            st.session_state.selected_suggestion = ""
            
        st.markdown(
            """
            <style>
            .suggestions-container {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }
            .suggestion-button {
                background-color: #f0f8ff;
                color: #333;
                border: none;
                padding: 5px 10px;
                font-size: 12px;
                border-radius: 5px;
                cursor: pointer;
                box-shadow: 1px 1px 5px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
            }
            .suggestion-button:hover {
                background-color: #d8e7f3;
                box-shadow: 2px 2px 7px rgba(0,0,0,0.3);
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown('<div class="suggestions-container">', unsafe_allow_html=True)
        for suggestion in suggestions:
            button_html = f"""
                <button class="suggestion-button" onclick="document.getElementById('task-input').value = '{suggestion}'" 
                        style="background-color: #f0f8ff; color: #333; border: none; padding: 5px 10px;
                               font-size: 12px; border-radius: 5px; cursor: pointer; 
                               box-shadow: 1px 1px 5px rgba(0,0,0,0.2); 
                               transition: all 0.3s ease;">
                    {suggestion}
                </button>
            """
            st.markdown(button_html, unsafe_allow_html=True)
            
            # suggestion_html += button_html
        # suggestion_html += "</div>"
        st.markdown("</div>", unsafe_allow_html=True)
        # Display suggestions
        # st.markdown(suggestion_html, unsafe_allow_html=True)
        

    def render(self):
        # st.title("To-Do List Manager")
        st.title("Task Manager with FastAPI and ChatGPT") #Google Gemini and

        # Display All Tasks
        if st.button("My Tasks", type='primary'):
            tasks = self.get_all_tasks()
            st.write(tasks)

        # Add a New Task
        st.header("Add a New Task")
        
        st.session_state.selected_suggestion = ""
        #self.render_suggestions()
        
        # Input fields
        task = st.text_input("Task", value=st.session_state.selected_suggestion)
        # description = st.text_area("Task Description")
        description = ''
        # Create Task
        if st.button("Create Task", type='primary'):
            
            # Generate help text using ChatGPT
            help_text = self.chatgpt.generate_help_text(task, description)
            
            result = self.create_task(task, help_text)
            # st.success(f"Task Created: {result}")
            st.success(f"Your task is added to the list 'My Tasks'")
            
            # # Generate task details using Gemini LLM
            # details = self.gemini_llm.generate_task_details(task, description)
            # st.subheader("Generated Task Details")
            # st.write(details)
            
            st.subheader("Here is some help from ChatGPT for your task")
            st.write(help_text)

def check_server_status(fastApi_url):
    #"""Check if the FastAPI server is running."""
    for _ in range(10):  # Retry for a few seconds
        try:
            response = requests.get(fastApi_url)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            time.sleep(1)
    return False

def connect_FastAPI(retry=2):
    global fastapi_process
    fastApi_url = "http://127.0.0.1:9000"
    start_command = ["uvicorn", "src.fastAPI_toDo_app:app", "--host", "127.0.0.1", "--port", "9000", "--reload"]
    
    # for _ in range(retry):  # Retry for a few times
    if not check_server_status(fastApi_url):
        #"""Start the FastAPI server in a subprocess."""
        fastapi_process = subprocess.Popen( start_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, ) 
        time.sleep(3)  # Wait for the FastAPI server to start
    
    return fastApi_url

def terminate_FastAPI():
    # Cleanup: Stop FastAPI when Streamlit exits
    # if "fastapi_process" in locals():
    fastapi_process.terminate()
    fastapi_process.wait()
    st.write("FastAPI server terminated...")    
    
fastapi_process = None
# Run the Streamlit app
if __name__ == "__main__":
     # Start the FastAPI server
    fastApi_url = connect_FastAPI()
    
    if check_server_status(fastApi_url):
        st.button("Connect FastAPI server", on_click=connect_FastAPI)
    else:    
        st.write("FastAPI server started... " + fastApi_url + '/docs')
        # st.button("Disconnect FastAPI server", on_click=terminate_FastAPI)
    
    todo_gui = ToDoGUI(fastApi_url)
    todo_gui.render()
    