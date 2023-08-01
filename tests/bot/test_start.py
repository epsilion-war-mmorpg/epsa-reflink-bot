from unittest.mock import AsyncMock

from app.bot import start


async def test_start():
    message_mock = AsyncMock()

    await start(message=message_mock)

    message_mock.reply.assert_called_once()
