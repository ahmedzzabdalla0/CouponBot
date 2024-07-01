from abc import ABC, abstractmethod
from typing import Callable
from coupon_bot import ITeleBot
from telebot import types

from db import get_db_session
from db.models import Manager, Merchant
from enums import UserType


class IHandler(ABC):

    def __init__(self, bot: ITeleBot) -> None:
        self.bot = bot

    def detect_user_type(self, chat_id: str | int):
        if not chat_id in self.bot.user_status:
            session = get_db_session()
            if session.query(Manager).filter_by(chat_id=chat_id):
                self.bot.user_status[chat_id] = UserType.MANAGER
            elif session.query(Merchant).filter_by(chat_id=chat_id):
                self.bot.user_status[chat_id] = UserType.MERCHANT
            else:
                self.bot.user_status[chat_id] = UserType.MERCHANT

    @abstractmethod
    def handler(*arg):
        ...
