# Imports

import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display, update_display
from openai import OpenAI
import ollama

# Checking the API Key
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if api_key and api_key.startswith('sk-proj-') and len(api_key)>10:
    print("API key looks good")
else:
    print("There might be a problem with your API key.")

# Setting Constants

MODEL_GPT = 'gpt-4o-mini'

OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL_LLAMA = 'llama3.2:3b'

# Setting the prompts

system_prompt = """
You're an AI Tutor built for explaining technical concepts to students in a simple way.
"""

question = """
what is stemming in NLP?
"""

messages=[
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": question}
  ]

# Using GPT

openai =  OpenAI()
stream = openai.chat.completions.create(
    model=MODEL_GPT,
    messages=messages,
    stream = True
    )
response = ""
display_handle = display(Markdown(""), display_id=True)
for chunk in stream:
    response += chunk.choices[0].delta.content or ''
    response = response.replace("```","").replace("markdown", "")
    update_display(Markdown(response), display_id=display_handle.display_id)


# Using Llama 3.2

response = ollama.chat(model=MODEL_LLAMA, messages=messages)
print(response['message']['content'])