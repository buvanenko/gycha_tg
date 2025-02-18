import aiohttp

from ollama import AsyncClient

async def get(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()

    caption = await AsyncClient().generate(model="moondream", prompt="Describe this image in as much detail as possible, listing all the details.", images=[content])

    return caption.response