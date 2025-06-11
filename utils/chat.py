from utils import qwen
import database
from prompts import prompts

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

async def get(username: str, message: str, thread_id: int = 0) -> str:
    add_message("user", username, message, thread_id)
    answer = await qwen.get_response(get_messages(thread_id))
    add_message("assistant", username, answer, thread_id)
    return answer