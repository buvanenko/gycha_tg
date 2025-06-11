import logging
import aiohttp
from prompts import prompts
from config import config

url = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions"

async def get(image_url: str) -> str | None:
    logging.info("Использую AlibabaCloud для распознавания изображения...")
    headers = {
        "Authorization": f"Bearer {config.qwen.token}",
        "Content-Type": "application/json"
    }
    messages=[
        {
            "role": "system",
            "content": [{"type": "text", "text": prompts.vision}],
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
        print(data)
    except:
        print(data)
        return None
    try:
        answer = data['choices'][0]['message']['content']
    except KeyError:
        answer = None
    return answer
