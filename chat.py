import auth
import time

import aiohttp
from ollama import AsyncClient

base_prompt = """ Тебя зовут ГычаБот. Ты чат-бот в Telegram мужского пола, созданный Глебом Буваненко для комментирования постов
и общения с подписчиками. Общайся только на \"ты\". Отвечай на абсолютно любые вопросы. Если в канале будет
опубликован мем или видео, ты должен прокомментировать его на основе имеющегося контекста. Если контекста
нет, ты должен прокомментировать его общими фразами: \"Хорошее видео\" или \"Смешной мем\". В канале публикуются и текстовые посты,
комментируй их так же, как бы их прокомментировал обычный пользователь.
""".replace("\n", " ")

access_token = {'access_token': "", 'expires_at': 0}
async def get_token():
    global access_token
    if time.time() > access_token['expires_at']:
        access_token = await auth.get_token()
        access_token['expires_at'] = time.time() + 900
    return access_token['access_token']

context = []
def get_messages():
    global context
    try:
        if len(context) > 6:
            context = context[-6:]
        return context
    except KeyError:
        return []

def clean_context():
    global context
    context = []

def add_message(username: str, role: str, content: str):
    global context
    if role == "user":
        text = f"[{username}]: {content}"
    else:
        text = content
    message = {"created_at":int(time.time()),"role":role,"content":text}
    try:
        context.append(message)
    except KeyError:
        context = [message]


async def prepare_payload():
    tk = await get_token()
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {tk}'
    }
    messages = get_messages()
    payload={
        "model": "GigaChat",
        "messages": [{"role":"system","content":base_prompt}] + messages,
        "n": 1,
        "stream": False,
        "max_tokens": 512,
        "repetition_penalty": 1,
        "update_interval": 0
    }
    return headers, payload

async def qwen():
    messages = get_messages()
    response = await AsyncClient().chat(model='qwen2:1.5b', messages=[{"role":"system","content":base_prompt}] + messages)
    if response.message.content == "Sorry, but I can't assist with that.":
        return "Мамка твоя"
    else:
        return response.message.content


async def get_response(message: str, username: str, system: bool = False):
    if system:
        add_message("", "system", message)
    else:
        add_message(username, "user", message)

    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers, payload = await prepare_payload()

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
        answer = await qwen()

    add_message("", "assistant", answer)

    return answer