import pytest
from sber import get_token, prepare_payload, get_response
from prompts import prompts

messages = [
    {"role":"system","content":prompts.chat}, 
    {"role":"user","content":"Как тебя зовут?"},
]

@pytest.mark.asyncio
async def test_get_token():
    result = await get_token()
    assert isinstance(result, str)

@pytest.mark.asyncio
async def test_prepare_payload():
    result1, result2 = await prepare_payload(messages)
    assert isinstance(result1, dict) and isinstance(result2, dict)


@pytest.mark.asyncio
async def test_get_response():
    result = await get_response(messages)
    assert "ГычаБот" in result