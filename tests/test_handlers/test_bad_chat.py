import pytest
from unittest.mock import AsyncMock, patch
from handlers.bad_chat import info

@pytest.mark.asyncio
async def test_info():
    # Создаем тестовые данные
    test_message = AsyncMock()
    test_message.chat.id = 123456789  # Замените на ID чата, который не является config.telegram.chat_id
    expected_reply = "Тут я не отвечаю. Я работаю только в комментариях этого канала: @gleb_vedaet"

    # Заменяем Message на mock объект
    with patch('handlers.bad_chat.Message', return_value=test_message):
        # Вызываем функцию info
        await info(test_message)

        # Проверяем, что функция reply была вызвана с ожидаемым аргументом
        test_message.reply.assert_called_with(expected_reply)
