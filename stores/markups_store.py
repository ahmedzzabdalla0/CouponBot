import buttons_store
from telebot.types import ReplyKeyboardMarkup

main_markup = ReplyKeyboardMarkup(text='القائمة الرئيسية')
main_markup.add(buttons_store.main_button)
