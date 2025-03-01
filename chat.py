from ollama import AsyncClient
from prompts import prompts
from config import config
import sber

import json

context = {}
def load():
    global context
    try:
        with open('dialogs.json', 'r', encoding='utf-8') as f:
            context = json.load(f)
    except FileNotFoundError:
        print('Немаэ')
def save():
    global context
    with open('dialogs.json', 'w', encoding='utf-8') as f:
        json.dump(context, f)

def get_messages(thread_id: int = 0) -> list:
    global context
    thread_id = str(thread_id)
    try:
        messages = context[thread_id]
    except KeyError:
        messages = context[thread_id] = []

    base_prompt = [{"role":"system","content":prompts.chat}]

    if len(messages) > 15:
        messages = [messages[0]] + messages[-15:]

    return base_prompt + messages


def add_message(role: str, username: str, content: str, thread_id: int = 0):
    global context
    thread_id = str(thread_id)
    if role == "user":
        text = f"[{username}]: {content}"
    else:
        text = content
    message = {"role":role,"content":text}
    try:
        context[thread_id].append(message)
    except KeyError:
        context[thread_id] = [message]

async def generate(thread_id: int = 0) -> str:
    messages = get_messages(thread_id)
    response = await AsyncClient().chat(model=config.models.chat, messages=messages)
    if response.message.content == "Sorry, but I can't assist with that.":
        return "Мамка твоя"
    else:
        return response.message.content
    
async def get(username: str, message: str, thread_id: int = 0) -> str:
    add_message("user", username, message, thread_id)
    answer = await sber.get_response(get_messages(thread_id))
    if answer is None:
        answer = await generate(thread_id)
    add_message("assistant", username, answer, thread_id)
    return answer