import pytest
from ocr import get

@pytest.mark.asyncio
async def test_get():
    url = "https://raw.githubusercontent.com/buvanenko/mocks/723a0dbfab1c554800ead55a9cd3731e7ececa8c/cyrillic_text.jpg"
    result = await get(url)
    assert "хомяк" in result.lower()