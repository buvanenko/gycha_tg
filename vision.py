import aiohttp
import logging

from ollama import AsyncClient
from prompts import prompts
from config import config
import sber
import qwen

url = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions"

async def translate(text: str) -> str:
    messages = [
        {"role":"system","content":prompts.translator},
        {"role":"user", "content":text}
    ]
    logging.info("Используем Qwen для перевода...")
    answer = await qwen.get_response(messages)
    if answer is None:
        logging.info("Ошибка при переводе через Qwen, используем ГигаЧат для перевода...")
        answer = await sber.get_response(messages)
    if answer is None:
        logging.info("Ошибка при переводе через ГигаЧат, переключаемся на локальную модель")
        response = await AsyncClient().chat(model=config.models.chat, messages=messages)
        answer = response.message.content
    return answer

async def get(url: str, lang="rus") -> str:
    logging.info("Использую локальную модель для распознавания изображения...")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()
    caption_eng = await AsyncClient().generate(model=config.models.vision, prompt=prompts.vision, images=[content])
    if lang == "rus":
        caption = await translate(caption_eng.response)
    else:
        caption = caption_eng.response
    return caption

async def get_qwen(image_url: str) -> str | None:
    logging.info("Использую AlibabaCloud для распознавания изображения...")
    headers = {
        "Authorization": f"Bearer {config.qwen.token}",
        "Content-Type": "application/json"
    }
    messages=[
        {
            "role": "system",
            "content": [{"type": "text", "text": prompts.vision_qwen}],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    },
                },
                {"type": "text", "text": "Опиши данное изображение."},
            ],
        },
    ]
    payload = {"model": config.qwen.visual, "messages": messages}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload, ssl=False) as response:
                data = await response.json()
    except:
        return None
    try:
        answer = data['choices'][0]['message']['content']
    except KeyError:
        answer = None
    return answer
