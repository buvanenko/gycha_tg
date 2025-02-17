import aiohttp

from ollama import AsyncClient

async def get(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()

    # img = BytesIO(content)

    caption = await AsyncClient().generate(model="moondream", prompt="What is this?", images=[content])
    print(caption.response)
    return caption.response