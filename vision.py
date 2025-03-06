import aiohttp
import logging

from ollama import AsyncClient
from prompts import prompts
from config import config
import sber
import qwen

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
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()
    caption_eng = await AsyncClient().generate(model=config.models.vision, prompt=prompts.vision, images=[content])
    if lang == "rus":
        caption = await translate(caption_eng.response)
    else:
        caption = caption_eng.response
    return caption