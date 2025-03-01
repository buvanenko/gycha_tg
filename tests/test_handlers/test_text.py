import pytest
from unittest.mock import AsyncMock, Mock, patch

from handlers.text import text

@pytest.mark.asyncio
async def test_text():
    # Создаем тестовые данные
    test_data = AsyncMock()
    test_data.file_path = "test_file_path"

    test_bot = AsyncMock()
    test_bot.id = 1
    test_bot.get_file.return_value = test_data

    test_chat = AsyncMock()
    test_chat.get.return_value = "test_answer"

    test_message = AsyncMock()
    test_message.is_automatic_forward = True
    test_message.text = "test_text"

    with patch('handlers.text.Message', return_value=test_message), \
        patch('handlers.text.bot', test_bot), \
        patch('handlers.text.chat', test_chat):

        await text(test_message)

        test_message.reply.assert_called_with("test_answer", parse_mode="Markdown")