import telebot
from telebot import types


class TGService:

    def __init__(self, user, bot_token, post_data: dict):
        self.user = user
        self.bot_token = bot_token
        self.post_data = post_data

    def post_to_channel(self):
        bot = telebot.TeleBot(self.bot_token)

        markup = types.InlineKeyboardMarkup()
        btn_my_site = types.InlineKeyboardButton(text='Заказать', url=self.post_data["url"])
        markup.add(btn_my_site)

        bot.send_photo(chat_id=self.user.tg_channel, photo=self.post_data[""],
                       caption=f"\n {self.post_data['title']}\n\n"
                               f"Цена: {self.post_data['price']}\n"
                               f"Скидка: {str(self.post_data['sale'])}%",
                       reply_markup=markup)

        return 0
