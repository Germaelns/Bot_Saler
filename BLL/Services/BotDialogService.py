import json
import telebot
from telebot import types
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound

from BLL.Services.UserService import UserService
from DAL.Entities.User import User


# db_session = sessionmaker(bind=db_engine)()
# self.session.query(User).filter(User.login == login).one()


class BotDialogService:

    def __init__(self, postgres):
        self.db_engine = create_engine(f"postgres://{postgres['user']}:{postgres['password']}@"
                                       f"{postgres['host']}:{postgres['port']}/{postgres['db']}",
                                       pool_pre_ping=True)

    def main_dialog(self, bot):

        @bot.message_handler(content_types=['text'])
        def start_message(message):
            keyboard = telebot.types.ReplyKeyboardMarkup()
            keyboard.row('Войти', 'Регистрация')

            bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                            "Добрый день, выберите необходимую опцию",
                                                            reply_markup=keyboard),
                                           first_choise)

        def first_choise(message):
            if message.text == "Регистрация":
                delete_keyboard = types.ReplyKeyboardRemove(selective=False)
                user_data = dict()
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                "Введите желаемый логин",
                                                                reply_markup=delete_keyboard),
                                               registration_login, user_data=user_data)

        def registration_login(message, user_data):
            try:
                session = sessionmaker(bind=self.db_engine)()
                UserService(session).get_user(message.text)
                session.close()
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                "Этот логин занят, введите другой"),
                                               registration_login, user_data=user_data)
            except NoResultFound:
                user_data["login"] = message.text
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                "Введите желаемый пароль"),
                                               registration_password, user_data=user_data)

        def registration_password(message, user_data):
            user_data["password"] = message.text
            bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                            "Введите свой телеграм канал по типу @channel"),
                                           registration_tg_channel, user_data=user_data)

        def registration_tg_channel(message, user_data):
            try:
                session = sessionmaker(bind=self.db_engine)()
                session.query(User).filter(User.tg_channel == message.text).one()
                session.close()
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                "Этот канал уже обслуживается, введите другой"),
                                               registration_tg_channel, user_data=user_data)
            except NoResultFound:
                user_data["tg_channel"] = message.text
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                "Введите свой токен приложения вконтакте"),
                                               registration_vk_token, user_data=user_data)

        def registration_vk_token(message, user_data):
            try:
                session = sessionmaker(bind=self.db_engine)()
                session.query(User).filter(User.vk_token == message.text).one()
                session.close()
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                "Этот токен вконтакте уже используется, введите другой"),
                                               registration_vk_token, user_data=user_data)
            except NoResultFound:
                user_data["vk_token"] = message.text
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                "Введите свой токен приложения EPN"),
                                               registration_epn_api_token, user_data=user_data)

        def registration_epn_api_token(message, user_data):

            try:
                session = sessionmaker(bind=self.db_engine)()
                session.query(User).filter(User.epn_api_token == message.text).one()
                session.close()
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                "Этот токен EPN уже используется, введите другой"),
                                               registration_epn_api_token, user_data=user_data)
            except NoResultFound:
                import requests
                data = {
                    "user_api_key": "" + message.text,
                    "user_hash": "",
                    "api_version": 1,
                    "requests": {

                    }
                }
                headers = {
                    'Content-Type': 'application/json'
                }

                response = requests.post("http://api.epn.bz/json",
                                         data=json.dumps(data),
                                         headers=headers)

                if "error" in response.json():
                    if response.json()["error"] == 'Bad deeplink hash!':
                        user_data["epn_api_token"] = message.text
                        bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                        "Введите свой хэш приложения EPN"),
                                                       registration_epn_hash, user_data=user_data)
                    elif response.json()["error"] == 'Bad auth data!':
                        bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                        "Epn не подтвердил наличие токена, "
                                                                        "убедитесь в его валидности и попробуйте "
                                                                        "ввести снова"),
                                                       registration_epn_api_token, user_data=user_data)

        def registration_epn_hash(message, user_data):
            try:
                session = sessionmaker(bind=self.db_engine)()
                session.query(User).filter(User.epn_hash == message.text).one()
                session.close()
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                "Этот хэш EPN уже используется, введите другой"),
                                               registration_epn_api_token, user_data=user_data)
            except NoResultFound:
                import requests
                data = {
                    "user_api_key": "" + user_data["epn_api_token"],
                    "user_hash": "" + message.text,
                    "api_version": 1,
                    "requests": {

                    }
                }
                headers = {
                    'Content-Type': 'application/json'
                }

                response = requests.post("http://api.epn.bz/json",
                                         data=json.dumps(data),
                                         headers=headers)
                if "error" in response.json():
                    if response.json()["error"] == 'Bad deeplink hash!':
                        bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                        "Epn не подтвердил наличие хэша, "
                                                                        "убедитесь в его валидности"),
                                                       registration_epn_hash, user_data=user_data)
                else:
                    user_data["epn_hash"] = message.text
                    bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                    "Введите время работы бота на вашем канале по типу "
                                                                    "начало:конец\n\nПример: 9:21 или 8:20"),
                                                   registration_post_time, user_data=user_data)
            except Exception as e:
                print(e)

        def registration_post_time(message, user_data):
            time = message.text.split(':')
            user_data["start_timer"] = time[0]
            user_data["end_timer"] = time[1]

            session = sessionmaker(bind=self.db_engine)()
            user_serv = UserService(session)
            user_serv.add_user(user_data)
            session.commit()
            session.close()

        bot.polling()
