import time
import aiohttp
from config import config

from prompts import prompts

url = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {config.qwen.token}",
    "Content-Type": "application/json"
}


async def get_response(messages: list) -> str | None:
    payload = {"model": config.qwen.model, "messages": messages}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload, ssl=False) as response:
            data = await response.json()
    try:
        answer = data['choices'][0]['message']['content']
    except:
        answer = None
    print(answer)
    return answer