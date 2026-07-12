import ollama   # AI library
import logging  # python logger
import json     # for parsing JSON strings
from functools import lru_cache
from src.config import get_chat_model, OLLAMA_URL, JSON_MAX_RETRIES   # import the configuration

logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def get_client():
    client = ollama.Client(host=OLLAMA_URL)
    return client

def generate(prompt, system_prompt=""):
    client = get_client()
    
    messages = [] # create message list
    
    if system_prompt:  # if system prompt exist, include it
        messages.append({"role": "system", "content": system_prompt})
        
    messages.append({"role": "user",   "content": prompt})
    
        
    response = client.chat(model=get_chat_model(), messages=messages, think=False)
 
        
    return response.message.content

def generate_streaming(prompt, system_prompt=""):
    client = get_client()
    
    messages = [] # create message list
    
    if system_prompt:  # if system prompt exist, include it
        messages.append({"role": "system", "content": system_prompt})
        
    messages.append({"role": "user",   "content": prompt})
    
        
    response = client.chat(model=get_chat_model(), messages=messages, stream=True, think=False)
    for chunk in response:
        yield chunk.message.content

def generate_json(prompt, system_prompt="", schema=None):
    client = get_client()

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.append({"role": "user", "content": prompt})

    # If a schema is provided, pass it through to the model's format parameter
    json_format = schema if schema is not None else "json"

    for attempt in range(JSON_MAX_RETRIES):
        response = client.chat(model=get_chat_model(), messages=messages, format=json_format, think=False, options={"temperature": 0.1})
        try:
            # When using Ollama with a schema, the content is still JSON text
            data = json.loads(response.message.content)
            return data
        except json.JSONDecodeError:
            logger.warning(f"JSON parse failed on attempt {attempt + 1} of {JSON_MAX_RETRIES}")
            # nudging the model to output only JSON for the retry
            messages[-1]["content"] = prompt + "\n\nRespond with ONLY a valid JSON object. No explanation, no markdown, just JSON."
    return None
    
     