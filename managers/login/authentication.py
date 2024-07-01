from datetime import datetime

import pytz
from enums import AuthStatus, UserType
from db import get_db_session
from db.models import Manager, Merchant, LoginRecord


# def check_user(message, bot, types, force_reply_markup, user_message, user_data, user_login, message_ids, confirm_login):
#     chat_id = message.chat.id
#     delete_previous_message(chat_id, bot, message_ids)

#     try:
#         user_data.pop(chat_id)
#         user_message.pop(chat_id)
#     except:
#         pass
#     if not user_login.get(chat_id):
#         user_login[chat_id] = 'managerLogin'
#     session = get_db_session()
#     if True:
#         current_date = datetime.now(pytz.UTC)
#         last_login = session.query(Login).filter_by(user_id=chat_id).first()
#         if last_login:
#             last_login_date = last_login.last_login_date.replace(
#                 tzinfo=pytz.UTC) if last_login.last_login_date.tzinfo is None else last_login.last_login_date.astimezone(pytz.UTC)
#             time_diff = current_date - last_login_date
#             time_diff_minutes = time_diff.total_seconds() / 60
#             if time_diff_minutes < 0:
#                 time_diff_minutes = 0

#             if time_diff_minutes > 30:
#                 if chat_id in user_login and user_login[chat_id] == 'managerLogin':
#                     confirm_login[chat_id] = 'managerPassword'
#                     sent_message = bot.send_message(
#                         chat_id, "أدخل كلمة المرور من فضلك:", reply_markup=force_reply_markup())
#                     message_ids[chat_id] = sent_message.message_id
#                 elif chat_id in user_login and user_login[chat_id] == 'salerLogin':
#                     confirm_login[chat_id] = 'salerPassword'
#                     sent_message = bot.send_message(
#                         chat_id, "أدخل كلمة المرور من فضلك:", reply_markup=force_reply_markup())
#                     message_ids[chat_id] = sent_message.message_id
#                 elif chat_id in user_login and user_login[chat_id] == 'userLogin':
#                     sent_message = bot.send_message(
#                         chat_id, 'المعذرة أنت غير مسجل')
#                     message_ids[chat_id] = sent_message.message_id
#             else:
#                 login_record = session.query(
#                     Login).filter_by(user_id=chat_id).first()
#                 if login_record:
#                     login_record.last_login_date = datetime.now(pytz.UTC)
#                     session.commit()

#                 if chat_id in user_login and user_login[chat_id] == 'managerLogin':
#                     control_panel(message, bot, types, message_ids)
#                 elif chat_id in user_login and user_login[chat_id] == 'salerLogin':
#                     saler_controlPanel(message, bot, types, message_ids)
#                 elif chat_id in user_login and user_login[chat_id] == 'userLogin':
#                     main_user_list(message, bot, types, message_ids)
#         else:
#             sent_message = bot.send_message(chat_id, 'المعذرة أنت غير مسجل')
#             message_ids[chat_id] = sent_message.message_id

#     '''finally:
#         session.close()'''


class Authenticator:

    def __init__(self, chat_id: int | str) -> None:
        self.chat_id = chat_id

    def authenticate(self, password: str) -> AuthStatus:

        session = get_db_session()

        manager = session.query(Manager).filter_by(
            chat_id=self.chat_id).first()

        merchant = session.query(Merchant).filter_by(
            chat_id=self.chat_id).first()

        user = manager or merchant

        if user:

            if user.password == password:
                return AuthStatus.Authenticated

            else:
                return AuthStatus.InvalidPassword

        else:

            return AuthStatus.InvalidChatId

    def last_auth(self) -> LoginRecord | None:

        session = get_db_session()

        return session.query(LoginRecord).filter_by(user_id=self.chat_id).first()

    def last_auth_in_sec(self) -> int | None:

        last_record = self.last_auth()
        if last_record:
            current_date = datetime.now(pytz.UTC)
            last_record_datetime: datetime = last_record.last_login_date
            last_record_utc = last_record_datetime.replace(
                tzinfo=pytz.UTC) if last_record_datetime.tzinfo is None else last_record_datetime.astimezone(pytz.UTC)
            return (current_date - last_record_utc).seconds

    def last_auth_in_min(self) -> float | None:

        seconds = self.last_auth_in_sec()
        if seconds is not None:
            return seconds / 60

    def new_login_record(self) -> float | None:

        session = get_db_session()

        manager = session.query(Manager).filter_by(
            chat_id=self.chat_id).first()

        merchant = session.query(Merchant).filter_by(
            chat_id=self.chat_id).first()

        now = datetime.now(pytz.UTC)

        record_query = LoginRecord(
            user_id=manager.id if manager else merchant.id,
            user_type=UserType.MANAGER.value if manager else UserType.MERCHANT.value,
            last_login_date=now
        )

        session.add(record_query)
        session.commit()

# def check_manager_permission(message, bot, types, main_markup, user_login, message_ids, confirm_login):
#     chat_id = message.chat.id
#     password = message.text
#     delete_previous_message(chat_id, bot, message_ids)
#     session = get_db_session()
#     manager = session.query(Manager).filter_by(user_id=chat_id).first()
#     if manager and manager.password == password and manager.permission == 'manager':
#         login_record = session.query(Login).filter_by(user_id=chat_id).first()
#         if login_record:
#             login_record.last_login_date = datetime.now()
#             session.commit()
#         control_panel(message, bot, types, message_ids)
#     else:
#         sent_message = bot.send_message(
#             chat_id, 'المعذرة: كلمة المرور خاطئة', reply_markup=main_markup)
#     del confirm_login[chat_id]
#     session.close()


# def check_saler_permission(message, bot, types, main_markup, user_login, message_ids, confirm_login):
#     chat_id = message.chat.id
#     password = message.text
#     delete_previous_message(chat_id, bot, message_ids)
#     session = get_db_session()
#     saler = session.query(Merchant).filter_by(user_id=chat_id).first()
#     if saler and saler.password == password and saler.permission == 'valid':
#         login_record = session.query(Login).filter_by(user_id=chat_id).first()
#         if login_record:
#             login_record.last_login_date = datetime.now()
#             session.commit()
#         saler_controlPanel(message, bot, types, message_ids)
#     else:
#         sent_message = bot.send_message(
#             chat_id, 'المعذرة: كلمة المرور خاطئة', reply_markup=main_markup)
#         message_ids[chat_id] = sent_message.message_id
#     del confirm_login[chat_id]
#     session.close()


# def login_options(call, bot, types, user_login, message_ids):
#     chat_id = call.message.chat.id
#     bot.send_message(chat_id, 'done')
#     login_types = call.data.split('_')[1]
#     if login_types == 'saler':
#         user_login[chat_id] = 'salerLogin'
#         status = 'تاجر'
#     elif login_types == 'user':
#         user_login[chat_id] = 'userLogin'
#         status = 'عميل'
#     elif login_types == 'manager':
#         user_login[chat_id] = 'managerLogin'
#         status = 'مدير'
#     sent_message = bot.send_message(chat_id, f'تم تسجيل دخولك ك{status}')
#     message_ids[chat_id] = sent_message.message_id
