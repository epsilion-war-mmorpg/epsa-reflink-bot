"""Telegram bot."""
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from app import custom_filters
from app.settings import app_settings

bot = Bot(
    token=app_settings.bot_token,
    parse_mode='Markdown',
)
router = Dispatcher(bot)


@router.message_handler(
    custom_filters.is_private,
    commands=['start', 'help'],
    state='*',
)
async def start(message: types.Message) -> None:
    """
    Show welcome message.

    """
    reflink = app_settings.reflink_template.format(user_id=app_settings.default_ref_user_id)
    help_message = '\n'.join([
        f'Бот предназначен для быстрого получения реферальной ссылки пользователя в игре [Epsilion War]({reflink}).',
        'Просто пришлите ссылку на аккаунт игрока или перешлите его сообщение.'
    ])
    await message.reply(
        text=help_message,
    )


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.debug else logging.INFO,
        format='%(asctime)s %(levelname)-8s bot: %(message)s',  # noqa: WPS323
    )

    executor.start_polling(router, skip_updates=True)
