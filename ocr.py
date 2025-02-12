import aiohttp
import pytesseract
from io import BytesIO
from PIL import Image

# pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()

    img = Image.open(BytesIO(content))
    text = pytesseract.image_to_string(img, lang="eng+rus")
    return text