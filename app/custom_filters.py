"""Custom filters for bot handlers."""

from aiogram import types
from aiogram.dispatcher import filters

is_private = filters.ChatTypeFilter(types.ChatType.PRIVATE)
