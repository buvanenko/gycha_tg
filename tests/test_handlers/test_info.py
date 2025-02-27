import pytest
from unittest.mock import AsyncMock, patch

from handlers.info import info

@pytest.mark.asyncio
async def test_info():
    # Создаем тестовые данные
    test_message = AsyncMock()
    test_message.chat.id = 123456789
    test_message.chat.type = "private"
    test_message.from_user.id = 987654321
    expected_reply = f"message.chat.id: {test_message.chat.id}\n"
    expected_reply += f"message.chat.type: {test_message.chat.type}\n"
    expected_reply += f"message.from_user.id: {test_message.from_user.id}"

    # Заменяем Message на mock объект
    with patch('handlers.info.Message', return_value=test_message):
        # Вызываем функцию info
        await info(test_message)

        # Проверяем, что функция reply была вызвана с ожидаемым аргументом
        test_message.reply.assert_called_with(expected_reply)
