"""Application settings."""

import os

from pydantic import Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Application settings class."""

    bot_token: str
    telegram_api_id: int = 123456
    telegram_api_hash: str = 'u_api_hash_here'
    telegram_phone_number: str = '+7123456789'
    user_bot_session: str = 'must be filled by python -m app.pyrogram_auth'

    debug: bool = Field(default=False)
    reflink_template: str = 'https://t.me/epsilionwarbot?start=ref-{user_id}'
    default_ref_user_id: int = 1105883852


app_settings = AppSettings(
    _env_file=os.path.join(os.path.dirname(__file__), '..', '.env'),  # type: ignore
)
