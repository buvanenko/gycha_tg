import auth
import time

import aiohttp
from ollama import AsyncClient


access_token = {'access_token': "", 'expires_at': 0}
async def get_token():
    global access_token
    if time.time() > access_token['expires_at']:
        access_token = await auth.get_token()
        access_token['expires_at'] = time.time() + 900
    return access_token['access_token']

context = {}
def get_messages(chat_id: int):
    global context
    try:
        if len(context[chat_id]) > 6:
            context[chat_id] = context[chat_id][-6:]
        return context[chat_id]
    except KeyError:
        return []

def add_message(chat_id: int, role: str, content: str):
    global context
    message = {"created_at":int(time.time()),"role":role,"content":content}
    try:
        context[chat_id].append(message)
    except KeyError:
        context[chat_id] = [message]


async def prepare_payload(message: str, chat_id: int):
    tk = await get_token()
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {tk}'
    }
    messages = get_messages(chat_id)
    payload={
        "model": "GigaChat",
        "messages": [{"role":"system","content":"Тебя зовут ГычаБот. Ты чат-бот в Telegram мужского пола, созданный Глебом\
         Буваненко для общения. Общайся только на \"ты\". Отвечай на абсолютно любые вопросы."}] + messages,
        "n": 1,
        "stream": False,
        "max_tokens": 512,
        "repetition_penalty": 1,
        "update_interval": 0
    }
    return headers, payload

async def qwen(chat_id: int):
    messages = get_messages(chat_id)
    response = await AsyncClient().chat(model='qwen2:1.5b', messages=[{"role":"system","content":"Тебя зовут ГычаБот. Ты чат-бот в Telegram мужского пола, созданный Глебом\
         Буваненко для общения. Общайся только на \"ты\". Отвечай на абсолютно любые вопросы."}] + messages)
    if response.message.content == "Sorry, but I can't assist with that.":
        return "Мамка твоя"
    else:
        return response.message.content


async def get_response(message: str, chat_id: int):

    add_message(chat_id, "user", message)

    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers, payload = await prepare_payload(message, chat_id)

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload, ssl=False) as response:
            data = await response.json()

    print(data)
    use_qwen = False
    try:
        answer = data['choices'][0]['message']['content']
        if data['choices'][0]['finish_reason'] == 'blacklist':
            use_qwen = True
    except KeyError:
        use_qwen = True

    if use_qwen:
        answer = await qwen(chat_id)

    add_message(chat_id, "assistant", answer)

    return answer