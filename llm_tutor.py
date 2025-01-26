# Imports

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import ollama
import gradio as gr


# Checking the API Key

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists")
else:
    print("OpenAI API Key not set")
    

# Setting Constants

MODEL = "gpt-4o-mini"
openai = OpenAI()

OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL_LLAMA = 'llama3.2:3b'


# Setting the prompts

system_message = """
You're an AI Tutor built for explaining technical concepts to students in a simple way.
"""
system_message += "Always be accurate. If you don't know the answer, say so."


def chat(message, history, model):
    try:
        if model == "GPT":
            # Prepare messages for OpenAI API
            messages = [{"role": "system", "content": "You are a helpful assistant."}] + \
                       [{"role": "user" if i % 2 == 0 else "assistant", "content": msg} 
                        for i, msg in enumerate(sum(history, []))] + \
                       [{"role": "user", "content": message}]
            
            # Stream response for OpenAI
            full_response = ""
            for chunk in openai.chat.completions.create(
                model=MODEL, 
                messages=messages,
                stream=True
            ):
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield full_response
        
        elif model == "Ollama":
            # Prepare messages for Ollama
            messages = [{"role": "user", "content": message}]
            
            # Stream response for Ollama
            full_response = ""
            for chunk in ollama.chat(
                model=MODEL_LLAMA, 
                messages=messages,
                stream=True
            ):
                if 'message' in chunk and 'content' in chunk['message']:
                    content = chunk['message']['content']
                    full_response += content
                    yield full_response
        
        else:
            yield "Invalid model selected"
    
    except Exception as e:
        yield f"An error occurred: {str(e)}"


# Create the Gradio interface

with gr.Blocks() as demo:
    # Model selection dropdown
    model_dropdown = gr.Dropdown(
        choices=["GPT", "Ollama"], 
        value="GPT", 
        label="Select Model"
    )
    
    # ChatInterface with model as an additional parameter
    chatbot = gr.ChatInterface(
        fn=chat,
        additional_inputs=[model_dropdown]
    )

# Launch the demo
demo.launch()