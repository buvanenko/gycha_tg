import time
import aiohttp
from config import config

url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

payload='scope=GIGACHAT_API_PERS'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'RqUID': config.sber.uid,
    'Authorization': 'Basic ' + config.sber.auth
}

access_token = {'access_token': "", 'expires_at': 0}
async def get_token() -> str:
    global access_token
    if time.time() > access_token['expires_at']:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload, headers=headers, ssl=False) as response:
                access_token = await response.json()
        access_token['expires_at'] = time.time() + 900
    return access_token['access_token']
        

async def prepare_payload(messages: list) -> tuple[dict, dict]:
    tk = await get_token()
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {tk}'
    }
    payload={
        "model": "GigaChat",
        "messages": messages,
        "n": 1,
        "stream": False,
        "max_tokens": 512,
        "repetition_penalty": 1,
        "update_interval": 0
    }
    return headers, payload


async def get_response(messages: list) -> str | None:
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers, payload = await prepare_payload(messages)
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload, ssl=False) as response:
            data = await response.json()
    try:
        answer = data['choices'][0]['message']['content']
        if data['choices'][0]['finish_reason'] == 'blacklist':
            return None
    except KeyError:
        return None
    return answer

if __name__ == "__main__":
    import asyncio
    async def main():
        print(await get_token())
    asyncio.run(main())