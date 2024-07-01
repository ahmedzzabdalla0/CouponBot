from telebot.types import CallbackQuery
from handlers import IHandler


class CallbackHandler(IHandler):

    @staticmethod
    def pre_receive(func):
        def inner1(self: IHandler, call: CallbackQuery):

            self.detect_user_type(call.message.chat.id)

            func(self, call)

        return inner1

    def handler(self, call: CallbackQuery):
        print(f"Call is {call.message.text}")
