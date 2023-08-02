import asyncio

from pyrogram import Client

from app.settings import app_settings


async def main() -> None:
    async with Client(
        name="user_bot_account",
        api_id=app_settings.telegram_api_id,
        api_hash=app_settings.telegram_api_hash,
        phone_number=app_settings.telegram_phone_number,
        session_string=app_settings.user_bot_session,
        in_memory=True,
    ) as user_bot_client:
        print('{0} session: "{1}"'.format(
            (await user_bot_client.get_me()).username,
            await user_bot_client.export_session_string(),
        ))


if __name__ == '__main__':
    asyncio.run(main())
