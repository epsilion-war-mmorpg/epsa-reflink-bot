from unittest.mock import AsyncMock

from app.bot import inline_reflink


async def test_inline_reflink():
    query_mock = AsyncMock()
    query_mock.query = 'esemiko'

    await inline_reflink(inline_query=query_mock)

    query_mock.answer.assert_called_once()
