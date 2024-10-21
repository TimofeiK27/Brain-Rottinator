import os, random, base64, io
from openai import OpenAI
from dotenv import load_dotenv
import requests
from PIL import Image

load_dotenv()
key = os.environ.get("OPENAI_KEY")

client = OpenAI(
    api_key=key
)

#model = "gpt-3.5-turbo"
model = "gpt-4o"

def chatGPT(prompt):
    temp = 1.0
    max_tokens = 500
    topic = ""
    frequency_penalty=0.9
    top_p=0.3
    presence_penalty=0.9
    messages = [
        {"role":"user","content":prompt}

    ]
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temp,
        max_tokens=max_tokens,
        frequency_penalty=frequency_penalty,
        top_p=top_p,
        presence_penalty=presence_penalty
    )
    return completion.choices[0].message.content[0:-1]

def promptE(prompt):
    temp = .8
    max_tokens = 500
    frequency_penalty=1.4
    presence_penalty=1.4
    messages = [
        {"role":"user","content":prompt}

    ]
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temp,
        max_tokens=max_tokens,
        frequency_penalty=frequency_penalty,
        #top_p=top_p,
        presence_penalty=presence_penalty
    )
    return completion.choices[0].message.content[0:-1]