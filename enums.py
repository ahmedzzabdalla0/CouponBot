from enum import Enum


class AuthStatus(Enum):
    Authenticated = "authenticated"
    InvalidPassword = "invalidPassword"
    InvalidChatId = "invalidChatId"


class Gender(Enum):
    male = "male"
    female = "female"


class UserType(Enum):
    MANAGER = "manager"
    customer = "customer"
    MERCHANT = "merchant"

# ------------ Sequence Status ------------


class Login(Enum):

    ReceivePassword = "receivePassword"

    Authenticated = "authenticated"
    InvalidPassword = "invalidPassword"
    InvalidChatId = "invalidChatId"

# ------------ TELEGRAM SYSTEM ------------


class ParseMode(Enum):
    HTML = 'HTML'
    MARKDOWN = 'Markdown'
    MARKDOWN_V2 = 'MarkdownV2'
