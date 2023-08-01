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
)
async def start(message: types.Message) -> None:
    """Show welcome message."""
    link = app_settings.reflink_template.format(user_id=app_settings.default_ref_user_id)
    help_message = '\n'.join([
        f'Бот предназначен для быстрого получения реферальной ссылки пользователя в игре [Epsilion War]({link}).',
        'Просто перешлите мне его сообщение и я попробую сгенерировать реферальную ссылку.',
    ])
    await message.reply(
        text=help_message,
        disable_web_page_preview=True,
    )


@router.message_handler()
async def reflink(message: types.Message) -> None:
    """Generate reflink by detected user_id."""
    user_id = _get_user_id_by_message(message)
    if not user_id:
        await message.answer(
            text='Не смог найти пользователя =( Попробуйте другой способ /help',
        )
        return

    link = app_settings.reflink_template.format(user_id=user_id)
    await message.reply(
        text=f'User: {user_id}.\nReflink: {link}',
        disable_web_page_preview=True,
    )


def _get_user_id_by_message(message: types.Message) -> int | None:
    logging.debug(message)

    if message.forward_from:
        # search by forward message
        return message.forward_from.id

    # todo search by @username mention
    # todo search by link t.me
    # todo search by user_id
    # todo search by mention in reply
    return None


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.debug else logging.INFO,
        format='%(asctime)s %(levelname)-8s bot: %(message)s',  # noqa: WPS323
    )

    executor.start_polling(router, skip_updates=True)
