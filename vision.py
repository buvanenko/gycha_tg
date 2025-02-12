import aiohttp

import moondream as md
from io import BytesIO
from PIL import Image

import asyncio

model = md.vl(model="moondream-0_5b-int8.mf.gz")

async def get(url: str):

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()

    img = Image.open(BytesIO(content))
    encoded_image = model.encode_image(img)

    caption = model.caption(encoded_image)["caption"]
    print(caption)

    return caption

async def main():
    url = "https://media.istockphoto.com/id/468091714/ru/видео/красивый-молодой-человек-на-кухне-с-чашкой-в-руки.jpg?s=640x640&k=20&c=JW-RumhahLxDuXJ0CqeONwywiUgleEKnqG7zqOIneHs="
    print(await get(url))

if __name__ == "__main__":
    asyncio.run(main())