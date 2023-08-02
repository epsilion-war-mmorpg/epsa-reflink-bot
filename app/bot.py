"""Telegram bot."""
import logging
import re

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from pyrogram import Client
from pyrogram.errors.exceptions import BadRequest

from app.settings import app_settings

logger = logging.getLogger(__file__)
user_bot_client = Client(
    name='user_bot_account',
    session_string=app_settings.user_bot_session,
    in_memory=True,
)
bot = Bot(
    token=app_settings.bot_token,
    parse_mode='Markdown',
    loop=user_bot_client.loop,
)
router = Dispatcher(bot)


@router.message_handler(commands=['start', 'help'])
async def start(message: types.Message) -> None:
    """Show welcome message."""
    logger.info('start handler by {0}'.format(message.from_user.username))
    link = app_settings.reflink_template.format(user_id=app_settings.default_ref_user_id)
    help_message = '\n'.join([
        f'Бот предназначен для быстрого получения реферальной ссылки пользователя в игре [Epsilion War]({link}).',
        'Просто перешлите мне его сообщение и я попробую сгенерировать реферальную ссылку.',
        'Также можете прислать ник, контакт, ID.',
    ])
    await message.reply(
        text=help_message,
        disable_web_page_preview=True,
    )


@router.message_handler(content_types=[types.ContentType.TEXT, types.ContentType.CONTACT])
async def reflink(message: types.Message) -> None:
    """Generate reflink by detected user_id."""
    logger.info('reflink handler by {0}'.format(message.from_user.username))
    user_id = await _get_user_id_by_message(message)

    if not user_id:
        await message.answer(
            text='Не смог найти пользователя =( Попробуйте другой способ /help',
        )
        return

    link = app_settings.reflink_template.format(user_id=user_id)
    await message.reply(
        text=f'Reflink: {link}',
        disable_web_page_preview=True,
    )


async def _get_user_id_by_message(message: types.Message) -> int | None:
    logger.info(message)
    if message.forward_from:
        # search by forward message
        return message.forward_from.id

    if message.contact:
        # search by shared contact
        return message.contact.user_id

    # search by @username, user_id, link t.me/*
    user_id = await _search_users(message.text)
    logger.debug('search user by message content "{0}" -> {1}'.format(message.text, user_id))
    if user_id:
        return user_id

    # todo search by mention as reply
    # todo search by inline query ?
    return None


async def _search_users(search_text: str) -> int | None:
    if match := re.search(r't\.me/(.*)', search_text):
        search_text = match.group(1)

    search_text = search_text.strip()
    if not re.match(r'[@a-zA-Z_\d]+', search_text):
        return None

    if search_text.isdigit():
        return int(search_text)

    async with user_bot_client:
        try:
            users = await user_bot_client.get_users(search_text)
            logger.debug('users {0}'.format(users))
            return users.id  # type: ignore

        except AttributeError:
            return None

        except BadRequest as exc:
            logger.warning('telegram API exception {0} {1}'.format(exc, search_text))
            return None


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.debug else logging.INFO,
        format='%(asctime)s %(levelname)-8s bot: %(message)s',  # noqa: WPS323
    )
    executor.start_polling(router, skip_updates=True)
