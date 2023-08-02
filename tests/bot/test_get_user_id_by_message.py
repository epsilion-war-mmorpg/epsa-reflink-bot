from unittest.mock import AsyncMock

from app.bot import _get_user_id_by_message


async def test_get_user_id_by_message_forward_message():
    message_mock = AsyncMock()
    message_mock.forward_from.id = 123

    response = await _get_user_id_by_message(message_mock)

    assert response == 123


async def test_get_user_id_by_message_forward_message_hidden():
    message_mock = AsyncMock()
    message_mock.forward_from = None
    message_mock.forward_sender_name = '🍻Jiřy'

    response = await _get_user_id_by_message(message_mock)

    assert response is None
