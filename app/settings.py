"""Application settings."""

import os

from pydantic import Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Application settings class."""

    bot_token: str
    debug: bool = Field(default=False)
    reflink_template: str = 'https://t.me/epsilionwarbot?start=ref-{user_id}'
    default_ref_user_id: int = 1105883852


app_settings = AppSettings(
    _env_file=os.path.join(os.path.dirname(__file__), '..', '.env'),  # type: ignore
)
