from message_center import MessagesCenter, Text


class LoginEnterPass(MessagesCenter):

    @staticmethod
    def generate() -> Text:

        text = Text(Text.bold(f"أدخل كلمة المرور من فضلك"))
        text.close_text()

        return text


class LoginIncorrectPass(MessagesCenter):

    @staticmethod
    def generate() -> Text:

        text = Text(Text.bold(f"المعذرة: كلمة المرور خاطئة"))
        text.close_text()

        return text


class LoginNotExisit(MessagesCenter):

    @staticmethod
    def generate() -> Text:

        text = Text(Text.bold(f"المعذرة أنت غير مسجل"))
        text.close_text()

        return text
