from unittest.mock import AsyncMock

from app.bot import reflink


async def test_reflink():
    message_mock = AsyncMock()
    message_mock.forward_from = None
    message_mock.text = ''

    await reflink(message=message_mock)

    message_mock.answer.assert_called_once()
