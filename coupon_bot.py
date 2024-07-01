from abc import ABC, abstractmethod
from telebot import ExceptionHandler, TeleBot, types
from telebot.handler_backends import HandlerBackend
from telebot.storage import StateStorageBase
from typing import Callable, Union, Dict, Tuple
from managers.flow_control import FlowControl
from message_center import Text
from enum import Enum
from enums import ParseMode, UserType

MESSAGE_RGX = "^(?!\/)(.|\n)*"
COMMAND_RGX = "^(?=\/)(.|\n)*"


class ITeleBot(ABC, TeleBot):

    def __init__(self, token: str, parse_mode: str | None = None, threaded: bool | None = True, skip_pending: bool | None = False, num_threads: int | None = 2, next_step_backend: HandlerBackend | None = None, reply_backend: HandlerBackend | None = None, exception_handler: ExceptionHandler | None = None, last_update_id: int | None = 0, suppress_middleware_excepions: bool | None = False, state_storage: StateStorageBase | None = ..., use_class_middlewares: bool | None = False, disable_web_page_preview: bool | None = None, disable_notification: bool | None = None, protect_content: bool | None = None, allow_sending_without_reply: bool | None = None, colorful_logs: bool | None = False):
        super().__init__(token, parse_mode, threaded, skip_pending, num_threads, next_step_backend, reply_backend, exception_handler, last_update_id, suppress_middleware_excepions,
                         state_storage, use_class_middlewares, disable_web_page_preview, disable_notification, protect_content, allow_sending_without_reply, colorful_logs)
        self.user_status: Dict[Union[str, int], Tuple[Enum, Enum]] = {}
        self.user_type: Dict[Union[str, int], UserType] = {}
        self.flow_control = FlowControl(self)
        from handlers.message_handler import MessageHandler
        from handlers.command_handler import CommandHandler
        from handlers.callback_query_handler import CallbackHandler as CallHandler
        self.message_handler(regexp=MESSAGE_RGX)(MessageHandler(self).handler)
        self.message_handler(regexp=COMMAND_RGX)(CommandHandler(self).handler)
        self.callback_query_handler(lambda x: True)(CallHandler(self).handler)

    @abstractmethod
    def send_message_queue(self, chat_id: Union[int, str], text: Text) -> None:
        ...


class CouponBot(ITeleBot):

    def send_message_queue(self, chat_id: Union[int, str], text: Text) -> None:

        self.flow_control.append_queue(chat_id, text)
