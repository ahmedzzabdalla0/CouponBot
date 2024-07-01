from collections import deque
from telebot import TeleBot
from typing import Tuple, Dict, Union
from threading import Lock
import time

from message_center import Text


class FlowControl:
    def __init__(self, bot: TeleBot) -> None:
        self.bot = bot
        self._message_queue: deque[Tuple[Union[str, int], Text]] = deque()
        self._last_sent_time: Dict[Union[str, int], float] = dict()
        self.lock = Lock()

    def __pop_queue(self) -> Tuple[Union[str, int], Text]:
        return self._message_queue.popleft()

    def append_queue(self, chat_id: str | int, text: Text) -> None:
        self._message_queue.append((chat_id, text))
        self._notify()

    def _notify(self):
        with self.lock:
            if not self._message_queue:
                return

            chat_id, text = self.__pop_queue()
            current_time = time.time()
            if chat_id in self._last_sent_time and current_time - self._last_sent_time[chat_id] < 1:
                time.sleep(
                    1.1 - (current_time - self._last_sent_time[chat_id]))
            self.bot.send_message(chat_id, text.text,
                                  parse_mode=text.parse_mode)
            self._last_sent_time[chat_id] = time.time()
            time.sleep(0.04)
