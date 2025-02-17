import aiohttp
import pytesseract
from io import BytesIO
from PIL import Image

from sys import platform

if platform == 'win32':
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
else:
    pytesseract.pytesseract.tesseract_cmd = './usr/bin/tesseract'

async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()

    img = Image.open(BytesIO(content))
    text = pytesseract.image_to_string(img, lang="eng+rus")
    return text