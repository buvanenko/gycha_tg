import pytest
from chat import *

def test_get_messages():
    messages = get_messages()
    assert len(messages) == 1

def test_add_message():
    add_message("user", "username", "message")
    messages = get_messages()
    assert len(messages) == 2

@pytest.mark.asyncio
async def test_generate():
    text = await generate()
    assert isinstance(text, str)

@pytest.mark.asyncio
async def test_get():
    text = await get("SomeGuy", "Как тебя зовут?")
    assert "ГычаБот" in text