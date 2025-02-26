from ollama import AsyncClient
from prompts import prompts
from config import config
import sber

context = []
def get_messages() -> list:
    global context
    base_prompt = [{"role":"system","content":prompts.chat}]
    try:
        if len(context) > 15:
            context = [context[0]] + context[-15:]
        return base_prompt + context
    except KeyError:
        return []
    
def clean_context():
    global context
    context = []

def add_message(role: str, username: str, content: str):
    global context
    if role == "user":
        text = f"[{username}]: {content}"
    else:
        text = content
    message = {"role":role,"content":text}
    try:
        context.append(message)
    except KeyError:
        context = [message]

async def generate() -> str:
    messages = get_messages()
    response = await AsyncClient().chat(model=config.models.chat, messages=messages)
    if response.message.content == "Sorry, but I can't assist with that.":
        return "Мамка твоя"
    else:
        return response.message.content
    
async def get(username: str, message: str) -> str:
    add_message("user", username, message)
    answer = await sber.get_response(get_messages())
    if answer is None:
        answer = await generate()
    add_message("assistant", username, answer)
    return answer