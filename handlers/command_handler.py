from telebot import types
from db import get_db_session
from db.models import Customer, Manager, Merchant
from handlers import IHandler
from enums import UserType


class CommandHandler(IHandler):

    @staticmethod
    def pre_receive(func):
        def inner1(self: IHandler, message: types.Message):

            self.detect_user_type(message.chat.id)

            func(self, message)

        return inner1

    @pre_receive
    def handler(self, message: types.Message):
        command, chat_id = message.text, message.chat.id

        print(self.bot.user_type)
