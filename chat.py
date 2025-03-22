from ollama import AsyncClient
from prompts import prompts
from config import config
import sber
import qwen
import database


def get_messages(thread_id: int = 0) -> list:
    thread_id = str(thread_id)
    messages = database.get_messages_by_dialog_id(thread_id)
    base_prompt = [{"role":"system","content":prompts.chat}]
    return base_prompt + messages


def add_message(role: str, username: str, content: str, thread_id: int = 0):
    thread_id = str(thread_id)
    if role == "user":
        text = f"[{username}]: {content}"
    else:
        text = content
    database.add_message(thread_id, role, text)


async def generate(thread_id: int = 0) -> str:
    messages = get_messages(thread_id)
    response = await AsyncClient().chat(model=config.models.chat, messages=messages)
    if response.message.content == "Sorry, but I can't assist with that.":
        return "Мамка твоя"
    else:
        return response.message.content
    
async def get(username: str, message: str, thread_id: int = 0) -> str:
    add_message("user", username, message, thread_id)
    answer = await qwen.get_response(get_messages(thread_id))
    if answer is None:
        answer = await sber.get_response(get_messages(thread_id))
    if answer is None:
        answer = await generate(thread_id)
    add_message("assistant", username, answer, thread_id)
    return answer