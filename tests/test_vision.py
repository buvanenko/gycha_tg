import pytest
from vision import get, translate

@pytest.mark.asyncio
async def test_translate():
    test_text = "Hello, world!"
    result = await translate(test_text)
    assert isinstance(result, str)

@pytest.mark.asyncio
async def test_get():
    url = "https://raw.githubusercontent.com/buvanenko/mocks/main/face.jpg"
    result = await get(url)
    assert isinstance(result, str)

