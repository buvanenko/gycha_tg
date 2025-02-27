import pytest
from unittest.mock import AsyncMock, patch

from handlers.video import video

@pytest.mark.asyncio
async def test_video():
    # Создаем тестовые данные
    test_data = AsyncMock()
    test_data.file_path = "test_file_path"

    test_bot = AsyncMock()
    test_bot.id = 1
    test_bot.get_file.return_value = test_data

    test_chat = AsyncMock()
    test_chat.get.return_value = "test_answer"

    test_message = AsyncMock()
    test_message.is_automatic_forward = False
    test_message.reply_to_message = AsyncMock()
    test_message.reply_to_message.from_user.id = test_bot.id
    test_message.text = None
    test_message.photo = [AsyncMock()]
    test_message.video.thumbnail.file_id = "test_file_id"
    test_message.from_user.username = "test_username"

    test_ocr = AsyncMock()
    test_ocr.get.return_value = "test_text_ocr"

    test_vision = AsyncMock()
    test_vision.get.return_value = "test_text_vision"

    with patch('handlers.video.Message', return_value=test_message), \
         patch('handlers.video.bot', test_bot), \
         patch('handlers.video.vision', test_vision), \
         patch('handlers.video.ocr', test_ocr), \
         patch('handlers.video.chat', test_chat):
        # Вызываем функцию photo
        await video(test_message)

        test_message.reply.assert_called_with("test_answer", parse_mode="Markdown")