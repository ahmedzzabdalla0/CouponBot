from telebot import types
from handlers import IHandler
from message_center import messages


class MessageHandler(IHandler):

    @staticmethod
    def pre_receive(func):
        def inner1(self: IHandler, message: types.Message):

            self.detect_user_type(message.chat.id)

            func(self, message)

        return inner1

    def handler(self, message: types.Message):
        print(f"Message is {message.text}")
        self.bot.send_message_queue(
            message.chat.id, messages.LoginEnterPass.generate())
