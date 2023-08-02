from unittest.mock import AsyncMock

import pytest

from app.bot import _get_user_id_by_message


async def test_get_user_id_by_message_contact():
    message_mock = AsyncMock()
    message_mock.forward_from = None
    message_mock.contact.user_id = 123456

    response = await _get_user_id_by_message(message_mock)

    assert response == 123456


async def test_get_user_id_by_message_forward_message():
    message_mock = AsyncMock()
    message_mock.forward_from.id = 123
    message_mock.text = 'dssdsd'

    response = await _get_user_id_by_message(message_mock)

    assert response == 123


async def test_get_user_id_by_message_forward_message_hidden():
    message_mock = AsyncMock()
    message_mock.contact = None
    message_mock.forward_from = None
    message_mock.forward_sender_name = '🍻Jiřy'
    message_mock.text = 'dssdsd'

    response = await _get_user_id_by_message(message_mock)

    assert response is None


@pytest.mark.parametrize('payload, expected', [
    ('537453818', 537453818),
    ('esemiko', 537453818),
    (' esemiko  ', 537453818),
    ('https://t.me/esemiko', 537453818),
    ('@World1010', 1501601109),
    ('невалидный ник', None),
    ('not_found_fffffffffffffffffffffffff', None),
    ('', None),

])
async def test_get_user_id_by_username(payload: str, expected: int | None):
    message_mock = AsyncMock()
    message_mock.forward_from = None
    message_mock.contact = None
    message_mock.text = payload

    response = await _get_user_id_by_message(message_mock)

    assert response == expected
