import json
import telebot
from telebot import types
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound

from BLL.Services.UserService import UserService
from BLL.Services.GroupService import GroupService
from DAL.Entities.User import User


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
                                           first_choice)

        def first_choice(message):
            user_data = dict()
            if message.text == "Регистрация":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('На главную')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                "Введите желаемый логин",
                                                                reply_markup=keyboard),
                                               registration_login, user_data=user_data)
            elif message.text == "Войти":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('На главную')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                "Введите свой логин",
                                                                reply_markup=keyboard),
                                               check_login)

        def registration_login(message, user_data):

            if message.text == "На главную":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Войти', 'Регистрация')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                'Главная страница',
                                                                reply_markup=keyboard),
                                               first_choice)
            else:
                try:
                    session = sessionmaker(bind=self.db_engine)()
                    UserService(session).get_user(message.text)
                    session.close()
                    bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                    "Этот логин занят, введите другой"),
                                                   registration_login, user_data=user_data)
                except NoResultFound:
                    keyboard = telebot.types.ReplyKeyboardMarkup()
                    keyboard.row('Назад', 'На главную')
                    user_data["login"] = message.text
                    bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                    "Введите желаемый пароль",
                                                                    reply_markup=keyboard),
                                                   registration_password, user_data=user_data)

        def registration_password(message, user_data):
            if message.text == "На главную":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Войти', 'Регистрация')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                'Главная страница',
                                                                reply_markup=keyboard),
                                               first_choice)
            elif message.text == "Назад":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('На главную')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                f"Введён логин:{user_data['login']}\n"
                                                                f"Введите желаемый логин",
                                                                reply_markup=keyboard),
                                               registration_login, user_data=user_data)
            else:
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Назад', 'На главную')
                user_data["password"] = message.text
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                "Введите свой телеграм канал по типу @channel",
                                                                reply_markup=keyboard),
                                               registration_tg_channel, user_data=user_data)

        def registration_tg_channel(message, user_data):
            if message.text == "На главную":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Войти', 'Регистрация')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                'Главная страница',
                                                                reply_markup=keyboard),
                                               first_choice)
            elif message.text == "Назад":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Назад', 'На главную')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                f"Введён пароль:{user_data['password']}\n"
                                                                f"Введите желаемый пароль",
                                                                reply_markup=keyboard),
                                               registration_password, user_data=user_data)
            else:
                try:
                    session = sessionmaker(bind=self.db_engine)()
                    session.query(User).filter(User.tg_channel == message.text).one()
                    session.close()
                    bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                    "Этот канал уже обслуживается, введите другой"),
                                                   registration_tg_channel, user_data=user_data)
                except NoResultFound:
                    keyboard = telebot.types.ReplyKeyboardMarkup()
                    keyboard.row('Назад', 'На главную')
                    user_data["tg_channel"] = message.text
                    bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                    "Введите свой токен приложения вконтакте",
                                                                    reply_markup=keyboard),
                                                   registration_vk_token, user_data=user_data)

        def registration_vk_token(message, user_data):
            if message.text == "На главную":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Войти', 'Регистрация')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                'Главная страница',
                                                                reply_markup=keyboard),
                                               first_choice)
            elif message.text == "Назад":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Назад', 'На главную')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                f"Введён канал:{user_data['tg_channel']}\n"
                                                                f"Введите желаемый канал",
                                                                reply_markup=keyboard),
                                               registration_tg_channel, user_data=user_data)
            else:
                try:
                    session = sessionmaker(bind=self.db_engine)()
                    session.query(User).filter(User.vk_token == message.text).one()
                    session.close()
                    bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                    "Этот токен вконтакте уже используется, введите другой"),
                                                   registration_vk_token, user_data=user_data)
                except NoResultFound:
                    keyboard = telebot.types.ReplyKeyboardMarkup()
                    keyboard.row('Назад', 'На главную')
                    user_data["vk_token"] = message.text
                    bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                    "Введите свой токен приложения EPN",
                                                                    reply_markup=keyboard),
                                                   registration_epn_api_token, user_data=user_data)

        def registration_epn_api_token(message, user_data):
            if message.text == "На главную":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Войти', 'Регистрация')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                'Главная страница',
                                                                reply_markup=keyboard),
                                               first_choice)
            elif message.text == "Назад":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Назад', 'На главную')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                f"Введён токен ВК:{user_data['vk_token']}\n"
                                                                f"Введите новый токен",
                                                                reply_markup=keyboard),
                                               registration_vk_token, user_data=user_data)
            else:
                try:
                    session = sessionmaker(bind=self.db_engine)()
                    session.query(User).filter(User.epn_api_token == message.text).one()
                    session.close()
                    keyboard = telebot.types.ReplyKeyboardMarkup()
                    keyboard.row('Назад', 'На главную')
                    bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                    "Этот токен EPN уже используется, введите другой",
                                                                    reply_markup=keyboard),
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
                            keyboard = telebot.types.ReplyKeyboardMarkup()
                            keyboard.row('Назад', 'На главную')
                            user_data["epn_api_token"] = message.text
                            bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                            "Введите свой хэш приложения EPN",
                                                                            reply_markup=keyboard),
                                                           registration_epn_hash, user_data=user_data)
                        elif response.json()["error"] == 'Bad auth data!':
                            keyboard = telebot.types.ReplyKeyboardMarkup()
                            keyboard.row('Назад', 'На главную')
                            bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                            "Epn не подтвердил наличие токена, "
                                                                            "убедитесь в его валидности и попробуйте "
                                                                            "ввести снова", reply_markup=keyboard),
                                                           registration_epn_api_token, user_data=user_data)

        def registration_epn_hash(message, user_data):
            if message.text == "На главную":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Войти', 'Регистрация')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                'Главная страница',
                                                                reply_markup=keyboard),
                                               first_choice)
            elif message.text == "Назад":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Назад', 'На главную')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                f"Введён токен приложения EPN:{user_data['epn_api_token']}\n"
                                                                f"Введите новый токен",
                                                                reply_markup=keyboard),
                                               registration_epn_api_token, user_data=user_data)
            else:
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

                    if 'error' in response.json():
                        if response.json()["error"] == 'Bad deeplink hash!':
                            keyboard = telebot.types.ReplyKeyboardMarkup()
                            keyboard.row('Назад', 'На главную')
                            bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                            "Epn не подтвердил наличие хэша, "
                                                                            "убедитесь в его валидности и введите снова",
                                                                            reply_markup=keyboard),
                                                           registration_epn_hash, user_data=user_data)

                    else:
                        keyboard = telebot.types.ReplyKeyboardMarkup()
                        keyboard.row('Назад', 'На главную')
                        user_data["epn_hash"] = message.text
                        bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                        "Введите время работы бота на вашем канале по типу "
                                                                        "начало:конец\n\nПример: 9:21 или 8:20",
                                                                        reply_markup=keyboard),
                                                       registration_post_time, user_data=user_data)
                except Exception as e:
                    print(e)

        def registration_post_time(message, user_data):
            if message.text == "На главную":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Войти', 'Регистрация')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                'Главная страница',
                                                                reply_markup=keyboard),
                                               first_choice)
            elif message.text == "Назад":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Назад', 'На главную')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                f"Введён хэш приложения EPN:{user_data['epn_hash']}\n"
                                                                f"Введите новый хэш",
                                                                reply_markup=keyboard),
                                               registration_epn_api_token, user_data=user_data)
            else:
                if ":" in message.text:
                    time = message.text.split(':')
                    user_data["start_timer"] = time[0]
                    user_data["end_timer"] = time[1]

                    session = sessionmaker(bind=self.db_engine)()
                    user_serv = UserService(session)
                    user_serv.add_user(user_data)
                    session.commit()
                    session.close()

                    keyboard = telebot.types.ReplyKeyboardMarkup()
                    keyboard.row('Войти', 'Регистрация')
                    bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                    'Пользователь успешно зарегистрирован',
                                                                    reply_markup=keyboard),
                                                   first_choice)

        def check_login(message):
            if message.text == "На главную":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Войти', 'Регистрация')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                'Главная страница',
                                                                reply_markup=keyboard),
                                               first_choice)
            else:
                session = sessionmaker(bind=self.db_engine)()
                try:
                    user = UserService(session).get_user(message.text)
                    session.close()
                    keyboard = telebot.types.ReplyKeyboardMarkup()
                    keyboard.row('На главную')
                    bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                    "Введите свой пароль",
                                                                    reply_markup=keyboard),
                                                   check_password, user=user)
                except NoResultFound:
                    session.close()
                    keyboard = telebot.types.ReplyKeyboardMarkup()
                    keyboard.row('Войти', 'Регистрация')
                    bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                    'Пользователя с таким логином не существует!',
                                                                    reply_markup=keyboard),
                                                   first_choice)

        def check_password(message, user):
            if message.text == "На главную":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Войти', 'Регистрация')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                'Главная страница',
                                                                reply_markup=keyboard),
                                               first_choice)
            else:
                if message.text == user.password:
                    keyboard = telebot.types.ReplyKeyboardMarkup()
                    keyboard.row('Оплата', 'Меню')
                    keyboard.row('На главную')
                    bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                    "Выберите опцию",
                                                                    reply_markup=keyboard),
                                                   main_menu, login=user.login)
                else:
                    keyboard = telebot.types.ReplyKeyboardMarkup()
                    keyboard.row('На главную')
                    bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                    'Пароль неверный!\n Попробуйте снова',
                                                                    reply_markup=keyboard),
                                                   check_password, user=user)

        def main_menu(message, login):
            if message.text == "Оплата":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Оплата', 'Меню')
                keyboard.row('На главную')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                "Услуга недоступна, выберите другую опцию",
                                                                reply_markup=keyboard),
                                               main_menu, login=login)
            elif message.text == "Меню":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Включить', 'Отключить')
                keyboard.row('Добавить группу', 'Удалить группу')
                keyboard.row('Изменить частоту', 'Изменить промежутки')
                keyboard.row('На главную', 'Удалить пользователя')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                "Выберите опцию", reply_markup=keyboard),
                                               menu, login=login)
            elif message.text == "На главную":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Войти', 'Регистрация')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                'Главная страница',
                                                                reply_markup=keyboard),
                                               first_choice)

        # def payment(message, login):
        #     keyboard = telebot.types.ReplyKeyboardMarkup()
        #     keyboard.row('Оплата', 'Меню')
        #     keyboard.row('На главную')
        #     bot.register_next_step_handler(bot.send_message(message.from_user.id,
        #                                                     "Выберите опцию",
        #                                                     reply_markup=keyboard),
        #                                    main_menu, login=login)

        def menu(message, login):
            if message.text == "Включить":
                session = sessionmaker(bind=self.db_engine)()
                user = UserService(session).get_user(login)
                if user.active:
                    bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                    "Бот уже работает!"),
                                                   menu, login=login)
                    session.close()
                elif not user.active:
                    user.active = True
                    session.commit()
                    session.close()
                    bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                    "Бот запущен!"),
                                                   menu, login=login)
            elif message.text == "Отключить":
                session = sessionmaker(bind=self.db_engine)()
                user = UserService(session).get_user(login)
                if user.active:
                    user.active = False
                    session.commit()
                    session.close()
                    bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                    "Бот отключён!"),
                                                   menu, login=login)
                elif not user.active:
                    bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                    "Бот уже отключён!"),
                                                   menu, login=login)
                    session.close()
            elif message.text == "На главную":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Войти', 'Регистрация')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                'Главная страница',
                                                                reply_markup=keyboard),
                                               first_choice)
            elif message.text == "Добавить группу":
                delete_keyboard = types.ReplyKeyboardRemove(selective=False)
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                "Введите имя группы ВК",
                                                                reply_markup=delete_keyboard),
                                               add_group_name, login=login)
            elif message.text == "Удалить группу":
                delete_keyboard = types.ReplyKeyboardRemove(selective=False)
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                "Введите ID группы ВК",
                                                                reply_markup=delete_keyboard),
                                               delete_group, login=login)
            elif message.text == "Изменить частоту":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Раз в 30 минут', 'Раз в 1 час')
                keyboard.row('Раз в 2 часа', 'Раз в 3 часа')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                "Выберите опцию",
                                                                reply_markup=keyboard),
                                               change_periodicity, login=login)
            elif message.text == "Изменить промежутки":
                delete_keyboard = types.ReplyKeyboardRemove(selective=False)
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                "Введите время по примеру 9:21",
                                                                reply_markup=delete_keyboard),
                                               change_post_time, login=login)
            elif message.text == "Удалить пользователя":
                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Отмена')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                "Введите пароль пользователя",
                                                                reply_markup=keyboard),
                                               delete_user, login=login)

        def add_group_name(message, login):
            group = {"name": message.text}
            bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                            "Введите ID группы ВК"),
                                           add_group_id, login=login, group=group)

        def add_group_id(message, login, group):
            session = sessionmaker(bind=self.db_engine)()
            user = UserService(session).get_user(login)
            group["vk_group_id"] = message.text
            group["user_id"] = user.id
            GroupService(session).add_group(group)
            session.commit()
            session.close()

            keyboard = telebot.types.ReplyKeyboardMarkup()
            keyboard.row('Включить', 'Отключить')
            keyboard.row('Добавить группу', 'Удалить группу')
            keyboard.row('Изменить частоту', 'Изменить промежутки')
            keyboard.row('На главную', 'Удалить пользователя')
            bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                            "Группа успешно добавлена", reply_markup=keyboard),
                                           menu, login=login)

        def delete_group(message, login):
            session = sessionmaker(bind=self.db_engine)()
            user = UserService(session).get_user(login)
            group_data = {"vk_group_id": message.text, "user_id": user.id}
            try:
                group = GroupService(session).get_group(group_data)
                GroupService(session).delete_group(group.id)
                session.commit()
                session.close()

                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Включить', 'Отключить')
                keyboard.row('Добавить группу', 'Удалить группу')
                keyboard.row('Изменить частоту', 'Изменить промежутки')
                keyboard.row('На главную', 'Удалить пользователя')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                "Группа успешно удалена", reply_markup=keyboard),
                                               menu, login=login)
            except NoResultFound:
                session.close()

                keyboard = telebot.types.ReplyKeyboardMarkup()
                keyboard.row('Включить', 'Отключить')
                keyboard.row('Добавить группу', 'Удалить группу')
                keyboard.row('Изменить частоту', 'Изменить промежутки')
                keyboard.row('На главную', 'Удалить пользователя')
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                "Группы не существует", reply_markup=keyboard),
                                               menu, login=login)

        def change_periodicity(message, login):
            session = sessionmaker(bind=self.db_engine)()
            user = UserService(session).get_user(login)
            if message.text == "Раз в 30 минут":
                user.post_iteration = 2
            elif message.text == "Раз в 1 час":
                user.post_iteration = 4
            elif message.text == "Раз в 2 часа":
                user.post_iteration = 8
            elif message.text == "Раз в 3 часа":
                user.post_iteration = 12
            else:
                user.post_iteration = 4
            session.commit()
            session.close()

            keyboard = telebot.types.ReplyKeyboardMarkup()
            keyboard.row('Включить', 'Отключить')
            keyboard.row('Добавить группу', 'Удалить группу')
            keyboard.row('Изменить частоту', 'Изменить промежутки')
            keyboard.row('На главную', 'Удалить пользователя')
            bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                            "Время успешно изменено!", reply_markup=keyboard),
                                           menu, login=login)

        def change_post_time(message, login):
            session = sessionmaker(bind=self.db_engine)()
            user = UserService(session).get_user(login)

            if ":" in message.text:
                time = message.text.split(':')

                user.start_timer = int(time[0])
                user.end_timer = int(time[1])
                session.commit()
                session.close()

            keyboard = telebot.types.ReplyKeyboardMarkup()
            keyboard.row('Включить', 'Отключить')
            keyboard.row('Добавить группу', 'Удалить группу')
            keyboard.row('Изменить частоту', 'Изменить промежутки')
            keyboard.row('На главную', 'Удалить пользователя')
            bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                            "Время успешно изменено!", reply_markup=keyboard),
                                           menu, login=login)

        def delete_user(message, login):

            keyboard = telebot.types.ReplyKeyboardMarkup()
            keyboard.row('Включить', 'Отключить')
            keyboard.row('Добавить группу', 'Удалить группу')
            keyboard.row('Изменить частоту', 'Изменить промежутки')
            keyboard.row('На главную', 'Удалить пользователя')

            if message.text == "Отмена":
                bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                "Удаление отменено!",
                                                                reply_markup=keyboard),
                                               menu,
                                               login=login)
            else:
                session = sessionmaker(bind=self.db_engine)()
                user = UserService(session).get_user(login)
                if user.password == message.text:
                    UserService(session).delete_user(user.id)
                    session.commit()
                    session.close()
                    bot.send_message(message.from_user.id, "Пользователь удалён!")
                else:
                    session.close()
                    bot.register_next_step_handler(bot.send_message(message.from_user.id,
                                                                    "Неверный пароль!", reply_markup=keyboard),
                                                   menu, login=login)

        bot.polling()
