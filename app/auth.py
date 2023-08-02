"""Staff-only util for auth in telegram as user account."""

import asyncio
import logging

from pyrogram import Client

from app.settings import app_settings

logger = logging.getLogger(__file__)


async def main() -> None:
    """Auth user."""
    async with Client(
        name='user_bot_auth',
        api_id=app_settings.telegram_api_id,
        api_hash=app_settings.telegram_api_hash,
        phone_number=app_settings.telegram_phone_number,
        session_string=app_settings.user_bot_session,
        in_memory=True,
    ) as user_bot_client:
        logger.info('{0} session: "{1}"'.format(
            (await user_bot_client.get_me()).username,
            await user_bot_client.export_session_string(),
        ))


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.debug else logging.INFO,
        format='%(asctime)s %(levelname)-8s bot: %(message)s',  # noqa: WPS323
    )
    asyncio.run(main())
