"""Telegram bot."""
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from pyrogram import Client
from pyrogram.errors.exceptions import BadRequest

from app.settings import app_settings

logger = logging.getLogger(__file__)
user_bot_client = Client(
    name="user_bot_account",
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
    logger.info('start handler')
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
    logger.info('reflink handler by {0}'.format(message.from_user.username))
    user_id = await _get_user_id_by_message(message)

    if not user_id:
        await message.answer(
            text='Не смог найти пользователя =( Попробуйте другой способ /help',
        )
        return

    link = app_settings.reflink_template.format(user_id=user_id)
    await message.reply(
        text=f'User: {user_id}\nReflink: {link}',
        disable_web_page_preview=True,
    )


async def _get_user_id_by_message(message: types.Message) -> int | None:
    logger.debug(message)

    if message.forward_from:
        # search by forward message
        return message.forward_from.id

    search_text = message.text.strip()
    logger.debug('search user by message content "{0}"'.format(search_text))
    user_id = None
    if search_text:
        # todo search by @username
        # todo search by user_id
        # todo search by link t.me
        user_id = await _search_users(search_text)

    if user_id:
        return user_id

    # todo search by mention as reply
    return None


async def _search_users(search_text: str) -> int | None:
    async with user_bot_client:
        try:
            users = await user_bot_client.get_users(search_text)
            logger.info('users %s', users)
            return users.id  # type: ignore

        except AttributeError:
            return None

        except BadRequest as exc:
            logger.warning('telegram API exception %s %s', exc, search_text)
            return None


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.debug else logging.INFO,
        format='%(asctime)s %(levelname)-8s bot: %(message)s',  # noqa: WPS323
    )
    executor.start_polling(router, skip_updates=True)
