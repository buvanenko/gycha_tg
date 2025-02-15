import aiohttp

import moondream as md
from io import BytesIO
from PIL import Image

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