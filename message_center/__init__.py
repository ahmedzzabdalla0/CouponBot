from abc import ABC, abstractmethod
import re
from enums import ParseMode


class MessagesCenter(ABC):

    @staticmethod
    @abstractmethod
    def generate(**kargs):
        ...


class Text:

    BOLD = "BOLDCONSTANT"
    ITALIC = "ITALICCONSTANT"
    REFACTOR_REGEX = r"(?<!\\)(_|\*|\[|\]|\(|\)|\~|`|>|#|\+|-|=|\||\{|\}|\.|\!)"

    def __init__(self, text: str) -> None:
        self.__text = self.refactor(text)
        self.parse_mode: str | None = None

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = self.refactor(text)

    @staticmethod
    def refactor(text: str) -> str:
        return re.sub(Text.REFACTOR_REGEX, lambda t: "\\"+t.group(), text)

    @staticmethod
    def bold(text: str) -> str:
        return Text.BOLD + text + Text.BOLD

    @staticmethod
    def italic(text: str) -> str:
        return Text.ITALIC + text + Text.ITALIC

    def add(self, text: str) -> None:
        self.text += text

    def add_new_space(self, text: str, num_of_sp: int = 1) -> None:
        self.text += ' ' * num_of_sp + text

    def add_new_line(self, text: str, num_of_br: int = 1) -> None:
        self.text += '\n' * num_of_br + text

    def close_text(self) -> None:
        if self.BOLD in self.__text or self.ITALIC in self.__text:
            self.parse_mode = ParseMode.MARKDOWN_V2.value if self.parse_mode is None else self.parse_mode
        self.__text = self.text.replace(
            self.BOLD, "*").replace(self.ITALIC, "_")

    def __repr__(self) -> str:
        return self.text

    def __str__(self) -> str:
        return self.text
