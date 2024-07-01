import telebot


def force_reply_markup():
    return telebot.types.ForceReply(selective=True)
